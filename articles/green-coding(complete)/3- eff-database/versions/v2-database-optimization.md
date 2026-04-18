# Database Optimization Strategies That Cut Energy Costs (And Your Cloud Bill)

*Part 3 of the Green Coding Series*

A production PostgreSQL database handling 50K queries/second. Response times were acceptable (50-100ms), but the RDS bill was $15K/month. The team had "optimized" by throwing hardware at it—db.r5.8xlarge instances with 32 vCPUs.

The problem wasn't the hardware. It was a single query pattern that ran 30K times per second:

```sql
SELECT * FROM users WHERE email = 'user@example.com'
```

No index on email. Every query was a full table scan of 10 million rows. The database was doing 300 billion row scans per second.

Added a single index:

```sql
CREATE INDEX idx_users_email ON users(email);
```

Query time dropped from 80ms to 0.5ms. CPU usage dropped 70%. Downgraded to db.r5.2xlarge (8 vCPUs). Monthly cost: $4K. Same performance, 73% less energy, $11K/month savings.

This isn't about database tuning wizardry. This is about understanding where databases waste energy and fixing it.

## Why Databases Are Energy Hogs

Your database does more work than any other part of your stack. While your application code might execute in microseconds, a single database query can take milliseconds to seconds. And unlike your application code that runs once per request, database queries often run millions of times per day.

### The Four Horsemen of Database Energy Consumption

Every database query touches four major subsystems, each with its own energy cost:

**1. Disk I/O: The Biggest Energy Drain (40-50% of total)**

Storage speed determines energy consumption:

- **SSD read**: ~100 microseconds, ~0.1 watts per operation
- **HDD read**: ~10 milliseconds, ~10 watts per operation (100x slower, 100x more energy)
- **Memory read**: ~100 nanoseconds, ~0.0001 watts per operation (1000x faster than SSD)

A full table scan on 10 million rows means ~10,000 disk operations. At 1000 queries/second, that's 100 kilowatts continuously—the power consumption of 10 homes. Tables don't fit in memory, indexes help but don't eliminate disk reads, and write operations are even more expensive due to write amplification, fsync, and journaling.

**2. CPU: The Query Processor (30-40% of total)**

Query planning overhead (parsing, validation, optimization) takes 1-2ms for simple queries, 10-50ms for complex ones. At 1000 queries/second, that's 1-50 CPU cores just on planning. Execution costs come from row filtering, joins, aggregations, sorting, and deduplication. A join between two 1 million row tables requires building a 100MB hash table and takes 100-500ms of CPU time.

**3. Memory: The Cache Layer (10-15% of total)**

The buffer pool caches frequently accessed pages (typically 50-80% of RAM). A 128GB server with a 100GB buffer pool consumes 100 watts continuously (~1 watt per GB). Working memory for sorts, joins, and temporary tables adds more—a complex query might need 170MB, and 100 concurrent queries consume 17 watts just for working memory.

**4. Network: The Data Highway (5-10% of total)**

Network interfaces consume 2-5 watts per 1 Gbps, plus switch/router overhead. Transferring 500MB of query results takes 6 seconds at 80 MB/s practical throughput, consuming 12 watt-seconds in network power plus CPU costs for serialization/deserialization. Bandwidth limits (80 MB/s practical vs 125 MB/s theoretical) create bottlenecks.

### The Multiplication Effect

The real problem isn't a single query—it's the multiplication effect.

**Example: E-commerce product search**

- Query: Search products by keyword
- Execution time: 50ms
- Queries per second: 1000 (moderate traffic)
- Queries per day: 86,400,000

**Energy calculation:**

- Disk I/O: 20ms × 0.1 watts = 2 milliwatt-seconds per query
- CPU: 25ms × 10 watts = 250 milliwatt-seconds per query
- Memory: 10ms × 0.1 watts = 1 milliwatt-second per query
- Network: 5ms × 2 watts = 10 milliwatt-seconds per query
- **Total per query**: 263 milliwatt-seconds = 0.263 watt-seconds

**Daily energy consumption:**

- 86,400,000 queries × 0.263 watt-seconds = 22,723,200 watt-seconds
- = 6,312 watt-hours = 6.3 kWh per day
- = 2,300 kWh per year
- = **$230/year in electricity** (at $0.10/kWh)
- = **920 kg CO2e per year** (at 400g CO2e/kWh)

That's for ONE query pattern. A typical application has 50-100 different query patterns. Total energy: 115-230 kWh/year, $11,500-$23,000/year, 46-92 tons CO2e/year.

### Why Inefficient Queries Are Catastrophic

An inefficient query doesn't just waste energy—it wastes it at scale.

**Scenario: Missing index on email lookup**

- Efficient query (with index): 1ms, 0.01 watt-seconds
- Inefficient query (full table scan): 100ms, 1 watt-second
- **100x more energy per query**

If this query runs 1000 times/second:

- Efficient: 10 watts continuous power
- Inefficient: 1000 watts continuous power
- **Difference: 990 watts = running 10 computers continuously**

Over a year:

- Efficient: 87.6 kWh, $8.76, 35 kg CO2e
- Inefficient: 8,760 kWh, $876, 3,504 kg CO2e
- **Difference: $867/year, 3.5 tons CO2e/year**

For a single missing index.

### The Hidden Cost: Idle Capacity

Databases are provisioned for peak load, but average utilization is often 20-40%. This means:

- 60-80% of hardware capacity sits idle
- Idle hardware still consumes 30-50% of peak power (CPUs idle, memory powered, disks spinning)
- **Embedded carbon waste**: Manufacturing emissions for hardware that's underutilized

A database server consuming 300 watts at peak might consume 100-150 watts at idle. If it runs at 30% average utilization:

- Peak power: 300 watts
- Actual power: 150 watts (30% load + 50% idle power)
- Wasted power: 60 watts (idle overhead)
- **40% of power consumption is waste**

### The Good News

Small changes have massive impact because:

1. **Queries run millions of times**: Fix one query, save millions of executions
2. **Inefficiencies compound**: One missing index affects every query that needs it
3. **Optimization is multiplicative**: Index + caching + batching = 100x-1000x improvement
4. **Right-sizing reduces waste**: Smaller instance = less idle power

A single index can save 990 watts of continuous power. Connection pooling can reduce CPU by 20%. Caching can eliminate 90% of queries. Together, these optimizations can reduce database energy consumption by 50-80%.

Let's start with the basics.

## Pattern 1: Index Strategically (Not Everything)

**Skill Level**: 🟢 Basic

### The Problem

When you query a database without an index, it performs a sequential scan—reading every single row from disk to find matches. For a 10 million row table, that's 10 million disk reads. Every time.

Disk I/O is expensive. An SSD read takes ~100 microseconds. Memory access takes ~100 nanoseconds. That's 1000x slower. When you scan 10 million rows, you're doing 10 million slow operations instead of a handful of fast ones.

But indexes aren't free. Every index:

- Consumes disk space (often 20-50% of table size)
- Slows down writes (INSERT, UPDATE, DELETE must update all indexes)
- Requires maintenance (VACUUM, REINDEX, statistics updates)
- Uses memory (buffer pool space for index pages)

The worst mistake: creating indexes on every column "just in case." I've seen databases with 20+ indexes on a single table, where only 3 were ever used. The other 17 were pure waste—slowing down every write, consuming memory, wasting disk space.

### The Solution

Index what you actually query, not what you think you might query someday.

Start by profiling. Use EXPLAIN ANALYZE (PostgreSQL), slow query log (MySQL), or explain() (MongoDB) to find sequential scans. Look for queries that scan thousands or millions of rows but return only a few.

**Composite indexes matter**. If you query `WHERE customer_id = 123 AND status = 'pending'`, create an index on both columns: `(customer_id, status)`. The order matters—put the most selective column first (the one that filters out the most rows).

**Index coverage**. Some databases (PostgreSQL, MySQL with InnoDB) can answer queries entirely from the index without touching the table. If you query `SELECT id, email FROM users WHERE email = 'user@example.com'`, an index on `(email, id)` can return the result without reading the table at all.

### How It Works

An index is a sorted data structure (usually a B-tree) that maps column values to row locations. Instead of scanning every row, the database:

1. Searches the B-tree (logarithmic time: log₂(10M) ≈ 23 comparisons)
2. Finds matching entries
3. Reads only those specific rows from disk

For a 10 million row table:

- Sequential scan: 10,000,000 disk reads
- Index scan: ~23 B-tree lookups + N row reads (where N = matching rows)

If your query returns 5 rows, that's 28 disk reads instead of 10 million. That's why the impact is so dramatic.

### Code Example

```sql
-- Before: Full table scan
SELECT * FROM orders WHERE customer_id = 123 AND status = 'pending';
-- Seq Scan on orders (cost=0.00..180000.00 rows=5000)
-- Reads all 10M rows from disk, filters in memory

-- After: Composite index
CREATE INDEX idx_orders_customer_status ON orders(customer_id, status);
-- Index Scan using idx_orders_customer_status (cost=0.43..25.50 rows=5)
-- Searches B-tree, reads only matching rows

-- Even better: Covering index (if you only need specific columns)
CREATE INDEX idx_orders_covering ON orders(customer_id, status) 
  INCLUDE (id, total, created_at);
-- Index-only scan: doesn't touch table at all
```

### Finding Missing Indexes

```sql
-- PostgreSQL: Find sequential scans
SELECT schemaname, tablename, seq_scan, seq_tup_read, 
       idx_scan, seq_tup_read / seq_scan as avg_rows_per_scan
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC
LIMIT 20;

-- Look for high seq_tup_read with low idx_scan
-- These tables need indexes
```

### Impact

- Query time: 500ms → 2ms (250x faster)
- CPU usage: -60% (less row filtering)
- Disk I/O: -95% (reading 28 rows instead of 10M)
- Memory usage: -90% (smaller working set)
- Energy savings: ~50% for read-heavy workloads

The key: profile first, index second. Don't guess. Measure.

## Pattern 2: Connection Pooling Done Right

**Skill Level**: 🟢 Basic

### The Problem

Every database connection has overhead. When your application opens a new connection:

1. **TCP handshake**: 3-way handshake (SYN, SYN-ACK, ACK) = 1-2 network round trips
2. **Authentication**: Username/password verification, SSL negotiation = 2-3 round trips
3. **Session setup**: Setting session variables, preparing statements = 1-2 round trips
4. **Memory allocation**: Connection buffers, prepared statement cache = ~10MB per connection

Total time: 50-100ms. For a query that takes 1ms, you're spending 50-100x more time on connection overhead than actual work.

Each idle connection also consumes resources:

- **Memory**: ~10MB per connection (buffers, caches, session state)
- **CPU**: Keep-alive packets, connection monitoring
- **File descriptors**: Limited resource on the database server

Most databases have connection limits (PostgreSQL default: 100, MySQL default: 151). If your application opens a new connection per request and you have 200 concurrent requests, you'll hit the limit and start queuing or failing.

But too many pooled connections is also wasteful. If you configure a pool of 100 connections but only use 10, you're wasting 900MB of memory (90 × 10MB) and CPU cycles on 90 idle connections.

### The Solution

Connection pooling: maintain a pool of open connections that are reused across requests.

**How it works:**

1. Application needs a connection → borrows from pool
2. Executes query
3. Returns connection to pool (doesn't close it)
4. Next request reuses the same connection

**Sizing the pool:**

- **Too small**: Requests queue waiting for connections (high latency)
- **Too large**: Wasted memory and CPU on idle connections
- **Rule of thumb**: Start with `pool_size = (CPU cores × 2) + effective_spindle_count`
  - For cloud databases: `pool_size = 10-20` is usually sufficient
  - Monitor connection usage and adjust

**Connection lifecycle:**

- **pool_pre_ping**: Verify connection is alive before using (prevents stale connections)
- **pool_recycle**: Close and recreate connections after N seconds (prevents long-lived connection issues)
- **max_overflow**: Allow temporary connections beyond pool_size during spikes

### How It Works

Without pooling:

```
Request 1: Open (50ms) → Query (1ms) → Close (5ms) = 56ms
Request 2: Open (50ms) → Query (1ms) → Close (5ms) = 56ms
Request 3: Open (50ms) → Query (1ms) → Close (5ms) = 56ms
Total: 168ms for 3ms of actual work
```

With pooling:

```
Request 1: Borrow (0ms) → Query (1ms) → Return (0ms) = 1ms
Request 2: Borrow (0ms) → Query (1ms) → Return (0ms) = 1ms
Request 3: Borrow (0ms) → Query (1ms) → Return (0ms) = 1ms
Total: 3ms for 3ms of actual work
```

### Code Example

```python
# Before: New connection per request
def get_user(user_id):
    conn = psycopg2.connect(DATABASE_URL)  # 50ms overhead!
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()  # 5ms overhead
    return user

# If this runs 1000 times/second:
# Connection overhead: 55ms × 1000 = 55 seconds of wasted time per second
# That's 55 CPU cores just managing connections!

# After: Connection pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,        # Keep 10 connections open
    max_overflow=20,     # Allow 20 more during spikes
    pool_pre_ping=True,  # Verify connection before use
    pool_recycle=3600    # Recycle after 1 hour
)

def get_user(user_id):
    with engine.connect() as conn:  # Borrows from pool (0ms)
        result = conn.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return result.fetchone()
    # Connection returned to pool automatically (0ms)

# If this runs 1000 times/second:
# Connection overhead: 0ms × 1000 = 0 seconds
# Actual work: 1ms × 1000 = 1 second of CPU time
```

### Monitoring Pool Health

```python
# Check pool statistics
from sqlalchemy import event

@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    print(f"Pool size: {engine.pool.size()}")
    print(f"Checked out: {engine.pool.checkedout()}")
    print(f"Overflow: {engine.pool.overflow()}")
    print(f"Checked in: {engine.pool.checkedin()}")

# If checkedout is consistently near pool_size, increase pool_size
# If checkedin is consistently high, decrease pool_size
```

### Impact

- Connection overhead: 50ms → 0ms (eliminates handshake/auth)
- Memory usage: -40% (10 connections instead of 100+ transient)
- CPU usage: -20% (no connection churn)
- Throughput: +3x (no connection bottleneck)
- Database load: -50% (fewer connection/disconnection events)

Use HikariCP (Java), SQLAlchemy (Python), pg-pool (Node.js), or database/sql (Go). All major languages have mature connection pooling libraries.

## Pattern 3: Query Result Caching

**Skill Level**: 🟡 Intermediate

### The Problem

Databases are good at executing queries, but they're not magic. Every query, even a fast one, requires:

- Parsing the SQL
- Planning the execution (choosing indexes, join order)
- Executing the plan (reading data, filtering, sorting)
- Formatting results
- Transferring over the network

For a simple query that returns the same data repeatedly, you're doing all this work over and over. If 1000 users request the same product page, you're executing the same query 1000 times.

Even with perfect indexes, a query takes time:

- Index lookup: 0.1-1ms
- Row retrieval: 0.1-1ms per row
- Network transfer: 0.1-1ms
- Total: 0.5-5ms per query

At 1000 requests/second, that's 500-5000ms of database CPU time per second. That's 0.5-5 CPU cores just serving repeated queries.

### The Solution

Cache query results. Compute once, serve many times.

**Where to cache:**

- **Application-level**: Redis, Memcached (most common)
- **Database query cache**: MySQL query cache (deprecated in 8.0), PostgreSQL shared buffers
- **CDN**: For public, rarely-changing data
- **Application memory**: For small, frequently-accessed data

**Cache invalidation strategies:**

- **Time-based (TTL)**: Cache expires after N seconds (simple, works for most cases)
- **Event-based**: Invalidate when data changes (complex, but always fresh)
- **Lazy**: Serve stale data, refresh in background (best user experience)

**What to cache:**

- User profiles (change infrequently)
- Product catalogs (change daily/hourly)
- Aggregations (expensive to compute)
- Configuration data (rarely changes)

**What NOT to cache:**

- Real-time data (stock prices, live scores)
- User-specific sensitive data (unless encrypted)
- Data that changes frequently (shopping cart, inventory)

### How It Works

Without caching:

```
Request 1: Query DB (5ms) → Return result
Request 2: Query DB (5ms) → Return result
Request 3: Query DB (5ms) → Return result
...
Request 1000: Query DB (5ms) → Return result
Total: 5000ms of database CPU time
```

With caching (90% hit rate):

```
Request 1: Query DB (5ms) → Store in cache → Return result
Request 2-10: Read from cache (0.1ms each) = 0.9ms
Request 11: Query DB (5ms) → Update cache → Return result
Request 12-20: Read from cache (0.1ms each) = 0.9ms
...
Total: 500ms DB time + 90ms cache time = 590ms total
Savings: 88% less database load
```

### Code Example

```python
import redis
import json
from functools import wraps
import hashlib

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def cache_query(ttl=300):
    """Cache query results with TTL in seconds"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            # Use hash for long keys
            key_data = f"{func.__name__}:{json.dumps(args)}:{json.dumps(kwargs)}"
            cache_key = f"query:{hashlib.md5(key_data.encode()).hexdigest()}"
        
            # Try cache first
            cached = redis_client.get(cache_key)
            if cached:
                print(f"Cache HIT: {func.__name__}")
                return json.loads(cached)
        
            print(f"Cache MISS: {func.__name__}")
            # Cache miss - query database
            result = func(*args, **kwargs)
        
            # Store in cache with TTL
            redis_client.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator

@cache_query(ttl=600)  # Cache for 10 minutes
def get_user_profile(user_id):
    """Expensive query with joins"""
    query = """
        SELECT 
            u.id, u.name, u.email, u.created_at,
            p.bio, p.avatar_url, p.location,
            COUNT(DISTINCT f.id) as follower_count,
            COUNT(DISTINCT p2.id) as post_count
        FROM users u
        JOIN profiles p ON u.id = p.user_id
        LEFT JOIN followers f ON u.id = f.following_id
        LEFT JOIN posts p2 ON u.id = p2.author_id
        WHERE u.id = %s
        GROUP BY u.id, u.name, u.email, u.created_at, p.bio, p.avatar_url, p.location
    """
    return execute_query(query, (user_id,))

# First call: Cache MISS, queries database (50ms)
profile = get_user_profile(123)

# Next 1000 calls: Cache HIT, reads from Redis (0.1ms each)
# Saves 49.9ms × 1000 = 49,900ms = 50 seconds of database time
```

### Cache Invalidation

```python
def update_user_profile(user_id, new_bio):
    """Update profile and invalidate cache"""
    # Update database
    execute_query(
        "UPDATE profiles SET bio = %s WHERE user_id = %s",
        (new_bio, user_id)
    )
  
    # Invalidate cache
    key_data = f"get_user_profile:{json.dumps([user_id])}:{json.dumps({})}"
    cache_key = f"query:{hashlib.md5(key_data.encode()).hexdigest()}"
    redis_client.delete(cache_key)
  
    # Next call will be cache miss and fetch fresh data
```

### Monitoring Cache Performance

```python
def get_cache_stats():
    """Monitor cache hit rate"""
    info = redis_client.info('stats')
    hits = info['keyspace_hits']
    misses = info['keyspace_misses']
    total = hits + misses
    hit_rate = (hits / total * 100) if total > 0 else 0
  
    return {
        'hits': hits,
        'misses': misses,
        'hit_rate': f"{hit_rate:.2f}%"
    }

# Aim for 80-95% hit rate
# If hit rate is low, increase TTL or cache more queries
# If hit rate is too high (>98%), you might be caching too aggressively
```

### Impact

- 90% cache hit rate = 90% fewer database queries
- Database CPU: -80% (only 10% of queries hit database)
- Response time: 50ms → 1ms (cache is 50x faster than database)
- Database connections: -90% (fewer concurrent queries)
- Energy savings: Proportional to cache hit rate (80-90% typical)

The tradeoff: cache invalidation is hard. Start with high TTL (5-10 minutes) for rarely-changing data. Use event-based invalidation only when necessary. Monitor staleness vs hit rate.

## Pattern 4: Batch Operations

**Skill Level**: 🟢 Basic

### The Problem

The N+1 query problem is one of the most common performance killers. It happens when you fetch a list of items, then loop through them making individual queries for related data.

Example: Loading 100 blog posts with their authors:

```python
# Fetch posts
posts = execute_query("SELECT * FROM posts LIMIT 100")

# For each post, fetch author (N+1 problem!)
for post in posts:
    author = execute_query("SELECT * FROM users WHERE id = %s", (post['author_id'],))
    post['author'] = author
```

This executes 101 queries: 1 for posts + 100 for authors. Each query has overhead:

- **Network round trip**: 0.5-2ms (even on localhost)
- **Query parsing**: 0.1-0.5ms
- **Query planning**: 0.1-1ms
- **Execution**: 0.1-1ms
- **Result formatting**: 0.1-0.5ms

Total per query: 1-5ms. For 100 queries, that's 100-500ms of overhead alone, before any actual work.

The database also has to:

- Acquire/release locks 100 times
- Update statistics 100 times
- Log 100 separate operations
- Manage 100 separate transactions

### The Solution

Batch operations: fetch or modify multiple rows in a single query.

**For reads**: Use `IN` clause or `JOIN`
**For writes**: Use multi-row `INSERT`, `UPDATE` with `VALUES`, or bulk operations

**Why batching works:**

- **Single network round trip**: 1ms instead of 100ms
- **Single query parse/plan**: 1ms instead of 100ms
- **Bulk execution**: Database can optimize (sort, batch I/O)
- **Single transaction**: Less lock contention

### How It Works

N+1 approach (bad):

```
Query 1: SELECT posts (1ms network + 1ms execution) = 2ms
Query 2: SELECT author WHERE id=1 (1ms network + 0.1ms execution) = 1.1ms
Query 3: SELECT author WHERE id=2 (1ms network + 0.1ms execution) = 1.1ms
...
Query 101: SELECT author WHERE id=100 (1ms network + 0.1ms execution) = 1.1ms
Total: 2ms + (100 × 1.1ms) = 112ms
```

Batched approach (good):

```
Query 1: SELECT posts (1ms network + 1ms execution) = 2ms
Query 2: SELECT authors WHERE id IN (1,2,...,100) (1ms network + 1ms execution) = 2ms
Total: 4ms
Savings: 96% faster (112ms → 4ms)
```

### Code Example: Batch Reads

```python
# Before: N+1 queries
def get_posts_with_authors_slow():
    # Query 1: Fetch posts
    posts = execute_query("SELECT * FROM posts LIMIT 100")
  
    # Queries 2-101: Fetch each author individually
    for post in posts:
        author = execute_query(
            "SELECT * FROM users WHERE id = %s",
            (post['author_id'],)
        )
        post['author'] = author
  
    return posts
# 101 queries, ~5 seconds

# After: Batched with IN clause
def get_posts_with_authors_fast():
    # Query 1: Fetch posts
    posts = execute_query("SELECT * FROM posts LIMIT 100")
  
    # Query 2: Fetch all authors in one query
    author_ids = [post['author_id'] for post in posts]
    authors = execute_query(
        "SELECT * FROM users WHERE id IN %s",
        (tuple(author_ids),)
    )
  
    # Build lookup map
    author_map = {author['id']: author for author in authors}
  
    # Attach authors to posts
    for post in posts:
        post['author'] = author_map.get(post['author_id'])
  
    return posts
# 2 queries, ~0.05 seconds

# Even better: Single query with JOIN
def get_posts_with_authors_best():
    return execute_query("""
        SELECT 
            p.*,
            u.id as author_id,
            u.name as author_name,
            u.email as author_email
        FROM posts p
        JOIN users u ON p.author_id = u.id
        LIMIT 100
    """)
# 1 query, ~0.02 seconds
```

### Code Example: Batch Writes

```python
# Before: N queries for updates
def update_user_scores_slow(user_scores):
    """Update scores for 1000 users"""
    for user_id, score in user_scores.items():
        execute_query(
            "UPDATE users SET score = %s WHERE id = %s",
            (score, user_id)
        )
    # 1000 queries = ~5 seconds
    # 1000 network round trips
    # 1000 transaction commits
    # 1000 index updates

# After: Single batched query
def update_user_scores_fast(user_scores):
    """Update scores for 1000 users in one query"""
    # Build VALUES clause
    values = [(user_id, score) for user_id, score in user_scores.items()]
  
    # Single query with temporary table
    query = """
        UPDATE users SET score = v.score
        FROM (VALUES %s) AS v(id, score)
        WHERE users.id = v.id
    """
    execute_values(cursor, query, values)
    # 1 query = ~0.05 seconds
    # 1 network round trip
    # 1 transaction commit
    # Bulk index update

# For inserts: Use multi-row INSERT
def insert_users_batch(users):
    """Insert 1000 users"""
    query = """
        INSERT INTO users (name, email, created_at)
        VALUES %s
    """
    values = [(u['name'], u['email'], u['created_at']) for u in users]
    execute_values(cursor, query, values)
    # 1 query instead of 1000
```

### Batch Size Considerations

Don't batch too large:

- **Network limits**: Most databases have max packet size (MySQL: 16MB default)
- **Memory limits**: Large batches consume memory on both client and server
- **Lock contention**: Very large batches hold locks longer
- **Transaction size**: Large transactions can cause replication lag

**Rule of thumb:**

- Reads: Batch up to 1000-5000 IDs in `IN` clause
- Writes: Batch 100-1000 rows per INSERT/UPDATE
- If you have 10,000 rows, split into 10 batches of 1000

```python
def batch_update(items, batch_size=1000):
    """Update items in batches"""
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        update_batch(batch)
        # Process 1000 at a time
```

### Impact

- 1000 queries → 1 query (or 10 batches of 100)
- Execution time: 5s → 0.05s (100x faster)
- Network overhead: -99% (1 round trip instead of 1000)
- Database connections: -99% (1 connection instead of 1000 concurrent)
- Lock contention: -90% (fewer, shorter locks)
- Transaction log: -99% (1 transaction instead of 1000)

This is low-hanging fruit. Find your N+1 queries (look for loops with database calls inside) and batch them. The impact is immediate and dramatic.

## Pattern 5: Avoid SELECT * (Seriously)

**Skill Level**: 🟢 Basic

### The Problem

`SELECT *` is convenient. You don't have to think about which columns you need. But convenience has a cost.

When you `SELECT *`, the database:

1. **Reads all columns from disk** (even if you only use 2 out of 50)
2. **Transfers all data over the network** (bandwidth waste)
3. **Allocates memory for all columns** (memory waste)
4. **Serializes all data** (CPU waste)

The problem compounds with large columns. A `TEXT` or `BLOB` column can be megabytes. If you have a `blog_content` column that's 5MB and you `SELECT *` for 100 blog posts, you're transferring 500MB when you might only need 100KB of metadata.

**Disk I/O impact:**

- Row-oriented databases (PostgreSQL, MySQL) store rows contiguously
- Reading a row means reading all columns
- If your row is 10KB but you only need 100 bytes, you're reading 100x more data than necessary

**Network impact:**

- Database → Application transfer is often the bottleneck
- 1 Gbps network = 125 MB/s theoretical max
- In practice: 50-80 MB/s with protocol overhead
- Transferring 500MB takes 6-10 seconds

**Memory impact:**

- Application must allocate memory for all columns
- Garbage collection pressure (especially in Java, Python)
- Cache pollution (filling caches with unused data)

### The Solution

Select only the columns you actually use.

**How to identify what you need:**

1. Look at your code—what fields do you actually access?
2. If you're returning JSON, only select fields in the JSON
3. If you're displaying a list, only select fields shown in the list

**Exceptions where SELECT * is okay:**

- Small tables (< 10 columns, < 1KB per row)
- When you genuinely need all columns
- Internal admin tools where convenience > performance

### How It Works

With `SELECT *`:

```
Row structure: id (4 bytes) + title (100 bytes) + excerpt (200 bytes) + 
               content (5MB) + author_id (4 bytes) + created_at (8 bytes)
Total per row: ~5MB

Query: SELECT * FROM blog_posts WHERE author_id = 123
Returns: 100 posts × 5MB = 500MB

Disk I/O: 500MB read from disk
Network: 500MB transferred
Memory: 500MB allocated
Time: ~10 seconds
```

With selective columns:

```
Query: SELECT id, title, excerpt, created_at FROM blog_posts WHERE author_id = 123
Returns: 100 posts × 312 bytes = 31KB

Disk I/O: 31KB read (if using covering index) or 500MB (if reading full rows)
Network: 31KB transferred
Memory: 31KB allocated
Time: ~0.01 seconds

Savings: 16,000x less data transferred
```

### Code Example

```sql
-- Before: Fetching everything
SELECT * FROM blog_posts WHERE author_id = 123;
-- Returns: id, title, excerpt, content (5MB), author_id, created_at, updated_at, 
--          slug, meta_description, featured_image, tags, status, view_count, ...
-- 100 posts × 5MB each = 500MB transferred
-- Query time: 10 seconds (mostly network transfer)

-- After: Select only needed columns
SELECT id, title, excerpt, published_at 
FROM blog_posts 
WHERE author_id = 123;
-- Returns: id, title, excerpt, published_at
-- 100 posts × 1KB each = 100KB transferred
-- Query time: 0.005 seconds
-- 5000x less data, 2000x faster

-- Even better: Covering index
CREATE INDEX idx_blog_posts_author_covering 
ON blog_posts(author_id) 
INCLUDE (id, title, excerpt, published_at);

-- Now the query can be answered entirely from the index
-- No table access needed at all
-- Query time: 0.001 seconds
```

### Real-World Example

```python
# Before: SELECT * in ORM
class BlogPost(Model):
    id = IntegerField()
    title = StringField()
    excerpt = StringField()
    content = TextField()  # 5MB average
    author_id = IntegerField()
    created_at = DateTimeField()
    # ... 20 more fields

# This fetches ALL fields
posts = BlogPost.query.filter_by(author_id=123).all()

# Renders list view (only uses id, title, excerpt)
for post in posts:
    print(f"{post.title}: {post.excerpt}")
# Transferred 500MB, used 31KB

# After: Select only needed fields
posts = BlogPost.query.filter_by(author_id=123)\
    .with_entities(BlogPost.id, BlogPost.title, BlogPost.excerpt)\
    .all()

# Or use defer() to exclude large columns
posts = BlogPost.query.filter_by(author_id=123)\
    .options(defer('content'))\
    .all()

# Transferred 31KB, used 31KB
# 16,000x improvement
```

### Finding SELECT * Queries

```sql
-- PostgreSQL: Find queries with SELECT *
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
WHERE query LIKE '%SELECT *%'
ORDER BY total_time DESC
LIMIT 20;

-- Look for high total_time queries
-- These are candidates for optimization
```

### Impact

- Network transfer: -99% (100KB instead of 500MB)
- Memory usage: -95% (only allocate what you need)
- Disk I/O: -90% (with covering indexes, -100%)
- Query time: 200ms → 5ms (40x faster)
- Bandwidth costs: -99% (especially important for cloud databases)

This is the easiest optimization. Stop using `SELECT *`. Specify columns. Your database, network, and cloud bill will thank you.

## Pattern 6: Optimize JOINs

**Skill Level**: 🟡 Intermediate

### The Problem

JOINs are powerful but expensive. The database has to match rows from multiple tables, and the cost grows with the size of the tables.

**Common JOIN problems:**

1. **Wrong JOIN order**: Database scans large table first, then filters
2. **Missing JOIN conditions**: Creates Cartesian product (every row × every row)
3. **Unnecessary JOINs**: Joining tables you don't actually need
4. **No indexes on JOIN columns**: Forces nested loop joins instead of hash/merge joins

**JOIN algorithms and their costs:**

- **Nested Loop**: O(N × M) - scans inner table for each outer row (slow for large tables)
- **Hash Join**: O(N + M) - builds hash table, then probes (fast, but needs memory)
- **Merge Join**: O(N log N + M log M) - sorts both tables, then merges (fast if already sorted)

The database query planner chooses the algorithm, but it's not always optimal. You can help by:

- Filtering early (reduce N and M)
- Adding indexes (enable merge joins)
- Reordering JOINs (start with smallest result set)

### The Solution

Filter early, JOIN late. Start with the most selective filter, then JOIN to other tables.

**Principle**: If you're filtering on `users.country = 'US'` and only 1% of users are in the US, filter users first. Then JOIN to orders. Don't JOIN all users to all orders, then filter.

### How It Works

Bad JOIN order (filter late):

```sql
SELECT o.id, o.total, u.name
FROM orders o  -- 10M rows
JOIN users u ON o.user_id = u.id  -- 10M × 1M = 10T comparisons
WHERE u.country = 'US'  -- Filters to 10K rows
  AND o.created_at > '2024-01-01';

-- Steps:
-- 1. Scan orders: 10M rows
-- 2. JOIN to users: 10M × 1M comparisons (nested loop)
-- 3. Filter: 10M rows → 10K rows
-- Result: 10K rows after processing 10M
```

Good JOIN order (filter early):

```sql
SELECT o.id, o.total, u.name
FROM users u  -- 1M rows
WHERE u.country = 'US'  -- Filters to 10K rows
JOIN orders o ON u.id = o.user_id  -- 10K × 10M comparisons
WHERE o.created_at > '2024-01-01';

-- Steps:
-- 1. Scan users with filter: 1M rows → 10K rows
-- 2. JOIN to orders: 10K × 10M comparisons (much smaller)
-- 3. Filter orders: 10K rows → 5K rows
-- Result: 5K rows after processing 10K
```

Savings: 10M rows processed → 10K rows processed (1000x reduction)

### Code Example

```sql
-- Before: Inefficient JOIN order
SELECT o.id, o.total, u.name, p.name as product_name
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
JOIN users u ON o.user_id = u.id
WHERE o.created_at > '2024-01-01'
  AND u.country = 'US';

-- Execution plan:
-- 1. Scan orders (10M rows)
-- 2. JOIN order_items (10M × 50M = 500M comparisons)
-- 3. JOIN products (500M × 1M comparisons)
-- 4. JOIN users (500M × 1M comparisons)
-- 5. Filter (500M rows → 5K rows)
-- Query time: 30 seconds

-- After: Filter early, JOIN late
SELECT o.id, o.total, u.name, p.name as product_name
FROM users u
WHERE u.country = 'US'  -- Filter first: 1M → 10K rows
JOIN orders o ON u.id = o.user_id
  AND o.created_at > '2024-01-01'  -- Filter during JOIN
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id;

-- Execution plan:
-- 1. Scan users with filter (1M → 10K rows)
-- 2. JOIN orders with filter (10K × 10M, but indexed)
-- 3. JOIN order_items (5K × 50M, but indexed)
-- 4. JOIN products (10K × 1M, but indexed)
-- Query time: 0.1 seconds
-- 300x faster

-- Even better: Use indexes and covering indexes
CREATE INDEX idx_users_country ON users(country);
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_products_id ON products(id);

-- Now all JOINs use index lookups instead of scans
-- Query time: 0.01 seconds
```

### Avoiding Cartesian Products

```sql
-- WRONG: Missing JOIN condition
SELECT u.name, o.total
FROM users u, orders o
WHERE u.country = 'US';
-- Creates Cartesian product: every user × every order
-- 10K users × 10M orders = 100B rows!
-- Query never finishes

-- RIGHT: Explicit JOIN condition
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.country = 'US';
-- Only matches related rows
-- 10K users with their orders = 50K rows
```

### Eliminating Unnecessary JOINs

```sql
-- Before: JOIN to table you don't need
SELECT o.id, o.total, o.created_at
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.created_at > '2024-01-01';
-- JOINs to users but doesn't use any user columns!

-- After: Remove unnecessary JOIN
SELECT o.id, o.total, o.created_at
FROM orders o
WHERE o.created_at > '2024-01-01';
-- 10x faster (no JOIN overhead)
```

### Using EXPLAIN to Understand JOINs

```sql
-- PostgreSQL: See execution plan
EXPLAIN ANALYZE
SELECT o.id, o.total, u.name
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.country = 'US';

-- Look for:
-- - "Seq Scan" (bad) vs "Index Scan" (good)
-- - "Nested Loop" (slow for large tables) vs "Hash Join" (faster)
-- - Rows estimate vs actual rows (if way off, run ANALYZE)
-- - Execution time breakdown by node
```

### Impact

- Rows processed: 10M → 100K (100x reduction)
- Query time: 5s → 0.1s (50x faster)
- CPU usage: -95% (less row processing)
- Memory usage: -90% (smaller intermediate results)
- Disk I/O: -95% (fewer rows read)

Use EXPLAIN ANALYZE to see what the database is actually doing. Reorder JOINs to filter early. Add indexes on JOIN columns. Remove unnecessary JOINs.

## Pattern 7: Pagination Done Right

**Skill Level**: 🟡 Intermediate

### The Problem

OFFSET pagination seems simple: `LIMIT 10 OFFSET 1000000` to get page 100,001. But it's a trap.

**How OFFSET works:**

1. Database scans rows from the beginning
2. Skips the first 1,000,000 rows
3. Returns the next 10 rows

The database does all the work of scanning 1,000,010 rows, but only returns 10. The other 1,000,000 rows are scanned and discarded.

**The cost grows linearly with page depth:**

- Page 1 (OFFSET 0): Scan 10 rows
- Page 100 (OFFSET 1000): Scan 1,010 rows
- Page 10,000 (OFFSET 100000): Scan 100,010 rows
- Page 100,000 (OFFSET 1000000): Scan 1,000,010 rows

For deep pagination, you're scanning millions of rows just to throw them away. This wastes:

- **CPU**: Processing rows you don't need
- **Disk I/O**: Reading rows you don't need
- **Memory**: Buffering rows you don't need
- **Time**: Linear growth with page depth

**Real-world impact:**

- Page 1: 10ms
- Page 100: 100ms
- Page 1,000: 1s
- Page 10,000: 10s
- Page 100,000: 100s (query timeout!)

### The Solution

Cursor-based pagination (also called keyset pagination): use the last seen value as a filter.

**How it works:**

1. Order by a unique, indexed column (id, created_at)
2. Remember the last value from the previous page
3. Use `WHERE column > last_value` to get the next page

**Benefits:**

- Constant time regardless of page depth
- No rows scanned and discarded
- Works with indexes efficiently
- Scales to millions of pages

**Tradeoff:**

- Can't jump to arbitrary pages (no "go to page 5000")
- Need to track cursor state
- Perfect for infinite scroll, "next page" navigation
- Not suitable for traditional page numbers (1, 2, 3, ...)

### How It Works

OFFSET pagination (bad):

```sql
-- Page 1
SELECT * FROM posts ORDER BY created_at DESC LIMIT 10 OFFSET 0;
-- Scans 10 rows, returns 10

-- Page 100,000
SELECT * FROM posts ORDER BY created_at DESC LIMIT 10 OFFSET 1000000;
-- Scans 1,000,010 rows, returns 10
-- 99.999% of work is wasted
```

Cursor pagination (good):

```sql
-- Page 1
SELECT * FROM posts ORDER BY created_at DESC LIMIT 10;
-- Returns posts with created_at: 2024-01-15 10:30:00 (last)

-- Page 2 (use last seen timestamp as cursor)
SELECT * FROM posts 
WHERE created_at < '2024-01-15 10:30:00'
ORDER BY created_at DESC 
LIMIT 10;
-- Scans 10 rows, returns 10

-- Page 100,000 (still fast!)
SELECT * FROM posts 
WHERE created_at < '2023-06-20 14:22:15'  -- Last seen from page 99,999
ORDER BY created_at DESC 
LIMIT 10;
-- Scans 10 rows, returns 10
-- Constant time regardless of page depth
```

### Code Example

```python
# Before: OFFSET pagination
def get_posts_offset(page=1, page_size=10):
    offset = (page - 1) * page_size
    query = """
        SELECT * FROM posts 
        ORDER BY created_at DESC 
        LIMIT %s OFFSET %s
    """
    return execute_query(query, (page_size, offset))

# Page 1: Fast (10ms)
posts = get_posts_offset(page=1)

# Page 100,000: Slow (100 seconds!)
posts = get_posts_offset(page=100000)
# Scans 1,000,010 rows, returns 10

# After: Cursor-based pagination
def get_posts_cursor(cursor=None, page_size=10):
    if cursor is None:
        # First page
        query = """
            SELECT * FROM posts 
            ORDER BY created_at DESC 
            LIMIT %s
        """
        posts = execute_query(query, (page_size,))
    else:
        # Subsequent pages
        query = """
            SELECT * FROM posts 
            WHERE created_at < %s
            ORDER BY created_at DESC 
            LIMIT %s
        """
        posts = execute_query(query, (cursor, page_size))
  
    # Return posts and cursor for next page
    next_cursor = posts[-1]['created_at'] if posts else None
    return {
        'posts': posts,
        'next_cursor': next_cursor,
        'has_more': len(posts) == page_size
    }

# Page 1: Fast (10ms)
result = get_posts_cursor()
posts = result['posts']
next_cursor = result['next_cursor']

# Page 100,000: Still fast (10ms!)
result = get_posts_cursor(cursor=next_cursor)
# Scans 10 rows, returns 10
# Constant time
```

### Handling Ties (Non-Unique Sort Columns)

```python
# Problem: If created_at has duplicates, cursor pagination can skip rows
# Solution: Use composite cursor with unique column

def get_posts_cursor_safe(cursor_time=None, cursor_id=None, page_size=10):
    if cursor_time is None:
        # First page
        query = """
            SELECT * FROM posts 
            ORDER BY created_at DESC, id DESC 
            LIMIT %s
        """
        posts = execute_query(query, (page_size,))
    else:
        # Subsequent pages: Use both created_at and id
        query = """
            SELECT * FROM posts 
            WHERE (created_at, id) < (%s, %s)
            ORDER BY created_at DESC, id DESC 
            LIMIT %s
        """
        posts = execute_query(query, (cursor_time, cursor_id, page_size))
  
    # Return composite cursor
    if posts:
        last_post = posts[-1]
        next_cursor = {
            'time': last_post['created_at'],
            'id': last_post['id']
        }
    else:
        next_cursor = None
  
    return {
        'posts': posts,
        'next_cursor': next_cursor,
        'has_more': len(posts) == page_size
    }

# Requires composite index
CREATE INDEX idx_posts_created_id ON posts(created_at DESC, id DESC);
```

### API Design for Cursor Pagination

```python
# REST API with cursor
@app.route('/api/posts')
def get_posts():
    cursor = request.args.get('cursor')
    page_size = int(request.args.get('page_size', 10))
  
    result = get_posts_cursor(cursor, page_size)
  
    return {
        'data': result['posts'],
        'pagination': {
            'next_cursor': result['next_cursor'],
            'has_more': result['has_more']
        }
    }

# Client usage:
# GET /api/posts?page_size=10
# Returns: { data: [...], pagination: { next_cursor: "2024-01-15T10:30:00Z", has_more: true } }

# GET /api/posts?page_size=10&cursor=2024-01-15T10:30:00Z
# Returns next page
```

### When to Use Each Approach

**Use OFFSET pagination when:**

- Small datasets (< 10,000 rows)
- Need to jump to arbitrary pages
- Traditional UI with page numbers (1, 2, 3, ...)
- Users rarely go beyond page 10

**Use cursor pagination when:**

- Large datasets (> 10,000 rows)
- Infinite scroll UI
- "Load more" / "Next page" navigation
- Users might paginate deep
- Performance is critical

### Impact

- Deep pagination: 5s → 0.01s (500x faster)
- Rows scanned: 1M → 10 (100,000x reduction)
- CPU usage: -99.999% (no wasted scanning)
- Disk I/O: -99.999% (only read needed rows)
- Consistent performance regardless of page depth

Cursor pagination is essential for large datasets. If you have millions of rows and users paginate deep, OFFSET will kill your database. Switch to cursors.

## Pattern 8: Aggregate in the Database

**Skill Level**: 🟡 Intermediate

### The Problem

Fetching all rows to your application and aggregating in code is wasteful. You're:

- **Transferring massive datasets** over the network
- **Using application memory** to hold all rows
- **Using application CPU** to compute aggregations
- **Doing work the database is optimized for**

Databases are designed for aggregations. They have:

- **Optimized algorithms**: Streaming aggregations, hash aggregations
- **Index support**: Can use indexes for GROUP BY
- **Parallel execution**: Can use multiple cores
- **Minimal data transfer**: Return only the aggregated result

When you fetch 10,000 rows to compute a SUM, you're transferring 5MB of data to return a single number. That's 5,000,000x more data than necessary.

### The Solution

Use database aggregation functions: SUM, COUNT, AVG, MIN, MAX, GROUP BY.

**Common aggregations:**

- **COUNT**: Number of rows
- **SUM**: Total of a column
- **AVG**: Average of a column
- **MIN/MAX**: Minimum/maximum value
- **GROUP BY**: Aggregate by category
- **HAVING**: Filter aggregated results

**Why it's faster:**

- Database processes data where it lives (no network transfer)
- Database can use indexes (covering indexes for COUNT, partial indexes)
- Database can stream results (doesn't need to hold all rows in memory)
- Database returns only the result (single row instead of 10,000 rows)

### How It Works

Aggregate in application (bad):

```python
# Fetch all orders
orders = execute_query("SELECT total FROM orders WHERE user_id = %s", (user_id,))
# Transfers 10,000 rows × 500 bytes = 5MB

# Compute in application
total_spent = sum(order['total'] for order in orders)
order_count = len(orders)
avg_order = total_spent / order_count if order_count > 0 else 0

# Used 5MB network, 5MB memory, application CPU
# Returned 3 numbers
```

Aggregate in database (good):

```sql
-- Compute in database
SELECT 
    SUM(total) as total_spent,
    COUNT(*) as order_count,
    AVG(total) as avg_order
FROM orders 
WHERE user_id = %s

-- Transfers 1 row × 100 bytes = 100 bytes
-- Used 100 bytes network, 100 bytes memory, database CPU
-- Returned 3 numbers
-- 50,000x less data transferred
```

### Code Example

```python
# Before: Aggregate in application
def get_order_stats_slow(user_id):
    # Fetch all orders
    orders = execute_query(
        "SELECT total, created_at FROM orders WHERE user_id = %s",
        (user_id,)
    )  # Fetches 10,000 orders = 5MB
  
    # Compute aggregations in Python
    total_spent = sum(order['total'] for order in orders)
    order_count = len(orders)
    avg_order = total_spent / order_count if order_count > 0 else 0
  
    # Compute by year
    by_year = {}
    for order in orders:
        year = order['created_at'].year
        if year not in by_year:
            by_year[year] = {'count': 0, 'total': 0}
        by_year[year]['count'] += 1
        by_year[year]['total'] += order['total']
  
    return {
        'total_spent': total_spent,
        'order_count': order_count,
        'avg_order': avg_order,
        'by_year': by_year
    }
# Query time: 500ms (mostly network transfer)
# Network: 5MB
# Memory: 5MB

# After: Aggregate in database
def get_order_stats_fast(user_id):
    # Single query with aggregations
    result = execute_query("""
        SELECT 
            SUM(total) as total_spent,
            COUNT(*) as order_count,
            AVG(total) as avg_order,
            EXTRACT(YEAR FROM created_at) as year,
            COUNT(*) as year_count,
            SUM(total) as year_total
        FROM orders 
        WHERE user_id = %s
        GROUP BY EXTRACT(YEAR FROM created_at)
    """, (user_id,))
  
    # Format results
    by_year = {
        row['year']: {
            'count': row['year_count'],
            'total': row['year_total']
        }
        for row in result
    }
  
    # Overall stats from first row
    first = result[0] if result else {}
  
    return {
        'total_spent': first.get('total_spent', 0),
        'order_count': first.get('order_count', 0),
        'avg_order': first.get('avg_order', 0),
        'by_year': by_year
    }
# Query time: 5ms
# Network: 100 bytes (10 years × 10 bytes)
# Memory: 100 bytes
# 100x faster, 50,000x less data
```

### Advanced Aggregations

```sql
-- Multiple aggregations in one query
SELECT 
    COUNT(*) as total_orders,
    COUNT(DISTINCT user_id) as unique_customers,
    SUM(total) as revenue,
    AVG(total) as avg_order_value,
    MIN(total) as min_order,
    MAX(total) as max_order,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total) as median_order,
    STDDEV(total) as stddev_order
FROM orders
WHERE created_at > NOW() - INTERVAL '30 days';

-- Returns 1 row with 8 aggregated values
-- Instead of fetching 100,000 orders and computing in application

-- Aggregation with filtering (HAVING)
SELECT 
    product_id,
    COUNT(*) as order_count,
    SUM(quantity) as total_sold,
    SUM(quantity * price) as revenue
FROM order_items
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY product_id
HAVING COUNT(*) > 100  -- Only products with > 100 orders
ORDER BY revenue DESC
LIMIT 10;

-- Returns top 10 products by revenue
-- Filters and sorts in database
-- Application receives only 10 rows
```

### Window Functions for Running Aggregations

```sql
-- Running total by date
SELECT 
    DATE(created_at) as date,
    SUM(total) as daily_revenue,
    SUM(SUM(total)) OVER (ORDER BY DATE(created_at)) as running_total
FROM orders
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY date;

-- Returns 30 rows (one per day) with running total
-- Instead of fetching all orders and computing running total in application

-- Rank products by revenue
SELECT 
    product_id,
    SUM(quantity * price) as revenue,
    RANK() OVER (ORDER BY SUM(quantity * price) DESC) as rank
FROM order_items
GROUP BY product_id
ORDER BY rank
LIMIT 10;

-- Returns top 10 products with their rank
-- Ranking computed in database
```

### Using Indexes for Aggregations

```sql
-- COUNT(*) can use index
CREATE INDEX idx_orders_user_id ON orders(user_id);

SELECT COUNT(*) FROM orders WHERE user_id = 123;
-- Uses index-only scan (doesn't touch table)
-- Very fast

-- Covering index for aggregations
CREATE INDEX idx_orders_user_total ON orders(user_id) INCLUDE (total);

SELECT SUM(total) FROM orders WHERE user_id = 123;
-- Uses covering index (doesn't touch table)
-- Reads only index pages
```

### Impact

- Data transferred: 10,000 rows → 1 row (10,000x reduction)
- Network: 5MB → 100 bytes (50,000x reduction)
- Processing time: 500ms → 5ms (100x faster)
- Memory usage: -99% (application doesn't hold all rows)
- CPU usage: -90% (database CPU is optimized for aggregations)

Let the database do what it's good at. Aggregations, GROUP BY, window functions—these are core database operations. Don't fetch data to aggregate in your application.
    MAX(total) as max_order,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total) as median_order,
    STDDEV(total) as stddev_order
FROM orders
WHERE created_at > NOW() - INTERVAL '30 days';

-- Returns 1 row with 8 aggregated values
-- Instead of fetching 100,000 orders and computing in application

-- Aggregation with filtering (HAVING)
SELECT
    product_id,
    COUNT(*) as order_count,
    SUM(quantity) as total_sold,
    SUM(quantity * price) as revenue
FROM order_items
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY product_id
HAVING COUNT(*) > 100  -- Only products with > 100 orders
ORDER BY revenue DESC
LIMIT 10;

-- Returns top 10 products by revenue
-- Filters and sorts in database
-- Application receives only 10 rows

```

### Window Functions for Running Aggregations

```sql
-- Running total by date
SELECT 
    DATE(created_at) as date,
    SUM(total) as daily_revenue,
    SUM(SUM(total)) OVER (ORDER BY DATE(created_at)) as running_total
FROM orders
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY date;

-- Returns 30 rows (one per day) with running total
-- Instead of fetching all orders and computing running total in application

-- Rank products by revenue
SELECT 
    product_id,
    SUM(quantity * price) as revenue,
    RANK() OVER (ORDER BY SUM(quantity * price) DESC) as rank
FROM order_items
GROUP BY product_id
ORDER BY rank
LIMIT 10;

-- Returns top 10 products with their rank
-- Ranking computed in database
```

### Using Indexes for Aggregations

```sql
-- Create covering index for common aggregation
CREATE INDEX idx_orders_user_total ON orders(user_id) INCLUDE (total, created_at);

-- This query can use index-only scan
SELECT 
    user_id,
    COUNT(*) as order_count,
    SUM(total) as total_spent
FROM orders
WHERE user_id IN (1, 2, 3, 4, 5)
GROUP BY user_id;

-- Database reads only the index, doesn't touch the table
-- Much faster for large tables
```

### Impact

- Data transferred: 10,000 rows → 1 row (10,000x reduction)
- Network: 5MB → 100 bytes (50,000x reduction)
- Processing time: 500ms → 5ms (100x faster)
- Memory usage: -99.998% (100 bytes vs 5MB)
- CPU: Database CPU (optimized) vs application CPU (unoptimized)
- Energy savings: Proportional to data reduction (99%+)

Always aggregate in the database. It's faster, uses less energy, and that's what databases are designed for.

## Pattern 9: Materialized Views for Complex Queries

**Skill Level**: 🔴 Advanced

### The Problem

Some queries are expensive no matter how well you optimize them:

- Complex joins across 5+ tables
- Aggregations over millions of rows
- Recursive queries (hierarchies, graphs)
- Queries that run frequently but results change infrequently

Example: Dashboard showing product sales by category for the last 30 days. The query:

- Joins products, categories, order_items, orders
- Aggregates millions of order_items
- Groups by category
- Takes 5 seconds to execute

If 1000 users view the dashboard per day, that's 5000 seconds (83 minutes) of database CPU time. For data that changes every few minutes.

### The Solution

Materialized views: pre-compute expensive queries and store the results.

**How it works:**

1. Create a materialized view (like a table, but defined by a query)
2. Database executes the query once and stores the result
3. Queries against the view are instant (just reading stored data)
4. Refresh the view periodically (hourly, daily, on-demand)

**When to use:**

- Query is expensive (> 1 second)
- Query runs frequently (> 100 times/day)
- Data changes infrequently (hourly, daily)
- Staleness is acceptable (dashboard data can be 5 minutes old)

**Refresh strategies:**

- **Scheduled**: Refresh every N minutes/hours (cron job, scheduled task)
- **On-demand**: Refresh when data changes (trigger, application code)
- **Incremental**: Update only changed rows (PostgreSQL REFRESH MATERIALIZED VIEW CONCURRENTLY)

### How It Works

Without materialized view:

```
User 1: Execute expensive query (5s)
User 2: Execute expensive query (5s)
User 3: Execute expensive query (5s)
...
User 1000: Execute expensive query (5s)
Total: 5000 seconds of database CPU time
```

With materialized view:

```
Background job: Execute query once (5s) → Store result
User 1: Read from materialized view (0.001s)
User 2: Read from materialized view (0.001s)
User 3: Read from materialized view (0.001s)
...
User 1000: Read from materialized view (0.001s)
Total: 5s + 1s = 6 seconds of database CPU time
Savings: 99.88% (5000s → 6s)
```

### Code Example

```sql
-- Complex query that runs 1000x/day
SELECT 
    c.name as category,
    COUNT(DISTINCT p.id) as product_count,
    AVG(p.price) as avg_price,
    SUM(oi.quantity) as total_sold,
    SUM(oi.quantity * oi.price) as revenue
FROM categories c
JOIN products p ON c.id = p.category_id
LEFT JOIN order_items oi ON p.id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.id
WHERE o.created_at > NOW() - INTERVAL '30 days'
GROUP BY c.id, c.name
ORDER BY revenue DESC;
-- Takes 5 seconds each time

-- Create materialized view
CREATE MATERIALIZED VIEW product_category_stats AS
SELECT 
    c.id as category_id,
    c.name as category,
    COUNT(DISTINCT p.id) as product_count,
    AVG(p.price) as avg_price,
    SUM(oi.quantity) as total_sold,
    SUM(oi.quantity * oi.price) as revenue,
    NOW() as last_updated
FROM categories c
JOIN products p ON c.id = p.category_id
LEFT JOIN order_items oi ON p.id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.id
WHERE o.created_at > NOW() - INTERVAL '30 days'
GROUP BY c.id, c.name;

-- Create index on materialized view
CREATE INDEX idx_category_stats_revenue ON product_category_stats(revenue DESC);

-- Query the view (instant)
SELECT * FROM product_category_stats 
WHERE category = 'Electronics'
ORDER BY revenue DESC;
-- Takes 0.001 seconds

-- Refresh the view (scheduled job, runs every hour)
REFRESH MATERIALIZED VIEW product_category_stats;
-- Takes 5 seconds, but only runs once per hour
```

### Refresh Strategies

```python
# Scheduled refresh (every hour)
import schedule
import time

def refresh_materialized_views():
    execute_query("REFRESH MATERIALIZED VIEW product_category_stats")
    execute_query("REFRESH MATERIALIZED VIEW user_activity_summary")
    print(f"Refreshed materialized views at {datetime.now()}")

# Run every hour
schedule.every().hour.at(":00").do(refresh_materialized_views)

while True:
    schedule.run_pending()
    time.sleep(60)

# Or use cron (Linux/Mac)
# 0 * * * * psql -d mydb -c "REFRESH MATERIALIZED VIEW product_category_stats"

# Or use pg_cron (PostgreSQL extension)
SELECT cron.schedule('refresh-stats', '0 * * * *', 
    'REFRESH MATERIALIZED VIEW product_category_stats');
```

### Concurrent Refresh (PostgreSQL)

```sql
-- Regular refresh: Locks the view (blocks reads)
REFRESH MATERIALIZED VIEW product_category_stats;
-- View is unavailable during refresh (5 seconds)

-- Concurrent refresh: Doesn't lock the view
REFRESH MATERIALIZED VIEW CONCURRENTLY product_category_stats;
-- View remains available during refresh
-- Requires unique index on the view

-- Create unique index for concurrent refresh
CREATE UNIQUE INDEX idx_category_stats_id ON product_category_stats(category_id);

-- Now concurrent refresh works
REFRESH MATERIALIZED VIEW CONCURRENTLY product_category_stats;
```

### Incremental Refresh (Manual)

```sql
-- Instead of recomputing everything, update only changed data
-- Track last refresh time
CREATE TABLE materialized_view_refresh_log (
    view_name TEXT PRIMARY KEY,
    last_refresh TIMESTAMP
);

-- Incremental refresh logic
WITH new_data AS (
    SELECT 
        c.id as category_id,
        c.name as category,
        COUNT(DISTINCT p.id) as product_count,
        SUM(oi.quantity) as total_sold,
        SUM(oi.quantity * oi.price) as revenue
    FROM categories c
    JOIN products p ON c.id = p.category_id
    LEFT JOIN order_items oi ON p.id = oi.product_id
    LEFT JOIN orders o ON oi.order_id = o.id
    WHERE o.created_at > (
        SELECT last_refresh FROM materialized_view_refresh_log 
        WHERE view_name = 'product_category_stats'
    )
    GROUP BY c.id, c.name
)
UPDATE product_category_stats
SET 
    product_count = product_count + new_data.product_count,
    total_sold = total_sold + new_data.total_sold,
    revenue = revenue + new_data.revenue
FROM new_data
WHERE product_category_stats.category_id = new_data.category_id;

-- Update refresh log
UPDATE materialized_view_refresh_log 
SET last_refresh = NOW() 
WHERE view_name = 'product_category_stats';
```

### When NOT to Use Materialized Views

- Data changes frequently (every second)
- Staleness is unacceptable (real-time requirements)
- Query is already fast (< 100ms)
- Storage is limited (materialized views consume disk space)
- Refresh time is too long (> 10 minutes)

### Impact

- Query time: 5s → 0.001s (5000x faster)
- Database load: 1000 expensive queries/day → 24 refresh operations/day
- CPU usage: -99.5% (5000s → 24s per day)
- Energy savings: Massive (compute once, read many times)
- Tradeoff: Staleness (data can be up to refresh interval old)

Materialized views are perfect for dashboards, reports, and analytics. If your query is expensive and runs frequently, materialize it.

## Pattern 10: Choosing the Right Database for the Job

**Skill Level**: 🔴 Advanced (Architecture Decision)

### The Problem

Using a relational database for everything is like using a hammer for every job. Sometimes you need a screwdriver.

The wrong database doesn't just perform poorly—it wastes massive amounts of energy:

- **Graph queries in PostgreSQL**: 100-1000x more CPU than Neo4j
- **Time-series in MySQL**: 30x more storage and CPU than TimescaleDB
- **Document storage in normalized tables**: 5x more queries and joins than MongoDB
- **Simple key-value lookups in RDBMS**: 100x more overhead than Redis

When you use the wrong database, you compensate with more hardware. That means:

- **More servers** = More manufacturing emissions (embedded carbon)
- **More CPU cycles** = More operational energy
- **More storage** = More disk manufacturing and power
- **Worse performance** = Frustrated users and wasted resources

### The Solution

Match database type to data access patterns. Different databases are optimized for different workloads.

**Database Types and Their Sweet Spots**:

**Relational (PostgreSQL, MySQL)**:

- **Best for**: Structured data with relationships, ACID transactions, complex queries
- **Energy profile**: Moderate CPU, high disk I/O for joins
- **Use when**: Data has clear relationships, need strong consistency
- **Examples**: User accounts, orders, inventory, financial transactions

**Document (MongoDB, CouchDB)**:

- **Best for**: Semi-structured data, flexible schemas, nested documents
- **Energy profile**: Lower CPU (no joins), moderate disk I/O
- **Use when**: Data is document-centric, schema evolves frequently
- **Examples**: Product catalogs, user profiles, content management, configuration

**Key-Value (Redis, DynamoDB)**:

- **Best for**: Simple lookups, caching, session storage
- **Energy profile**: Very low CPU, minimal disk I/O (often in-memory)
- **Use when**: Need fast lookups, data is simple key-value pairs
- **Examples**: Session storage, rate limiting, real-time leaderboards, caching

**Graph (Neo4j, Amazon Neptune)**:

- **Best for**: Highly connected data, relationship queries, traversals
- **Energy profile**: High CPU for traversals, but efficient for graph queries
- **Use when**: Relationships are first-class citizens, need path finding
- **Examples**: Social networks, recommendation engines, fraud detection, knowledge graphs

**Time-Series (InfluxDB, TimescaleDB)**:

- **Best for**: Time-stamped data, metrics, IoT data
- **Energy profile**: Optimized for time-range queries, efficient compression
- **Use when**: Data is time-ordered, need aggregations over time windows
- **Examples**: Metrics, logs, sensor data, financial data, monitoring

### How It Works

Wrong database = inefficient queries = more hardware = more energy:

```python
# Wrong: Graph query in PostgreSQL
# Finding friends-of-friends (2 degrees of separation)
query = """
    WITH RECURSIVE friend_network AS (
        SELECT user_id, friend_id, 1 as depth
        FROM friendships
        WHERE user_id = %s
        UNION
        SELECT f.user_id, f.friend_id, fn.depth + 1
        FROM friendships f
        JOIN friend_network fn ON f.user_id = fn.friend_id
        WHERE fn.depth < 2
    )
    SELECT DISTINCT friend_id FROM friend_network;
"""
# Query time: 5 seconds
# Scans millions of rows
# Multiple self-joins
# Recursive CTE overhead
# CPU: 100% for 5 seconds

# Right: Same query in Neo4j
query = """
    MATCH (user:User {id: $userId})-[:FRIENDS_WITH*1..2]-(friend)
    RETURN DISTINCT friend.id
"""
# Query time: 0.05 seconds (100x faster)
# Native graph traversal
# Follows relationship pointers
# CPU: 10% for 0.05 seconds
# 95% less energy
```

### Code Examples

```python
# Wrong: Time-series data in PostgreSQL
# Storing 1 billion metrics over 7 days
# Query: Average CPU usage per hour

query = """
    SELECT 
        DATE_TRUNC('hour', timestamp) as hour,
        AVG(cpu_usage) as avg_cpu,
        MAX(memory_usage) as max_memory
    FROM metrics
    WHERE timestamp > NOW() - INTERVAL '7 days'
    GROUP BY hour
    ORDER BY hour;
"""
# Storage: 1B rows × 100 bytes = 100 GB uncompressed
# Query: Full table scan, 1B rows, 30 seconds
# Hardware needed: db.r5.4xlarge (16 vCPU, 128 GB RAM)
# Power: 200W
# Energy per query: 200W × 30s = 1.67 watt-hours

# Right: Same data in TimescaleDB (time-series optimized)
query = """
    SELECT 
        time_bucket('1 hour', timestamp) as hour,
        AVG(cpu_usage) as avg_cpu,
        MAX(memory_usage) as max_memory
    FROM metrics
    WHERE timestamp > NOW() - INTERVAL '7 days'
    GROUP BY hour
    ORDER BY hour;
"""
# Storage: 1B rows × 20 bytes compressed = 20 GB (5x less)
# Query: Time-based partition scan, 0.1 seconds (300x faster)
# Hardware needed: db.r5.xlarge (4 vCPU, 32 GB RAM) - 4x smaller
# Power: 50W
# Energy per query: 50W × 0.1s = 0.0014 watt-hours
# 99% less energy per query
```

### Decision Matrix

| Data Pattern               | Best Database         | Why                                  | Energy Impact                        |
| -------------------------- | --------------------- | ------------------------------------ | ------------------------------------ |
| Structured, relational     | PostgreSQL, MySQL     | ACID, complex queries                | Baseline                             |
| Documents, flexible schema | MongoDB               | No joins, nested data                | 2-5x less CPU                        |
| Simple key-value           | Redis, DynamoDB       | Fast lookups, low overhead           | 10-100x less CPU                     |
| Highly connected           | Neo4j, Neptune        | Native graph traversal               | 100-1000x less CPU for graph queries |
| Time-series                | InfluxDB, TimescaleDB | Time-based optimization, compression | 10-30x less storage and CPU          |
| Full-text search           | Elasticsearch         | Inverted indexes                     | 10-100x faster search                |
| Analytics, OLAP            | ClickHouse, BigQuery  | Column-oriented, compression         | 10-100x less I/O                     |

### Polyglot Persistence

Using multiple databases for different workloads:

```python
# Monolithic approach: Everything in PostgreSQL
# - User accounts: PostgreSQL (good fit) ✓
# - Session data: PostgreSQL (bad fit - Redis 100x faster) ✗
# - Product catalog: PostgreSQL (bad fit - MongoDB more flexible) ✗
# - Recommendations: PostgreSQL (bad fit - Neo4j 100x faster) ✗
# - Metrics: PostgreSQL (bad fit - InfluxDB 30x more efficient) ✗

# Total hardware: 5x db.r5.4xlarge instances (80 vCPU, 640 GB RAM)
# Total power: 1,000W
# Total embedded carbon: 10,000 kg CO2e (server manufacturing)

# Polyglot approach: Right database for each workload
# - User accounts: PostgreSQL db.r5.large (2 vCPU, 16 GB) ✓
# - Session data: Redis cache.r5.large (2 vCPU, 13 GB) ✓
# - Product catalog: MongoDB db.r5.large (2 vCPU, 16 GB) ✓
# - Recommendations: Neo4j db.r5.large (2 vCPU, 16 GB) ✓
# - Metrics: InfluxDB db.r5.large (2 vCPU, 16 GB) ✓

# Total hardware: 5x db.r5.large instances (10 vCPU, 77 GB RAM)
# Total power: 250W (75% reduction)
# Total embedded carbon: 2,500 kg CO2e (75% reduction)
# Performance: 10-100x better for specialized workloads
```

### Energy and Embedded Carbon Considerations

**The Wrong Database = Wasted Resources**:

Using PostgreSQL for time-series data:

- **Storage**: 10x more disk space (no time-series compression)
- **Query CPU**: 30x more CPU cycles (full table scans vs time-based partitions)
- **Memory**: 5x more RAM (inefficient caching)
- **Hardware**: 4x larger instances to compensate
- **Embedded carbon waste**: Manufacturing emissions for oversized hardware

Using PostgreSQL for graph queries:

- **Query CPU**: 100-1000x more CPU (recursive CTEs vs native graph traversal)
- **Response time**: 10-100x slower (multiple JOINs vs single graph query)
- **Scaling**: Requires 10x more hardware to achieve same throughput
- **Embedded carbon**: Manufacturing emissions for 10x more servers

**Energy Calculation Example**:

```python
# Scenario: 1 billion time-series data points, 7-day retention
# Query: Average CPU usage per hour for last 7 days
# Queries: 1000/day

# Wrong: PostgreSQL (general-purpose RDBMS)
# Storage: 1B rows × 100 bytes = 100 GB uncompressed
# Query: Full table scan, 1B rows, 30 seconds
# Hardware: db.r5.4xlarge (16 vCPU, 128 GB RAM)
# Power: 200W
# Energy: 200W × 30s × 1000 queries / 3600 = 1.67 kWh/day
# Annual energy: 609 kWh/year
# Annual cost: $61/year (at $0.10/kWh)
# Embedded carbon: 2,000 kg CO2e (server manufacturing, amortized over 4 years = 500 kg/year)
# Total carbon: 500 kg (embedded) + 244 kg (operational at 400g/kWh) = 744 kg CO2e/year

# Right: TimescaleDB (time-series optimized)
# Storage: 1B rows × 20 bytes compressed = 20 GB (5x less)
# Query: Time-based partition scan, 0.1 seconds (300x faster)
# Hardware: db.r5.xlarge (4 vCPU, 32 GB RAM) - 4x smaller
# Power: 50W
# Energy: 50W × 0.1s × 1000 queries / 3600 = 0.014 kWh/day
# Annual energy: 5 kWh/year (99% reduction)
# Annual cost: $0.50/year
# Embedded carbon: 500 kg CO2e (4x smaller server, amortized = 125 kg/year)
# Total carbon: 125 kg (embedded) + 2 kg (operational) = 127 kg CO2e/year

# Total savings:
# - Operational energy: 604 kWh/year (99% reduction)
# - Embedded carbon: 375 kg CO2e/year (75% reduction)
# - Total carbon: 617 kg CO2e/year (83% reduction)
# - Hardware cost: 75% reduction
# - Query performance: 300x faster
```

### The Embedded Carbon Tradeoff

**Operational complexity** (managing multiple databases) vs **resource efficiency** (right tool for the job):

**More databases** = More operational overhead:

- Monitoring multiple systems
- Backup and recovery for each
- Security updates and patching
- Different query languages and tools
- Team training and expertise

**Right databases** = Less hardware, less energy, less embedded carbon:

- Smaller instances (less manufacturing emissions)
- Better performance (less CPU waste)
- Efficient storage (less disk manufacturing)
- Lower operational energy (optimized for workload)

**Sweet spot**: 2-4 specialized databases for distinct workload types

### Decision Framework

1. **Identify workload types**: Transactional, caching, documents, graphs, time-series, analytics
2. **Calculate resource requirements**: CPU, memory, storage for each database type
3. **Compare total resource footprint**: Monolithic vs polyglot
4. **Factor in operational complexity**: Can your team manage multiple databases?
5. **Choose**: If resource savings > 50% and team can manage, use polyglot persistence

### Impact

- Right database for workload: 10-100x performance improvement
- Energy savings: 50-95% for specialized workloads
- Embedded carbon savings: 50-75% (smaller hardware footprint)
- Storage savings: 5-10x (compression and optimization)
- Operational complexity: +20-50% (multiple systems to manage)
- Tradeoff: Complexity vs efficiency (usually worth it for large systems)

Choose the right database for the job. The energy savings and performance improvements far outweigh the operational complexity.

## Pattern 11: Cloud vs On-Premises Databases

**Skill Level**: 🟡 Intermediate (Infrastructure Decision)

### The Problem

Cloud databases and on-premises databases have different energy profiles. The wrong choice wastes energy and money.

**Cloud overhead**:

- Virtualization: 10-20% performance penalty
- Network latency: Not on same physical hardware as application
- Multi-tenancy: Noisy neighbor problem

**On-premises waste**:

- Idle capacity: Provisioned for peak, runs at 20-40% average utilization
- Fixed location: Can't move to low-carbon regions
- Embedded carbon: Manufacturing emissions locked into underutilized hardware

### The Solution

Understand the energy and embedded carbon tradeoffs. Choose based on workload patterns.

**Cloud Databases (RDS, Aurora, Azure SQL, Cloud SQL)**:

**Advantages**:

- **Auto-scaling**: Right-size automatically, scale to zero when idle
- **Pay for what you use**: No idle hardware costs
- **Geographic distribution**: Place data near users, choose low-carbon regions
- **Shared infrastructure**: Cloud provider achieves 60-80% utilization across fleet
- **No embedded carbon waste**: Hardware amortized across many customers

**Disadvantages**:

- **Virtualization overhead**: 10-20% performance penalty
- **Network latency**: Database not on same physical hardware as application
- **Multi-tenancy**: Noisy neighbor problem (other tenants affect performance)
- **Vendor lock-in**: Harder to migrate

**Energy Profile**:

- Better for variable workloads (scale to zero when idle)
- Worse for consistent high-load (virtualization overhead)
- Can choose low-carbon regions (huge impact: 10-30x difference in grid carbon intensity)

**On-Premises Databases**:

**Advantages**:

- **No virtualization overhead**: Bare metal performance
- **No network latency**: Same data center as application
- **Full control**: Hardware, configuration, security
- **Predictable costs**: For steady workloads

**Disadvantages**:

- **Upfront hardware costs**: Capital expenditure
- **Idle capacity waste**: Can't scale to zero, runs 24/7
- **Operational overhead**: Patching, backups, monitoring, hardware replacement
- **Fixed location**: Can't move to low-carbon regions
- **Embedded carbon locked in**: Manufacturing emissions for underutilized hardware

**Energy Profile**:

- Better for consistent high-load (no virtualization overhead)
- Worse for variable workloads (idle capacity waste)
- Stuck with local grid carbon intensity

### The Embedded Carbon Problem

Manufacturing a server generates significant carbon emissions before it's even powered on:

- **Server manufacturing**: ~1,000-3,000 kg CO2e per server
- **Expected lifetime**: 3-5 years
- **Amortized embedded carbon**: ~200-1,000 kg CO2e per year

If your on-prem database server runs at 30% average utilization:

- **Wasted embedded carbon**: 70% of manufacturing emissions
- **Equivalent to**: Running the server for 2+ years with zero workload

Cloud providers achieve 60-80% utilization across their fleet by:

- **Multi-tenancy**: Multiple customers share same hardware
- **Workload diversity**: Different usage patterns balance out (some peak at night, others during day)
- **Auto-scaling**: Consolidate workloads on fewer servers

### Energy Calculation Example

```python
# On-Prem: Fixed capacity, low utilization
# Hardware: 2x database servers (active + standby for HA)
# Utilization: 30% average (provisioned for peak)
# Power: 300W per server
# Embedded carbon: 2,000 kg CO2e per server (manufacturing)

# Operational carbon (per year):
operational = 2 servers × 300W × 8760 hours × 400 gCO2e/kWh / 1000
operational = 2,102 kg CO2e/year

# Embedded carbon (amortized over 4 years):
embedded = 2 servers × 2,000 kg CO2e / 4 years
embedded = 1,000 kg CO2e/year

# Total carbon: 3,102 kg CO2e/year
# Wasted capacity: 70% idle = 2,171 kg CO2e/year wasted
# Cost: $5,256/year (operational energy at $0.10/kWh)

# Cloud: Auto-scaling, high utilization
# Same workload, but cloud provider achieves 70% utilization across fleet
# Shares hardware with other tenants
# Power: 300W per server (but shared)

# Your share of operational carbon:
operational = 300W × 8760 hours × 30% utilization × 400 gCO2e/kWh / 1000
operational = 315 kg CO2e/year

# Your share of embedded carbon (cloud provider amortizes across tenants):
embedded = 2,000 kg CO2e / 4 years × 30% utilization
embedded = 150 kg CO2e/year

# Total carbon: 465 kg CO2e/year
# Savings: 85% less carbon (3,102 → 465 kg CO2e/year)
# Cost: $788/year (operational energy)
# Savings: $4,468/year (85% reduction)
```

### Code Examples

```python
# Cloud: Auto-scaling based on load
# AWS RDS Aurora Serverless v2
{
    "MinCapacity": 0.5,  # Scale down to 0.5 ACU when idle
    "MaxCapacity": 16,   # Scale up to 16 ACU under load
    "AutoPause": True,   # Pause when no connections
    "SecondsUntilAutoPause": 300  # Pause after 5 minutes idle
}
# Energy savings: 70-90% for variable workloads
# Scales to near-zero during off-hours (nights, weekends)
# Embedded carbon: Shared across many customers

# On-prem: Fixed capacity
# Always running at provisioned capacity
# 24/7 operation even if only used 8 hours/day (business hours)
# Energy waste: 67% (16 hours idle / 24 hours total)
# Embedded carbon: Locked into dedicated hardware
```

### Decision Matrix

| Workload Pattern            | Best Choice                  | Why                           |
| --------------------------- | ---------------------------- | ----------------------------- |
| Variable load (dev/test)    | Cloud                        | Auto-scaling, scale to zero   |
| Consistent high load (24/7) | On-prem or cloud             | Calculate TCO and energy      |
| Development/test            | Cloud                        | Scale to zero when not in use |
| Production with spikes      | Cloud                        | Auto-scaling handles peaks    |
| Multi-region                | Cloud                        | Easy geographic distribution  |
| Latency-sensitive           | On-prem or cloud same-region | Minimize network hops         |
| Low-carbon priority         | Cloud                        | Choose low-carbon regions     |
| Predictable steady load     | On-prem                      | No virtualization overhead    |

### Hybrid Approach

Best of both worlds:

- **Production databases**: On-prem (consistent load, bare metal performance)
- **Dev/test databases**: Cloud (scale to zero when not in use)
- **Analytics databases**: Cloud (variable load, can use spot instances)
- **Disaster recovery**: Cloud (pay only when needed)

### Impact

- Cloud for variable workloads: 70-90% energy savings (auto-scaling)
- On-prem for consistent load: 10-20% better performance (no virtualization)
- Cloud in low-carbon regions: 10-30x lower carbon emissions (grid carbon intensity varies by region)
- Embedded carbon savings: 50-85% (cloud multi-tenancy vs on-prem idle capacity)
- Hybrid approach: Optimize for each workload type

The cloud vs on-prem decision isn't just about cost—it's about energy efficiency and embedded carbon. For variable workloads, cloud wins. For consistent high-load, calculate the tradeoffs.

## Pattern 12: Serverless vs Provisioned Databases

**Skill Level**: 🟡 Intermediate (Architecture Decision)

### The Problem

Provisioned databases run 24/7, even when idle. You pay for capacity you don't use.

Serverless databases scale to zero, but have cold start overhead. First query after idle period takes 1-30 seconds.

Wrong choice = paying for idle capacity OR suffering cold start latency.

### The Solution

Match database model to usage patterns.

**Provisioned Databases (RDS, Aurora Provisioned, Azure SQL)**:

**Characteristics**:

- Always running (24/7)
- Fixed capacity (or manual scaling)
- Predictable performance
- No cold starts
- Pay per hour (even when idle)

**Energy Profile**:

- Idle power consumption: 30-50% of peak (CPUs idle, memory powered, disks spinning)
- Good for: Consistent load, 24/7 applications
- Bad for: Variable load, idle periods

**Serverless Databases (Aurora Serverless, Azure SQL Serverless, Cosmos DB)**:

**Characteristics**:

- Auto-scales based on load
- Scales to zero when idle
- Pay per request (not per hour)
- Cold start latency (1-30 seconds after idle)
- Auto-pause after idle period (5-10 minutes)

**Energy Profile**:

- Zero power consumption when paused
- Good for: Variable load, dev/test, sporadic traffic
- Bad for: Latency-sensitive, high-frequency operations

### How It Works

Provisioned (always running):

```
Hour 1: 100% load, 100W power
Hour 2: 50% load, 75W power (50% idle overhead)
Hour 3: 10% load, 40W power (75% idle overhead)
Hour 4: 0% load, 30W power (100% idle overhead)
...
Hour 24: 0% load, 30W power
Average: 50W continuous power
Daily energy: 1.2 kWh
```

Serverless (scales to zero):

```
Hour 1: 100% load, 100W power
Hour 2: 50% load, 50W power
Hour 3: 10% load, 10W power
Hour 4: 0% load, auto-pause after 5 min → 0W power
...
Hour 24: 0% load, 0W power
Average: 15W (only when active)
Daily energy: 0.36 kWh (70% reduction)
```

### Code Examples

```python
# Provisioned: Always running
# AWS RDS PostgreSQL db.t3.medium
# Cost: $0.068/hour × 24 hours × 30 days = $49/month
# Energy: 50W × 24 hours × 30 days = 36 kWh/month
# Idle time: 16 hours/day (67% of time)
# Wasted energy: 24 kWh/month (67% waste)

# Serverless: Scales to zero
# AWS Aurora Serverless v2
# Cost: $0.12 per ACU-hour (only when active)
# Active: 8 hours/day × 2 ACU = 16 ACU-hours/day
# Cost: 16 × $0.12 × 30 = $58/month (slightly higher per-hour, but only 8 hours/day)
# Energy: 50W × 8 hours × 30 days = 12 kWh/month
# Idle time: 16 hours/day → auto-pause → 0W
# Wasted energy: 0 kWh/month (0% waste)
# Energy savings: 67% (36 kWh → 12 kWh)
```

### Cold Start Mitigation

```python
# Problem: Cold start takes 10-30 seconds
# First query after idle period is slow

# Solution 1: Keep-alive ping for critical applications
import schedule
import time

def keep_alive_ping():
    """Ping database every 4 minutes to prevent auto-pause"""
    execute_query("SELECT 1")

# Run every 4 minutes (before 5-minute auto-pause threshold)
schedule.every(4).minutes.do(keep_alive_ping)

while True:
    schedule.run_pending()
    time.sleep(60)

# Tradeoff: Prevents cold starts, but reduces energy savings
# Database never pauses, but still scales down capacity

# Solution 2: Accept cold start for non-critical workloads
# Development, testing, batch jobs can tolerate 10-30 second cold start
# Energy savings: 70-90%
```

### Decision Matrix

| Usage Pattern     | Best Choice | Why                                     |
| ----------------- | ----------- | --------------------------------------- |
| 24/7 production   | Provisioned | No cold starts, predictable performance |
| Development/test  | Serverless  | Scale to zero, save costs and energy    |
| Infrequent access | Serverless  | Pay only when used                      |
| Batch jobs        | Serverless  | Pay only when running                   |
| Sporadic traffic  | Serverless  | Auto-scale, efficient                   |
| High throughput   | Provisioned | No scaling delays                       |
| Cost-sensitive    | Serverless  | Pay per use                             |
| Latency-sensitive | Provisioned | No cold starts                          |

### Hybrid Approach

- **Production**: Provisioned (consistent load, no cold starts)
- **Staging**: Serverless with keep-alive (balance cost and availability)
- **Development**: Serverless (scale to zero when not in use)
- **Analytics**: Serverless (run queries on-demand)

### Energy and Embedded Carbon Considerations

**Provisioned Databases - The Idle Capacity Problem**:

Provisioned databases waste energy during idle periods:

- **Idle power**: 30-50% of peak power (CPUs idle, memory powered, disks spinning)
- **Typical utilization**: 20-40% average (provisioned for peak)
- **Wasted energy**: 60-80% of capacity sits idle

Example: Database provisioned for peak load (1000 requests/second), but average load is 200 requests/second:

- **Peak capacity**: 100W
- **Average load**: 20W (20% utilization)
- **Idle overhead**: 30W (30% of peak)
- **Total power**: 50W (20W active + 30W idle)
- **Wasted power**: 30W (60% waste)

**Embedded carbon waste**:

- Server manufactured for peak capacity
- Manufacturing emissions: 2,000 kg CO2e
- Amortized over 4 years: 500 kg CO2e/year
- Utilization: 20%
- **Wasted embedded carbon**: 400 kg CO2e/year (80% of manufacturing emissions wasted)

**Serverless Databases - Efficient Resource Utilization**:

Serverless databases scale to zero, eliminating idle capacity waste:

- **Pay per use**: Only consume resources when actively processing
- **Auto-pause**: Zero power consumption when idle
- **Shared infrastructure**: Cloud provider amortizes hardware across many customers
- **No embedded carbon waste**: Manufacturing emissions shared across many workloads

Example: Same workload on serverless:

- **Active time**: 8 hours/day (33% of time)
- **Active power**: 20W (when processing)
- **Idle power**: 0W (auto-paused)
- **Average power**: 6.7W (20W × 33%)
- **Energy savings**: 87% (50W → 6.7W)

**Embedded carbon efficiency**:

- Shared hardware across many customers
- Cloud provider achieves 70% utilization
- Your share of embedded carbon: 500 kg × 20% utilization = 100 kg CO2e/year
- **Embedded carbon savings**: 80% (400 kg → 100 kg)

### The Cold Start Tradeoff

Cold starts add latency but eliminate idle capacity waste:

- **Cold start penalty**: 1-30 seconds (one-time cost per wake-up)
- **Idle capacity elimination**: 70-90% energy savings for variable workloads
- **Embedded carbon savings**: No wasted manufacturing emissions

**When cold starts are acceptable**:

- Development and testing (latency not critical)
- Batch processing (scheduled jobs, not latency-sensitive)
- Infrequent access (admin panels, reporting)
- Background processing (async jobs, queues)

**When cold starts are problematic**:

- User-facing APIs (latency-sensitive)
- Real-time applications (sub-second response requirements)
- High-frequency operations (cold start overhead adds up)

### Mitigation Strategy - Selective Keep-Alive

```python
# Production: Keep-alive ping every 4 minutes
# - Prevents auto-pause (no cold starts)
# - Maintains 100% availability
# - Trades some energy savings for performance
# - Still scales down capacity (not full idle waste)
# - Energy savings: 40-60% (vs 70-90% with full auto-pause)

# Development: Full auto-pause
# - Scales to zero after 5 minutes idle
# - Accepts cold start penalty (10-30 seconds)
# - Maximizes energy and cost savings
# - 76% reduction in operational energy (8 hours active / 24 hours total × 30% idle overhead)
```

### Impact

- Serverless for variable workloads: 70-90% energy savings
- Serverless for dev/test: 70-90% cost reduction
- Embedded carbon waste elimination: 80% (no idle capacity)
- Provisioned for production: Predictable performance, no cold starts
- Keep-alive for critical serverless: 40-60% energy savings (balance performance and efficiency)
- Hybrid approach: 50-60% total carbon reduction across database fleet

The serverless vs provisioned decision is about matching database behavior to workload patterns. For variable workloads, serverless wins on energy and cost. For consistent load, provisioned wins on predictability.

## Real-World Case Study: E-Commerce Platform Optimization

**Company**: Mid-sized e-commerce platform
**Scale**: 50K requests/second, 10M products, 100M orders
**Problem**: $15K/month RDS bill, slow queries, frequent timeouts

### Initial State

**Infrastructure**:

- 3x PostgreSQL db.r5.8xlarge (32 vCPU, 256 GB RAM each)
- No connection pooling (new connection per request)
- No query result caching
- No indexes on frequently queried columns
- SELECT * everywhere
- N+1 queries in product listing pages

**Performance**:

- Average query time: 80ms
- P95 query time: 500ms
- Database CPU: 85% average
- Frequent connection limit errors
- Slow product search (3-5 seconds)

**Energy Profile**:

- Power consumption: 600W (3 × 200W)
- Annual energy: 5,256 kWh
- Annual carbon: 2,102 kg CO2e (at 400g/kWh)
- Monthly cost: $15,000

### Optimization Journey

**Phase 1: Low-Hanging Fruit (Week 1)**

1. **Added missing indexes** (Pattern 1)

   - Email lookups: Added index on users(email)
   - Product search: Added index on products(name, category)
   - Order queries: Added composite index on orders(user_id, status, created_at)
   - Result: Query time 80ms → 5ms (16x faster)
2. **Implemented connection pooling** (Pattern 2)

   - Configured SQLAlchemy pool: size=20, max_overflow=40
   - Result: Eliminated connection errors, CPU -20%
3. **Stopped using SELECT *** (Pattern 5)

   - Product listings: SELECT id, name, price, image_url (was fetching 50 columns including 5MB descriptions)
   - Result: Network transfer -95%, query time -60%

**Phase 1 Results**:

- Query time: 80ms → 5ms (16x faster)
- CPU usage: 85% → 50% (41% reduction)
- Downgraded: 3x db.r5.8xlarge → 3x db.r5.4xlarge (16 vCPU each)
- Monthly cost: $15,000 → $7,500 (50% reduction)
- Energy: 600W → 300W (50% reduction)

**Phase 2: Caching and Batching (Week 2)**

4. **Implemented Redis caching** (Pattern 3)

   - Product catalog: 10-minute TTL
   - User profiles: 5-minute TTL
   - Category listings: 30-minute TTL
   - Result: 85% cache hit rate, database queries -85%
5. **Fixed N+1 queries** (Pattern 4)

   - Product listings with reviews: 101 queries → 2 queries
   - Order history with items: 1001 queries → 2 queries
   - Result: Page load time 3s → 0.2s (15x faster)

**Phase 2 Results**:

- Database queries: -85% (cache hit rate)
- CPU usage: 50% → 15% (70% reduction from Phase 1)
- Downgraded: 3x db.r5.4xlarge → 2x db.r5.2xlarge (8 vCPU each)
- Monthly cost: $7,500 → $4,000 (73% reduction from initial)
- Energy: 300W → 100W (83% reduction from initial)

**Phase 3: Advanced Optimizations (Week 3-4)**

6. **Materialized views for analytics** (Pattern 9)

   - Sales dashboard: 5s query → 0.001s (5000x faster)
   - Product performance reports: Refresh hourly instead of computing on-demand
   - Result: Analytics queries -99% CPU
7. **Cursor-based pagination** (Pattern 7)

   - Product browsing: Deep pagination 5s → 0.01s (500x faster)
   - Order history: Consistent performance regardless of page depth
8. **Database aggregations** (Pattern 8)

   - Order statistics: Moved from application to database
   - Result: Data transfer 5MB → 100 bytes (50,000x reduction)

**Phase 3 Results**:

- CPU usage: 15% → 10% (88% reduction from initial)
- Maintained: 2x db.r5.2xlarge (sufficient capacity)
- Monthly cost: $4,000 (stable)
- Energy: 100W (stable)

### Final State

**Infrastructure**:

- 2x PostgreSQL db.r5.2xlarge (8 vCPU, 64 GB RAM each)
- Connection pooling (pool_size=20)
- Redis caching (85% hit rate)
- Proper indexes on all frequently queried columns
- Cursor-based pagination
- Materialized views for analytics
- Database aggregations

**Performance**:

- Average query time: 5ms (16x faster)
- P95 query time: 20ms (25x faster)
- Database CPU: 10% average (88% reduction)
- No connection errors
- Product search: 0.2s (15-25x faster)

**Energy Profile**:

- Power consumption: 100W (83% reduction)
- Annual energy: 876 kWh (83% reduction)
- Annual carbon: 350 kg CO2e (83% reduction)
- Monthly cost: $4,000 (73% reduction)

### Savings Summary

| Metric             | Before             | After          | Improvement     |
| ------------------ | ------------------ | -------------- | --------------- |
| Monthly cost       | $15,000 | $4,000   | 73% reduction  |                 |
| Annual cost        | $180,000 | $48,000 | $132,000 saved |                 |
| Power consumption  | 600W               | 100W           | 83% reduction   |
| Annual energy      | 5,256 kWh          | 876 kWh        | 4,380 kWh saved |
| Annual carbon      | 2,102 kg CO2e      | 350 kg CO2e    | 1,752 kg saved  |
| Average query time | 80ms               | 5ms            | 16x faster      |
| P95 query time     | 500ms              | 20ms           | 25x faster      |
| Database CPU       | 85%                | 10%            | 88% reduction   |

**ROI**: $132,000/year savings, 4 weeks of engineering time

### Key Lessons

1. **Start with the basics**: Indexes, connection pooling, and avoiding SELECT * gave 50% savings in week 1
2. **Measure everything**: Used EXPLAIN ANALYZE to find slow queries, pg_stat_user_tables to find missing indexes
3. **Caching is powerful**: 85% cache hit rate eliminated 85% of database queries
4. **Fix N+1 queries**: Single biggest performance improvement (3s → 0.2s page loads)
5. **Right-size infrastructure**: Started with 3x db.r5.8xlarge, ended with 2x db.r5.2xlarge (87% less hardware)
6. **Energy follows performance**: Faster queries = less CPU = less energy

The optimizations paid for themselves in the first month and continue saving $132,000/year.

## The Tradeoffs

Database optimization isn't free. Every pattern has tradeoffs. Here's what you're trading:

### Indexes

**Gain**: 10-1000x faster queries, 50-95% less disk I/O
**Cost**: Slower writes (INSERT, UPDATE, DELETE must update indexes), more storage (20-50% of table size), maintenance overhead (VACUUM, REINDEX)
**When to accept**: Read-heavy workloads (10:1 read:write ratio or higher)
**When to avoid**: Write-heavy workloads, very small tables (< 1000 rows)

### Connection Pooling

**Gain**: Eliminates connection overhead (50ms → 0ms), 20-40% less CPU, 3x throughput
**Cost**: Complexity (pool configuration, monitoring), potential connection leaks (if not properly returned)
**When to accept**: Always (benefits far outweigh costs)
**When to avoid**: Never (always use connection pooling)

### Caching

**Gain**: 80-95% fewer database queries, 50x faster response times
**Cost**: Staleness (data can be out of date), cache invalidation complexity, additional infrastructure (Redis, Memcached)
**When to accept**: Data changes infrequently (minutes to hours), staleness is acceptable
**When to avoid**: Real-time requirements, frequently changing data, sensitive data

### Batching

**Gain**: 100-1000x fewer queries, 99% less network overhead
**Cost**: Complexity (batch size tuning, error handling), potential for large transactions
**When to accept**: Always for N+1 queries (benefits far outweigh costs)
**When to avoid**: Never (always batch when possible)

### Avoiding SELECT *

**Gain**: 90-99% less data transfer, 50-90% faster queries
**Cost**: More verbose queries (must list columns), potential for missing columns
**When to accept**: Always (benefits far outweigh costs)
**When to avoid**: Never (always select only needed columns)

### Materialized Views

**Gain**: 1000-10000x faster queries, 99% less CPU for complex aggregations
**Cost**: Staleness (data can be out of date), refresh overhead, additional storage
**When to accept**: Complex queries that run frequently, staleness is acceptable (minutes to hours)
**When to avoid**: Real-time requirements, frequently changing data, limited storage

### Cursor Pagination

**Gain**: 100-1000x faster deep pagination, consistent performance
**Cost**: Can't jump to arbitrary pages, more complex API
**When to accept**: Large datasets, infinite scroll UI, deep pagination
**When to avoid**: Small datasets (< 10,000 rows), need page numbers (1, 2, 3...)

### Right Database Choice

**Gain**: 10-100x better performance, 50-95% less energy for specialized workloads
**Cost**: Operational complexity (multiple databases to manage), team training
**When to accept**: Large systems with distinct workload types, resource savings > 50%
**When to avoid**: Small systems, team can't manage multiple databases

### Cloud vs On-Premises

**Gain (Cloud)**: 70-90% energy savings for variable workloads, auto-scaling, low-carbon regions
**Cost (Cloud)**: 10-20% performance penalty (virtualization), vendor lock-in
**Gain (On-Prem)**: 10-20% better performance (bare metal), full control
**Cost (On-Prem)**: 60-80% idle capacity waste, embedded carbon waste
**When to accept**: Cloud for variable workloads, on-prem for consistent high-load

### Serverless vs Provisioned

**Gain (Serverless)**: 70-90% energy savings for variable workloads, scale to zero
**Cost (Serverless)**: Cold start latency (1-30 seconds), slightly higher per-hour cost
**Gain (Provisioned)**: No cold starts, predictable performance
**Cost (Provisioned)**: 60-80% idle capacity waste, pay for unused capacity
**When to accept**: Serverless for dev/test and variable workloads, provisioned for production 24/7

### General Principles

1. **Start with low-hanging fruit**: Indexes, connection pooling, avoiding SELECT * have minimal tradeoffs
2. **Measure before optimizing**: Don't guess, use EXPLAIN ANALYZE and monitoring
3. **Accept staleness when possible**: Caching and materialized views save massive energy
4. **Batch everything**: N+1 queries are never acceptable
5. **Right-size infrastructure**: Don't over-provision, use auto-scaling
6. **Choose the right database**: Polyglot persistence is worth the operational complexity for large systems

The tradeoffs are almost always worth it. The energy savings, cost savings, and performance improvements far outweigh the complexity.

## Measuring Impact

You can't optimize what you don't measure. Here's how to measure database energy consumption and optimization impact.

### What to Measure

**Query Performance**:

- Query execution time (EXPLAIN ANALYZE)
- Rows scanned vs rows returned
- Index usage (pg_stat_user_indexes)
- Sequential scans (pg_stat_user_tables)
- Cache hit rate (pg_stat_database)

**Resource Utilization**:

- CPU usage (CloudWatch, Datadog, New Relic)
- Memory usage (buffer pool, working memory)
- Disk I/O (read/write IOPS, throughput)
- Network transfer (bytes in/out)
- Connection count (active, idle)

**Energy Metrics**:

- Power consumption (watts)
- Energy consumption (kWh)
- Carbon emissions (kg CO2e)
- Cost ($/month)

### Tools and Techniques

**PostgreSQL**:

```sql
-- Find slow queries
SELECT 
    query,
    calls,
    total_exec_time,
    mean_exec_time,
    max_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- Find missing indexes (sequential scans)
SELECT 
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read,
    idx_scan,
    seq_tup_read / NULLIF(seq_scan, 0) as avg_rows_per_scan
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC
LIMIT 20;

-- Check cache hit rate
SELECT 
    sum(heap_blks_read) as heap_read,
    sum(heap_blks_hit) as heap_hit,
    sum(heap_blks_hit) / NULLIF(sum(heap_blks_hit) + sum(heap_blks_read), 0) * 100 as cache_hit_rate
FROM pg_statio_user_tables;
-- Aim for > 99% cache hit rate

-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
-- Look for indexes with idx_scan = 0 (unused indexes)
```

**MySQL**:

```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;  -- Log queries > 1 second

-- Check InnoDB buffer pool hit rate
SHOW STATUS LIKE 'Innodb_buffer_pool%';
-- Calculate: (Innodb_buffer_pool_read_requests - Innodb_buffer_pool_reads) / Innodb_buffer_pool_read_requests
-- Aim for > 99%

-- Check table statistics
SELECT 
    TABLE_SCHEMA,
    TABLE_NAME,
    TABLE_ROWS,
    DATA_LENGTH,
    INDEX_LENGTH
FROM information_schema.TABLES
WHERE TABLE_SCHEMA NOT IN ('information_schema', 'mysql', 'performance_schema')
ORDER BY DATA_LENGTH + INDEX_LENGTH DESC;
```

**Cloud Monitoring**:

```python
# AWS CloudWatch metrics
import boto3

cloudwatch = boto3.client('cloudwatch')

# Get database CPU utilization
response = cloudwatch.get_metric_statistics(
    Namespace='AWS/RDS',
    MetricName='CPUUtilization',
    Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': 'my-database'}],
    StartTime=datetime.now() - timedelta(hours=24),
    EndTime=datetime.now(),
    Period=3600,  # 1 hour
    Statistics=['Average', 'Maximum']
)

# Get database connections
response = cloudwatch.get_metric_statistics(
    Namespace='AWS/RDS',
    MetricName='DatabaseConnections',
    Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': 'my-database'}],
    StartTime=datetime.now() - timedelta(hours=24),
    EndTime=datetime.now(),
    Period=3600,
    Statistics=['Average', 'Maximum']
)
```

### Energy Calculation

```python
# Calculate database energy consumption

# 1. Get CPU utilization (from monitoring)
cpu_utilization = 0.45  # 45% average

# 2. Get instance specifications
instance_type = "db.r5.2xlarge"
vcpus = 8
tdp_per_cpu = 15  # Watts (typical for AWS instances)
total_tdp = vcpus * tdp_per_cpu  # 120W

# 3. Calculate power consumption
# Power = TDP × CPU_utilization × PUE
# PUE (Power Usage Effectiveness) = 1.2 for modern data centers
pue = 1.2
power_consumption = total_tdp * cpu_utilization * pue
# 120W × 0.45 × 1.2 = 64.8W

# 4. Calculate energy consumption
hours_per_month = 730
energy_per_month = power_consumption * hours_per_month / 1000  # kWh
# 64.8W × 730 hours / 1000 = 47.3 kWh/month

# 5. Calculate carbon emissions
grid_carbon_intensity = 400  # gCO2e/kWh (varies by region)
carbon_per_month = energy_per_month * grid_carbon_intensity / 1000  # kg CO2e
# 47.3 kWh × 400 gCO2e/kWh / 1000 = 18.9 kg CO2e/month

# 6. Calculate cost
electricity_cost = 0.10  # $/kWh
cost_per_month = energy_per_month * electricity_cost
# 47.3 kWh × $0.10 = $4.73/month (operational energy cost)

print(f"Power consumption: {power_consumption:.1f}W")
print(f"Energy per month: {energy_per_month:.1f} kWh")
print(f"Carbon per month: {carbon_per_month:.1f} kg CO2e")
print(f"Cost per month: ${cost_per_month:.2f}")
```

### Before/After Comparison

```python
# Before optimization
before = {
    'instance': 'db.r5.8xlarge',
    'vcpus': 32,
    'cpu_utilization': 0.85,
    'power': 32 * 15 * 0.85 * 1.2,  # 489.6W
    'energy_per_month': 489.6 * 730 / 1000,  # 357.4 kWh
    'carbon_per_month': 357.4 * 400 / 1000,  # 142.9 kg CO2e
    'cost_per_month': 15000  # AWS RDS cost
}

# After optimization
after = {
    'instance': 'db.r5.2xlarge',
    'vcpus': 8,
    'cpu_utilization': 0.10,
    'power': 8 * 15 * 0.10 * 1.2,  # 14.4W
    'energy_per_month': 14.4 * 730 / 1000,  # 10.5 kWh
    'carbon_per_month': 10.5 * 400 / 1000,  # 4.2 kg CO2e
    'cost_per_month': 4000  # AWS RDS cost
}

# Calculate savings
savings = {
    'power': before['power'] - after['power'],  # 475.2W (97% reduction)
    'energy': before['energy_per_month'] - after['energy_per_month'],  # 346.9 kWh (97% reduction)
    'carbon': before['carbon_per_month'] - after['carbon_per_month'],  # 138.7 kg CO2e (97% reduction)
    'cost': before['cost_per_month'] - after['cost_per_month']  # $11,000 (73% reduction)
}

print(f"Power savings: {savings['power']:.1f}W ({savings['power']/before['power']*100:.0f}%)")
print(f"Energy savings: {savings['energy']:.1f} kWh/month ({savings['energy']/before['energy_per_month']*100:.0f}%)")
print(f"Carbon savings: {savings['carbon']:.1f} kg CO2e/month ({savings['carbon']/before['carbon_per_month']*100:.0f}%)")
print(f"Cost savings: ${savings['cost']:,}/month ({savings['cost']/before['cost_per_month']*100:.0f}%)")
```

### Continuous Monitoring

Set up alerts for:

- CPU utilization > 80% (need to scale up or optimize)
- Cache hit rate < 95% (need more memory or better caching)
- Slow queries > 1 second (need indexes or optimization)
- Connection count > 80% of max (need connection pooling or scale up)
- Disk I/O > 80% of provisioned IOPS (need faster storage or optimization)

Measure weekly, optimize monthly, report quarterly. Energy savings compound over time.

## What's Next?

You've optimized your database. What's next in your green coding journey?

### Immediate Next Steps

1. **Implement the basics** (Week 1):

   - Add missing indexes (use EXPLAIN ANALYZE to find sequential scans)
   - Set up connection pooling (SQLAlchemy, HikariCP, pg-pool)
   - Stop using SELECT * (select only needed columns)
   - Measure baseline (CPU, memory, query times, cost)
2. **Add caching** (Week 2):

   - Set up Redis or Memcached
   - Cache frequently accessed data (user profiles, product catalogs)
   - Start with high TTL (10-30 minutes), tune based on staleness tolerance
   - Monitor cache hit rate (aim for 80-95%)
3. **Fix N+1 queries** (Week 3):

   - Find loops with database calls inside
   - Batch with IN clause or JOIN
   - Use ORM eager loading (select_related, prefetch_related)
   - Measure impact (page load times, database queries)
4. **Right-size infrastructure** (Week 4):

   - Review CPU utilization (if < 40%, downgrade instance)
   - Consider serverless for dev/test (scale to zero)
   - Use auto-scaling for variable workloads
   - Calculate savings (cost, energy, carbon)

### Advanced Optimizations

5. **Materialized views** (Month 2):

   - Identify expensive queries that run frequently
   - Create materialized views with refresh strategy
   - Monitor staleness vs performance tradeoff
6. **Cursor pagination** (Month 2):

   - Replace OFFSET pagination with cursor-based
   - Implement for large datasets (> 10,000 rows)
   - Update API to support cursor tokens
7. **Database aggregations** (Month 2):

   - Move aggregations from application to database
   - Use SUM, COUNT, AVG, GROUP BY
   - Reduce data transfer by 1000x
8. **Right database choice** (Month 3-6):

   - Evaluate workload types (transactional, caching, documents, graphs, time-series)
   - Calculate resource requirements for each database type
   - Implement polyglot persistence if savings > 50%

### Beyond Databases

9. **Application code optimization** (Ongoing):

   - Energy-efficient algorithms (see Part 2 of this series)
   - Async/await for I/O-bound operations
   - Lazy loading and pagination
   - Code profiling and optimization
10. **Infrastructure optimization** (Ongoing):

    - Right-size compute instances
    - Use spot instances for batch jobs
    - Choose low-carbon regions
    - Implement auto-scaling
11. **Monitoring and measurement** (Ongoing):

    - Set up continuous monitoring (CloudWatch, Datadog, New Relic)
    - Track energy metrics (power, kWh, CO2e)
    - Report quarterly on sustainability goals
    - Celebrate wins with the team

### Resources for Continued Learning

**Books**:

- "High Performance MySQL" by Baron Schwartz
- "PostgreSQL: Up and Running" by Regina Obe and Leo Hsu
- "Designing Data-Intensive Applications" by Martin Kleppmann

**Online Resources**:

- Use The Index, Luke (https://use-the-index-luke.com/) - SQL indexing guide
- PostgreSQL Performance Tuning (https://wiki.postgresql.org/wiki/Performance_Optimization)
- AWS RDS Best Practices (https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_BestPractices.html)

**Tools**:

- pgAdmin (PostgreSQL GUI)
- MySQL Workbench (MySQL GUI)
- DataGrip (JetBrains multi-database IDE)
- CloudWatch (AWS monitoring)
- Datadog (multi-cloud monitoring)

**Community**:

- Database Administrators Stack Exchange (https://dba.stackexchange.com/)
- PostgreSQL mailing lists (https://www.postgresql.org/list/)
- MySQL forums (https://forums.mysql.com/)

The journey to sustainable software is ongoing. Start with the basics, measure everything, and optimize continuously.

## Key Takeaways

1. **Databases are energy hogs**: They consume 40-60% of backend infrastructure energy through disk I/O, CPU, memory, and network.
2. **Small changes, massive impact**: A single index can save 990 watts of continuous power. Connection pooling can reduce CPU by 20%. Caching can eliminate 90% of queries.
3. **Start with the basics**: Indexes, connection pooling, and avoiding SELECT * provide 50-80% savings with minimal complexity.
4. **Measure everything**: Use EXPLAIN ANALYZE, pg_stat_user_tables, and monitoring tools. You can't optimize what you don't measure.
5. **Fix N+1 queries**: They're never acceptable. Batch operations provide 100-1000x improvement.
6. **Cache aggressively**: 80-95% cache hit rate eliminates 80-95% of database queries. Accept staleness when possible.
7. **Right-size infrastructure**: Don't over-provision. Use auto-scaling and serverless for variable workloads.
8. **Choose the right database**: Polyglot persistence can provide 10-100x improvement for specialized workloads. The operational complexity is worth it.
9. **Embedded carbon matters**: Idle capacity wastes manufacturing emissions. Cloud multi-tenancy and serverless eliminate this waste.
10. **Energy follows performance**: Faster queries = less CPU = less energy. Performance optimization is sustainability optimization.
11. **Tradeoffs are worth it**: The energy savings, cost savings, and performance improvements far outweigh the complexity.
12. **Continuous improvement**: Optimize weekly, measure monthly, report quarterly. Energy savings compound over time.

The database is often the biggest energy consumer in your stack, but it's also the biggest opportunity for optimization. Start today, measure impact, and watch your energy consumption (and cloud bill) drop.

---

*This is Part 3 of the Green Coding series. Read [Part 1: Why Your Code&#39;s Carbon Footprint Matters](#) and [Part 2: Energy-Efficient Algorithm Patterns](#) for more sustainable software practices.*

*Have database optimization stories to share? Found these patterns helpful? Let me know in the comments below.*
