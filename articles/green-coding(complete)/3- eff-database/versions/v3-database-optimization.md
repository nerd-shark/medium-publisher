# Database Optimization: Cut Energy Costs by 70%

*Part 3 of the Green Coding Series*

A production PostgreSQL database: 50K queries/second, $15K/month RDS bill. The team had "optimized" with a db.r5.8xlarge (32 vCPUs).

The problem? A single query running 30K times/second:

```sql
SELECT * FROM users WHERE email = 'user@example.com'
```

No index. Full table scan of 10 million rows. 300 billion row scans per second.

One index later:

```sql
CREATE INDEX idx_users_email ON users(email);
```

Result: Query time 80ms → 0.5ms. CPU -70%. Downgraded to db.r5.2xlarge. Cost: $4K/month. **Savings: $11K/month, 73% less energy.**

## Why Databases Waste Energy

Databases consume more energy than any other part of your stack. A single query touches four subsystems:

**1. Disk I/O (40-50% of energy)**
- SSD read: ~100 microseconds, 0.1 watts
- Memory read: ~100 nanoseconds, 0.0001 watts (1000x faster)
- Full table scan on 10M rows = 10,000 disk operations
- At 1000 queries/second = 100 kilowatts continuous (10 homes worth)

**2. CPU (30-40% of energy)**
- Query planning: 1-2ms simple, 10-50ms complex
- At 1000 queries/second = 1-50 CPU cores just planning
- Join on 1M rows = 100MB hash table, 100-500ms CPU

**3. Memory (10-15% of energy)**
- Buffer pool: ~1 watt per GB
- 128GB server with 100GB buffer = 100 watts continuous
- Working memory for complex queries adds more

**4. Network (5-10% of energy)**
- 2-5 watts per 1 Gbps
- 500MB transfer = 6 seconds at 80 MB/s = 12 watt-seconds

### The Multiplication Effect

One inefficient query × millions of executions = catastrophic waste.

**Missing index example:**
- Efficient (with index): 1ms, 0.01 watt-seconds
- Inefficient (full scan): 100ms, 1 watt-second
- **100x more energy per query**

At 1000 queries/second:
- Efficient: 10 watts
- Inefficient: 1000 watts (10 computers running continuously)

**Annual impact:**
- Efficient: 87.6 kWh, $8.76, 35 kg CO2e
- Inefficient: 8,760 kWh, $876, 3,504 kg CO2e
- **Difference: $867/year, 3.5 tons CO2e for ONE missing index**

### The Good News

Small changes = massive impact:
- Queries run millions of times (fix once, save millions)
- Optimizations multiply (index + caching + batching = 100x-1000x improvement)
- Right-sizing reduces idle waste (smaller instance = less idle power)

## Pattern 1: Index Strategically

**Problem:** Sequential scans read every row. 10M rows = 10M disk reads.

**Solution:** Index what you query, not what you might query someday.

```sql
-- Before: Full table scan
SELECT * FROM orders WHERE customer_id = 123 AND status = 'pending';
-- Seq Scan: reads all 10M rows

-- After: Composite index
CREATE INDEX idx_orders_customer_status ON orders(customer_id, status);
-- Index Scan: reads ~28 rows (23 B-tree lookups + 5 matching rows)

-- Best: Covering index (no table access)
CREATE INDEX idx_orders_covering ON orders(customer_id, status) 
  INCLUDE (id, total, created_at);
```

**Find missing indexes:**

```sql
-- PostgreSQL: Find sequential scans
SELECT schemaname, tablename, seq_scan, seq_tup_read, idx_scan
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC LIMIT 20;
```

**Impact:**
- Query time: 500ms → 2ms (250x faster)
- CPU: -60%
- Disk I/O: -95%
- Energy: ~50% savings for read-heavy workloads

**Key:** Profile first, index second. Don't guess.

## Pattern 2: Connection Pooling

**Problem:** New connection = 50-100ms overhead (TCP handshake, auth, session setup). For a 1ms query, that's 50-100x more time on overhead than work.

**Solution:** Reuse connections.

```python
# Before: New connection per request
def get_user(user_id):
    conn = psycopg2.connect(DATABASE_URL)  # 50ms!
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()  # 5ms
    return user
# At 1000 req/s: 55 CPU cores just managing connections

# After: Connection pooling
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600
)

def get_user(user_id):
    with engine.connect() as conn:  # 0ms
        result = conn.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return result.fetchone()
# At 1000 req/s: 1 second of actual CPU time
```

**Impact:**
- Connection overhead: 50ms → 0ms
- Memory: -40%
- CPU: -20%
- Throughput: +3x

## Pattern 3: Cache Query Results

**Problem:** Same query executed 1000 times = 1000x the work.

**Solution:** Compute once, serve many.

```python
import redis
import json
from functools import wraps
import hashlib

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def cache_query(ttl=300):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key_data = f"{func.__name__}:{json.dumps(args)}:{json.dumps(kwargs)}"
            cache_key = f"query:{hashlib.md5(key_data.encode()).hexdigest()}"
            
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            result = func(*args, **kwargs)
            redis_client.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator

@cache_query(ttl=600)
def get_user_profile(user_id):
    # Expensive query with joins
    return execute_query("""
        SELECT u.*, p.*, COUNT(f.id) as followers
        FROM users u
        JOIN profiles p ON u.id = p.user_id
        LEFT JOIN followers f ON u.id = f.following_id
        WHERE u.id = %s
        GROUP BY u.id, p.id
    """, (user_id,))
```

**Impact (90% hit rate):**
- Database queries: -90%
- Database CPU: -80%
- Response time: 50ms → 1ms
- Energy: 80-90% savings

**Cache what:**
- User profiles (change infrequently)
- Product catalogs (change daily/hourly)
- Aggregations (expensive to compute)

**Don't cache:**
- Real-time data (stock prices)
- Frequently changing data (shopping cart)

## Pattern 4: Batch Operations

**Problem:** N+1 queries. Loading 100 posts with authors = 101 queries (1 for posts + 100 for authors).

**Solution:** Batch reads and writes.

```python
# Before: N+1 queries (101 queries, ~5 seconds)
posts = execute_query("SELECT * FROM posts LIMIT 100")
for post in posts:
    author = execute_query("SELECT * FROM users WHERE id = %s", (post['author_id'],))
    post['author'] = author

# After: Batched (2 queries, ~0.05 seconds)
posts = execute_query("SELECT * FROM posts LIMIT 100")
author_ids = [post['author_id'] for post in posts]
authors = execute_query("SELECT * FROM users WHERE id IN %s", (tuple(author_ids),))
author_map = {author['id']: author for author in authors}
for post in posts:
    post['author'] = author_map.get(post['author_id'])

# Best: Single JOIN (1 query, ~0.02 seconds)
posts = execute_query("""
    SELECT p.*, u.id as author_id, u.name as author_name
    FROM posts p
    JOIN users u ON p.author_id = u.id
    LIMIT 100
""")
```

**Batch writes:**

```python
# Before: 1000 queries, ~5 seconds
for user_id, score in user_scores.items():
    execute_query("UPDATE users SET score = %s WHERE id = %s", (score, user_id))

# After: 1 query, ~0.05 seconds
values = [(user_id, score) for user_id, score in user_scores.items()]
execute_values(cursor, """
    UPDATE users SET score = v.score
    FROM (VALUES %s) AS v(id, score)
    WHERE users.id = v.id
""", values)
```

**Impact:**
- 1000 queries → 1 query
- Time: 5s → 0.05s (100x faster)
- Network: -99%
- Lock contention: -90%

## Pattern 5: Avoid SELECT *

**Problem:** `SELECT *` reads all columns, even if you only need 2 out of 50. With large TEXT/BLOB columns, you're transferring megabytes when you need kilobytes.

**Solution:** Select only what you use.

```sql
-- Before: 100 posts × 5MB content = 500MB transfer, ~10 seconds
SELECT * FROM blog_posts WHERE author_id = 123;

-- After: 100 posts × 312 bytes = 31KB transfer, ~0.01 seconds
SELECT id, title, excerpt, created_at FROM blog_posts WHERE author_id = 123;

-- Savings: 16,000x less data
```

**Impact:**
- Network: -99%
- Memory: -99%
- Disk I/O: -95% (with covering index)
- Response time: 10s → 0.01s

## Pattern 6: Optimize Joins

**Problem:** Joins are expensive. Nested loop join on 1M × 1M rows = 1 trillion comparisons.

**Solution:** Use appropriate join algorithms and indexes.

```sql
-- Before: Nested loop (1 trillion comparisons)
SELECT * FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.status = 'pending';

-- After: Hash join with indexes
CREATE INDEX idx_orders_status_customer ON orders(status, customer_id);
CREATE INDEX idx_customers_id ON customers(id);

-- Database chooses hash join: 1M + 1M = 2M operations
```

**Join strategies:**
- **Nested loop**: Best for small tables (< 1000 rows)
- **Hash join**: Best for large tables with equality conditions
- **Merge join**: Best for sorted data

**Impact:**
- Query time: 60s → 0.5s (120x faster)
- CPU: -95%
- Memory: -80%

## Pattern 7: Partition Large Tables

**Problem:** Queries on 100M row tables scan millions of rows even with indexes.

**Solution:** Partition by time, geography, or category.

```sql
-- Partition by month
CREATE TABLE orders_2024_01 PARTITION OF orders
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE orders_2024_02 PARTITION OF orders
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Query only scans relevant partition
SELECT * FROM orders WHERE created_at >= '2024-01-15';
-- Scans orders_2024_01 only (3M rows instead of 100M)
```

**Impact:**
- Query time: 5s → 0.15s (33x faster)
- Disk I/O: -97%
- Maintenance: Easier (drop old partitions)

## Pattern 8: Use Read Replicas

**Problem:** Read-heavy workloads overload primary database.

**Solution:** Route reads to replicas, writes to primary.

```python
# Primary for writes
primary_engine = create_engine(PRIMARY_DB_URL)

# Replicas for reads
replica_engine = create_engine(REPLICA_DB_URL)

def get_user(user_id):
    with replica_engine.connect() as conn:  # Read from replica
        return conn.execute("SELECT * FROM users WHERE id = %s", (user_id,))

def update_user(user_id, data):
    with primary_engine.connect() as conn:  # Write to primary
        conn.execute("UPDATE users SET ... WHERE id = %s", (data, user_id))
```

**Impact:**
- Primary load: -80%
- Read throughput: +5x (with 5 replicas)
- Availability: Higher (failover to replica)

## Measuring Impact

**Before optimization:**
```
Queries/second: 1000
Avg query time: 50ms
CPU usage: 80%
Memory usage: 90GB
Instance: db.r5.8xlarge (32 vCPUs)
Cost: $15,000/month
Energy: ~2000 kWh/month
CO2e: ~800 kg/month
```

**After optimization (all patterns):**
```
Queries/second: 1000 (same load)
Avg query time: 2ms (25x faster)
CPU usage: 20%
Memory usage: 20GB
Instance: db.r5.xlarge (4 vCPUs)
Cost: $2,000/month
Energy: ~250 kWh/month
CO2e: ~100 kg/month
```

**Savings:**
- Cost: $13,000/month ($156K/year)
- Energy: 87.5% reduction
- CO2e: 87.5% reduction (8.4 tons/year)

## Implementation Checklist

**Week 1: Quick Wins**
- [ ] Add missing indexes (Pattern 1)
- [ ] Implement connection pooling (Pattern 2)
- [ ] Fix SELECT * queries (Pattern 5)
- [ ] Batch N+1 queries (Pattern 4)

**Week 2: Caching**
- [ ] Set up Redis/Memcached
- [ ] Cache expensive queries (Pattern 3)
- [ ] Monitor cache hit rate (aim for 80-95%)

**Week 3: Advanced**
- [ ] Optimize joins (Pattern 6)
- [ ] Partition large tables (Pattern 7)
- [ ] Set up read replicas (Pattern 8)

**Week 4: Monitor & Tune**
- [ ] Set up query monitoring
- [ ] Track slow queries
- [ ] Right-size database instance
- [ ] Measure energy/cost savings

## Monitoring Queries

```sql
-- PostgreSQL: Find slow queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    max_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 20;

-- Find missing indexes
SELECT 
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read,
    idx_scan
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC;
```

## Key Takeaways

1. **Profile first**: Measure before optimizing
2. **Index strategically**: Not everything, just what you query
3. **Pool connections**: Eliminate connection overhead
4. **Cache aggressively**: 90% hit rate = 90% less database load
5. **Batch operations**: 1 query instead of 1000
6. **Select precisely**: Only columns you need
7. **Optimize joins**: Right algorithm + indexes
8. **Partition wisely**: Reduce scan size
9. **Scale reads**: Use replicas for read-heavy workloads
10. **Monitor continuously**: Track slow queries and resource usage

**The bottom line:** Database optimization isn't about exotic techniques. It's about eliminating waste. A missing index, uncached query, or N+1 problem wastes energy at scale. Fix these, and you'll cut costs 70-90% while reducing your carbon footprint.

Next in the series: Efficient API design patterns that reduce network overhead and server load.

---

*Have database optimization stories? Share them in the comments. What patterns have you found most effective?*
