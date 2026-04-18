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

Storage speed determines energy consumption. An SSD read takes ~100 microseconds and consumes ~0.1 watts per operation. Memory access takes ~100 nanoseconds and uses ~0.0001 watts per operation—1000x faster than SSD. A full table scan on 10 million rows means ~10,000 disk operations. At 1000 queries/second, that's 100 kilowatts continuously—the power consumption of 10 homes.

**2. CPU: The Query Processor (30-40% of total)**

Query planning overhead takes 1-2ms for simple queries, 10-50ms for complex ones. At 1000 queries/second, that's 1-50 CPU cores just on planning. Execution costs come from row filtering, joins, aggregations, sorting, and deduplication. A join between two 1 million row tables requires building a 100MB hash table and takes 100-500ms of CPU time.

**3. Memory: The Cache Layer (10-15% of total)**

The buffer pool caches frequently accessed pages, typically 50-80% of RAM. A 128GB server with a 100GB buffer pool consumes 100 watts continuously—about 1 watt per GB. Working memory for sorts, joins, and temporary tables adds more.

**4. Network: The Data Highway (5-10% of total)**

Network interfaces consume 2-5 watts per 1 Gbps, plus switch/router overhead. Transferring 500MB of query results takes 6 seconds at 80 MB/s practical throughput, consuming 12 watt-seconds in network power plus CPU costs for serialization/deserialization.

### The Multiplication Effect

The real problem isn't a single query—it's the multiplication effect. Consider an e-commerce product search that takes 50ms and runs 1000 times per second. That's 86.4 million queries per day. Each query consumes about 0.263 watt-seconds. Daily energy consumption: 6.3 kWh. Annual: 2,300 kWh, costing $230 and producing 920 kg of CO2e.

That's for ONE query pattern. A typical application has 50-100 different query patterns. Total energy: 115-230 kWh per year, $11,500-$23,000 per year, 46-92 tons of CO2e per year.

### Why Inefficient Queries Are Catastrophic

An inefficient query doesn't just waste energy—it wastes it at scale. Take a missing index on an email lookup. An efficient query with an index takes 1ms and uses 0.01 watt-seconds. An inefficient full table scan takes 100ms and uses 1 watt-second—100x more energy per query.

If this query runs 1000 times per second, the efficient version uses 10 watts of continuous power. The inefficient version uses 1000 watts—equivalent to running 10 computers continuously. Over a year, that's the difference between 87.6 kWh ($8.76, 35 kg CO2e) and 8,760 kWh ($876, 3,504 kg CO2e). A difference of $867 per year and 3.5 tons of CO2e for a single missing index.

### The Good News

Small changes have massive impact because queries run millions of times. Fix one query, save millions of executions. Inefficiencies compound—one missing index affects every query that needs it. Optimizations are multiplicative: index + caching + batching = 100x-1000x improvement. And right-sizing reduces waste since a smaller instance means less idle power consumption.

Let's start with the basics.

## Pattern 1: Index Strategically (Not Everything)

**Skill Level**: 🟢 Basic

### The Problem

When you query a database without an index, it performs a sequential scan—reading every single row from disk to find matches. For a 10 million row table, that's 10 million disk reads every time. Disk I/O is expensive. An SSD read takes ~100 microseconds while memory access takes ~100 nanoseconds—1000x slower. When you scan 10 million rows, you're doing 10 million slow operations instead of a handful of fast ones.

But indexes aren't free. Every index consumes disk space (often 20-50% of table size), slows down writes since INSERT, UPDATE, and DELETE must update all indexes, requires maintenance through VACUUM and REINDEX operations, and uses memory for buffer pool space. The worst mistake is creating indexes on every column "just in case." I've seen databases with 20+ indexes on a single table where only 3 were ever used. The other 17 were pure waste.

### The Solution

Index what you actually query, not what you think you might query someday. Start by profiling using EXPLAIN ANALYZE in PostgreSQL, slow query log in MySQL, or explain() in MongoDB to find sequential scans. Look for queries that scan thousands or millions of rows but return only a few.

Composite indexes matter. If you query `WHERE customer_id = 123 AND status = 'pending'`, create an index on both columns: `(customer_id, status)`. The order matters—put the most selective column first. Some databases can answer queries entirely from the index without touching the table. If you query `SELECT id, email FROM users WHERE email = 'user@example.com'`, an index on `(email, id)` can return the result without reading the table at all.

An index is a sorted data structure, usually a B-tree, that maps column values to row locations. For a 10 million row table, that's about 23 B-tree comparisons instead of 10 million disk reads. If your query returns 5 rows, that's 28 disk reads instead of 10 million.

```sql
-- Before: Full table scan
SELECT * FROM orders WHERE customer_id = 123 AND status = 'pending';
-- Seq Scan on orders (cost=0.00..180000.00 rows=5000)

-- After: Composite index
CREATE INDEX idx_orders_customer_status ON orders(customer_id, status);
-- Index Scan using idx_orders_customer_status (cost=0.43..25.50 rows=5)

-- Best: Covering index
CREATE INDEX idx_orders_covering ON orders(customer_id, status) 
  INCLUDE (id, total, created_at);
-- Index-only scan: doesn't touch table at all
```

To find missing indexes in PostgreSQL:

```sql
SELECT schemaname, tablename, seq_scan, seq_tup_read, 
       idx_scan, seq_tup_read / seq_scan as avg_rows_per_scan
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC
LIMIT 20;
```

Look for high seq_tup_read with low idx_scan. These tables need indexes.

**Impact**: Query time drops from 500ms to 2ms (250x faster). CPU usage drops 60%. Disk I/O drops 95%. Memory usage drops 90%. Energy savings around 50% for read-heavy workloads.

The key: profile first, index second. Don't guess. Measure.

## Pattern 2: Connection Pooling Done Right

**Skill Level**: 🟢 Basic

### The Problem

Every database connection has overhead. When your application opens a new connection, it performs a TCP handshake (1-2 network round trips), authentication with username/password verification and SSL negotiation (2-3 round trips), session setup with session variables and prepared statements (1-2 round trips), and memory allocation for connection buffers and prepared statement cache (~10MB per connection). Total time: 50-100ms. For a query that takes 1ms, you're spending 50-100x more time on connection overhead than actual work.

Most databases have connection limits—PostgreSQL defaults to 100, MySQL to 151. If your application opens a new connection per request and you have 200 concurrent requests, you'll hit the limit and start queuing or failing. But too many pooled connections is also wasteful. If you configure a pool of 100 connections but only use 10, you're wasting 900MB of memory and CPU cycles on 90 idle connections.

### The Solution

Connection pooling maintains a pool of open connections that are reused across requests. The application borrows a connection from the pool, executes the query, and returns the connection without closing it. The next request reuses the same connection.

For sizing, start with `pool_size = (CPU cores × 2) + effective_spindle_count`. For cloud databases, 10-20 is usually sufficient. Configure pool_pre_ping to verify connections are alive before using them, pool_recycle to close and recreate connections after N seconds, and max_overflow to allow temporary connections beyond pool_size during spikes.

```python
# Before: New connection per request
def get_user(user_id):
    conn = psycopg2.connect(DATABASE_URL)  # 50ms overhead!
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()  # 5ms overhead
    return user

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
    with engine.connect() as conn:
        result = conn.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return result.fetchone()
```

**Impact**: Connection overhead drops from 50ms to 0ms. Memory usage drops 40%. CPU usage drops 20%. Throughput increases 3x. Database load drops 50% from fewer connection/disconnection events.

## Pattern 3: Query Result Caching

**Skill Level**: 🟡 Intermediate

### The Problem

Every query requires parsing the SQL, planning the execution, executing the plan, formatting results, and transferring over the network. For a simple query that returns the same data repeatedly, you're doing all this work over and over. If 1000 users request the same product page, you're executing the same query 1000 times.

Even with perfect indexes, a query takes 0.5-5ms. At 1000 requests per second, that's 0.5-5 CPU cores just serving repeated queries.

### The Solution

Cache query results. Compute once, serve many times. Use Redis or Memcached at the application level for most cases. For cache invalidation, time-based TTL is simple and works for most cases—cache expires after N seconds. Event-based invalidation happens when data changes but is complex. Lazy invalidation serves stale data while refreshing in the background for the best user experience.

Cache user profiles that change infrequently, product catalogs that change daily or hourly, expensive aggregations, and configuration data. Don't cache real-time data like stock prices, user-specific sensitive data unless encrypted, or data that changes frequently like shopping carts.

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
    query = """
        SELECT u.id, u.name, u.email, p.bio, p.avatar_url,
               COUNT(DISTINCT f.id) as follower_count
        FROM users u
        JOIN profiles p ON u.id = p.user_id
        LEFT JOIN followers f ON u.id = f.following_id
        WHERE u.id = %s
        GROUP BY u.id, u.name, u.email, p.bio, p.avatar_url
    """
    return execute_query(query, (user_id,))
```

**Impact**: With 90% cache hit rate, database queries drop 90%. Database CPU drops 80%. Response time drops from 50ms to 1ms. Database connections drop 90%. Energy savings proportional to cache hit rate, typically 80-90%.

The tradeoff: cache invalidation is hard. Start with high TTL of 5-10 minutes for rarely-changing data. Use event-based invalidation only when necessary.

## Pattern 4: Batch Operations

**Skill Level**: 🟢 Basic

### The Problem

The N+1 query problem is one of the most common performance killers. It happens when you fetch a list of items, then loop through them making individual queries for related data. Loading 100 blog posts with their authors means 101 queries: 1 for posts plus 100 for authors.

Each query has overhead: network round trip (0.5-2ms), query parsing (0.1-0.5ms), query planning (0.1-1ms), execution (0.1-1ms), and result formatting (0.1-0.5ms). Total per query: 1-5ms. For 100 queries, that's 100-500ms of overhead alone. The database also has to acquire/release locks 100 times, update statistics 100 times, log 100 separate operations, and manage 100 separate transactions.

### The Solution

Batch operations fetch or modify multiple rows in a single query. For reads, use IN clause or JOIN. For writes, use multi-row INSERT or UPDATE with VALUES. Batching works because you get a single network round trip, single query parse/plan, bulk execution where the database can optimize, and a single transaction with less lock contention.

```python
# Before: N+1 queries (101 queries, ~5 seconds)
posts = execute_query("SELECT * FROM posts LIMIT 100")
for post in posts:
    author = execute_query("SELECT * FROM users WHERE id = %s", (post['author_id'],))
    post['author'] = author

# After: Batched with IN clause (2 queries, ~0.05 seconds)
posts = execute_query("SELECT * FROM posts LIMIT 100")
author_ids = [post['author_id'] for post in posts]
authors = execute_query("SELECT * FROM users WHERE id IN %s", (tuple(author_ids),))
author_map = {author['id']: author for author in authors}
for post in posts:
    post['author'] = author_map.get(post['author_id'])

# Best: Single query with JOIN (1 query, ~0.02 seconds)
posts = execute_query("""
    SELECT p.*, u.id as author_id, u.name as author_name
    FROM posts p
    JOIN users u ON p.author_id = u.id
    LIMIT 100
""")
```

For writes:

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

Don't batch too large. For reads, batch up to 1000-5000 IDs in an IN clause. For writes, batch 100-1000 rows per INSERT/UPDATE. If you have 10,000 rows, split into 10 batches of 1000.

**Impact**: Execution time drops from 5s to 0.05s (100x faster). Network overhead drops 99%. Database connections drop 99%. Lock contention drops 90%. Transaction log entries drop 99%.

## Pattern 5: Avoid SELECT * (Seriously)

**Skill Level**: 🟢 Basic

### The Problem

SELECT * is convenient, but when you SELECT *, the database reads all columns from disk even if you only use 2 out of 50, transfers all data over the network, allocates memory for all columns, and serializes all data wasting CPU.

The problem compounds with large columns. A TEXT or BLOB column can be megabytes. If you have a blog_content column that's 5MB and you SELECT * for 100 blog posts, you're transferring 500MB when you might only need 100KB of metadata.

Row-oriented databases like PostgreSQL and MySQL store rows contiguously. Reading a row means reading all columns. If your row is 10KB but you only need 100 bytes, you're reading 100x more data than necessary. Database to application transfer is often the bottleneck. A 1 Gbps network delivers 50-80 MB/s with protocol overhead. Transferring 500MB takes 6-10 seconds.

### The Solution

Select only the columns you actually use. Look at your code to see what fields you actually access. If you're returning JSON, only select fields in the JSON. If you're displaying a list, only select fields shown in the list.

```sql
-- Before: 100 posts × 5MB content = 500MB transfer, ~10 seconds
SELECT * FROM blog_posts WHERE author_id = 123;

-- After: 100 posts × 312 bytes = 31KB transfer, ~0.01 seconds
SELECT id, title, excerpt, created_at 
FROM blog_posts 
WHERE author_id = 123;
```

With a covering index, you can avoid touching the table entirely:

```sql
CREATE INDEX idx_blog_posts_covering 
ON blog_posts(author_id) 
INCLUDE (id, title, excerpt, created_at);
```

**Impact**: Network transfer drops 99%. Memory usage drops 99%. Disk I/O drops 95% with covering index. Response time drops from 10s to 0.01s.

## Pattern 6: Optimize JOINs

**Skill Level**: 🟡 Intermediate

### The Problem

JOINs are expensive. The database has to match rows from multiple tables. A nested loop join on 1M × 1M rows means 1 trillion comparisons. Even with indexes, poorly optimized JOINs can scan millions of unnecessary rows.

The database chooses a join algorithm based on table sizes, available indexes, and statistics. Nested loop is best for small tables (< 1000 rows). Hash join is best for large tables with equality conditions. Merge join is best for sorted data. But the database can only choose well if you give it the right tools: indexes on JOIN columns and accurate statistics.

### The Solution

Add indexes on all JOIN columns. Filter early—apply WHERE clauses before JOINs when possible. Remove unnecessary JOINs—if you don't use columns from a joined table, don't join it. Reorder JOINs to filter early—join the most selective tables first.

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

Use EXPLAIN ANALYZE to see what the database is actually doing:

```sql
EXPLAIN ANALYZE
SELECT * FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.status = 'pending';
```

Look for "Seq Scan" (bad), "Nested Loop" on large tables (bad), and "Hash Join" or "Merge Join" (good).

**Impact**: Query time drops from 60s to 0.5s (120x faster). CPU usage drops 95%. Memory usage drops 80%.

## Pattern 7: Pagination Done Right

**Skill Level**: 🟡 Intermediate

### The Problem

OFFSET pagination is the most common approach, but it's catastrophically inefficient for deep pagination. When you query `LIMIT 100 OFFSET 10000`, the database still has to scan 10,100 rows, sort them, then discard the first 10,000. At page 100, you're scanning 10,000 rows just to throw them away.

For a 10 million row table, page 100,000 means scanning 10 million rows. That takes seconds and wastes enormous energy.

### The Solution

Use cursor-based pagination (also called keyset pagination). Instead of OFFSET, use WHERE with the last seen value. This works for any sortable column with an index.

```sql
-- Before: OFFSET pagination (scans 10,100 rows)
SELECT * FROM posts 
ORDER BY created_at DESC 
LIMIT 100 OFFSET 10000;

-- After: Cursor pagination (scans 100 rows)
SELECT * FROM posts 
WHERE created_at < '2024-01-15 10:30:00'
ORDER BY created_at DESC 
LIMIT 100;

-- Create index for efficiency
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
```

For the first page, omit the WHERE clause. For subsequent pages, use the created_at value from the last row of the previous page.

**Impact**: Deep pagination drops from 5s to 0.01s (500x faster). Disk I/O drops 99%. CPU usage drops 95%. Works consistently regardless of page depth.

## Pattern 8: Aggregate in the Database

**Skill Level**: 🟡 Intermediate

### The Problem

Aggregating data in your application means transferring all the raw data over the network, then processing it in application memory. If you need to count 10,000 orders, you're transferring 10,000 rows (potentially megabytes of data) just to count them.

Databases are optimized for aggregation. They can count, sum, average, and group without transferring all the data. They use indexes, parallel execution, and optimized algorithms.

### The Solution

Always aggregate in the database using COUNT, SUM, AVG, GROUP BY, and HAVING. Let the database do what it's designed to do.

```sql
-- Before: Aggregate in application (transfers 10,000 rows)
orders = execute_query("SELECT * FROM orders WHERE status = 'completed'")
total = sum(order['amount'] for order in orders)
count = len(orders)

-- After: Aggregate in database (transfers 1 row)
result = execute_query("""
    SELECT COUNT(*) as count, SUM(amount) as total
    FROM orders 
    WHERE status = 'completed'
""")
```

For complex aggregations with multiple dimensions:

```sql
SELECT 
    DATE_TRUNC('day', created_at) as day,
    status,
    COUNT(*) as order_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount
FROM orders
WHERE created_at >= '2024-01-01'
GROUP BY DATE_TRUNC('day', created_at), status
ORDER BY day DESC, status;
```

**Impact**: Data transferred drops from 10,000 rows to 1 row (10,000x reduction). Network usage drops 99%. Memory usage drops 99%. Query time drops from 5s to 0.05s (100x faster).

## Pattern 9: Choose the Right Database and Deployment Model

**Skill Level**: 🔴 Advanced (Architecture Decision)

### The Problem

Using a relational database for everything is like using a hammer for every job. The wrong database doesn't just perform poorly—it wastes massive amounts of energy. Graph queries in PostgreSQL use 100-1000x more CPU than Neo4j. Time-series in MySQL uses 30x more storage and CPU than TimescaleDB. Simple key-value lookups in an RDBMS have 100x more overhead than Redis.

When you use the wrong database, you compensate with more hardware. That means more servers (more manufacturing emissions), more CPU cycles (more operational energy), more storage (more disk manufacturing and power), and worse performance (frustrated users and wasted resources).

Beyond database type, deployment model matters. Provisioned databases run 24/7 even when idle. Cloud databases offer auto-scaling but have virtualization overhead. On-premises databases give bare metal performance but waste idle capacity. Each choice has different energy and carbon implications.

### The Solution: Match Database to Workload

Different databases are optimized for different workloads. Here's when each type makes sense:

**Relational (PostgreSQL, MySQL)**: Best for structured data with relationships, ACID transactions, and complex queries. Use for user accounts, orders, inventory, and financial transactions. Energy profile: moderate CPU, high disk I/O for joins.

**Document (MongoDB)**: Best for semi-structured data, flexible schemas, and nested documents. Use for product catalogs, user profiles, content management, and configuration. Energy profile: lower CPU (no joins), moderate disk I/O.

**Key-Value (Redis, DynamoDB)**: Best for simple lookups, caching, and session storage. Use for session storage, rate limiting, real-time leaderboards, and caching. Energy profile: very low CPU, minimal disk I/O (often in-memory).

**Graph (Neo4j)**: Best for highly connected data, relationship queries, and traversals. Use for social networks, recommendation engines, fraud detection, and knowledge graphs. Energy profile: high CPU for traversals, but 100-1000x more efficient than SQL for graph queries.

**Time-Series (InfluxDB, TimescaleDB)**: Best for time-stamped data, metrics, and IoT data. Use for metrics, logs, sensor data, financial data, and monitoring. Energy profile: optimized for time-range queries, efficient compression (5-10x less storage).

Here's a concrete example. Finding friends-of-friends (2 degrees of separation) in PostgreSQL requires recursive CTEs, multiple self-joins, and scanning millions of rows. Query time: 5 seconds at 100% CPU. The same query in Neo4j uses native graph traversal following relationship pointers. Query time: 0.05 seconds at 10% CPU. That's 100x faster and 95% less energy.

For time-series data, storing 1 billion metrics in PostgreSQL takes 100 GB uncompressed. Queries scan the full table taking 30 seconds. In TimescaleDB, the same data compresses to 20 GB (5x less storage). Time-based partition scans take 0.1 seconds (300x faster). Hardware requirements drop from db.r5.4xlarge to db.r5.xlarge (4x smaller). Energy per query drops 99%.

### Cloud vs On-Premises: The Utilization Problem

On-premises databases are provisioned for peak load but run at 20-40% average utilization. That means 60-80% of hardware capacity sits idle, still consuming 30-50% of peak power. A database server consuming 300 watts at peak might consume 100-150 watts at idle. If it runs at 30% average utilization, you're wasting 60 watts of idle overhead—40% of power consumption is pure waste.

Manufacturing a server generates 1,000-3,000 kg CO2e before it's even powered on. If your on-prem server runs at 30% utilization, 70% of those manufacturing emissions are wasted. That's embedded carbon waste—manufacturing emissions for hardware that's underutilized.

Cloud providers achieve 60-80% utilization across their fleet through multi-tenancy and workload diversity. Different customers have different usage patterns that balance out. Some peak at night, others during the day. Auto-scaling consolidates workloads on fewer servers. Your share of embedded carbon is proportional to your actual usage, not provisioned capacity.

For variable workloads, cloud wins dramatically. A development database that's only used 8 hours per day (business hours) wastes 67% of energy on-premises (16 hours idle / 24 hours total). In the cloud with auto-scaling, it scales down or pauses during off-hours. Energy savings: 70-90%.

For consistent high-load 24/7 workloads, the calculation is more nuanced. Cloud has 10-20% virtualization overhead but better overall utilization. On-premises has bare metal performance but idle capacity waste. Calculate total cost of ownership including operational energy, embedded carbon, and operational overhead.

One powerful option: hybrid approach. Run production databases on-premises for consistent load and bare metal performance. Run dev/test databases in the cloud to scale to zero when not in use. Run analytics databases in the cloud for variable load and spot instances. Use cloud for disaster recovery, paying only when needed.

### Serverless vs Provisioned: The Idle Capacity Problem

Provisioned databases run 24/7, even when idle. You pay for capacity you don't use. Idle power consumption is 30-50% of peak—CPUs idle, memory powered, disks spinning. For a database provisioned for peak load (1000 requests/second) but averaging 200 requests/second (20% utilization), you're wasting 60-80% of capacity.

Serverless databases scale to zero when idle. After 5-10 minutes of inactivity, they auto-pause. Zero power consumption when paused. You pay per request, not per hour. For variable workloads, energy savings are dramatic: 70-90%.

The tradeoff is cold start latency. First query after an idle period takes 1-30 seconds as the database wakes up. For development, testing, batch jobs, and infrequent access, this is acceptable. For user-facing APIs and real-time applications, it's problematic.

The solution: match deployment model to usage pattern. Use provisioned for 24/7 production workloads where latency matters. Use serverless for development/test environments that can scale to zero. Use serverless with keep-alive pings for staging environments—ping every 4 minutes to prevent auto-pause, maintaining availability while still scaling down capacity. Use serverless for batch jobs and analytics that run on-demand.

A development database on provisioned infrastructure costs $49/month and consumes 36 kWh/month. Active only 8 hours per day means 67% of energy is wasted (24 kWh/month). The same workload on serverless costs $58/month but consumes only 12 kWh/month—67% energy savings. The slightly higher per-hour cost is offset by only paying for 8 hours instead of 24.

### Polyglot Persistence: Right Tool for Each Job

Using multiple databases for different workloads can dramatically reduce resource requirements. A monolithic approach using PostgreSQL for everything might require 5x db.r5.4xlarge instances (80 vCPU, 640 GB RAM) consuming 1,000W with 10,000 kg CO2e in embedded carbon.

A polyglot approach using the right database for each workload—PostgreSQL for user accounts, Redis for sessions, MongoDB for product catalog, Neo4j for recommendations, InfluxDB for metrics—might need only 5x db.r5.large instances (10 vCPU, 77 GB RAM) consuming 250W with 2,500 kg CO2e in embedded carbon. That's 75% reduction in power and embedded carbon, with 10-100x better performance for specialized workloads.

The tradeoff is operational complexity. More databases mean more monitoring, backups, security updates, and team training. The sweet spot is typically 2-4 specialized databases for distinct workload types. If resource savings exceed 50% and your team can manage the complexity, polyglot persistence is worth it.

### Decision Framework

Start by identifying workload types: transactional, caching, documents, graphs, time-series, analytics. Calculate resource requirements (CPU, memory, storage) for each database type. Compare total resource footprint for monolithic versus polyglot approaches. Factor in operational complexity—can your team manage multiple databases? If resource savings exceed 50% and the team can manage it, use polyglot persistence.

For deployment model, consider usage patterns. Variable load and dev/test environments benefit from cloud serverless (70-90% energy savings). Consistent 24/7 production workloads need provisioned databases (no cold starts). Hybrid approaches optimize for each workload type.

For cloud versus on-premises, variable workloads favor cloud (auto-scaling, scale to zero). Consistent high-load workloads require calculating total cost including operational energy, embedded carbon, and operational overhead. Multi-region deployments favor cloud (easy geographic distribution). Low-carbon priority favors cloud (choose low-carbon regions—grid carbon intensity varies 10-30x by region).

**Impact**: Right database for workload delivers 10-100x performance improvement. Energy savings of 50-95% for specialized workloads. Embedded carbon savings of 50-75% from smaller hardware footprint. Storage savings of 5-10x from compression and optimization. Cloud auto-scaling provides 70-90% energy savings for variable workloads. Serverless deployment provides 70-90% energy savings for dev/test environments. The tradeoff is operational complexity (+20-50%), but for large systems, the efficiency gains far outweigh the complexity cost.

## Real-World Case Study: E-Commerce Platform Optimization

**Company**: Mid-sized e-commerce platform  
**Scale**: 50K queries/second, 10M products, 100M orders  
**Initial State**: db.r5.8xlarge (32 vCPUs), $15K/month, 2000 kWh/month

### Week 1: Indexing and Connection Pooling

Added 12 strategic indexes on frequently queried columns. Implemented connection pooling with pool_size=15. Fixed SELECT * in product listing queries.

**Results**: Query time -60%, CPU usage -40%, cost $12K/month (-20%)

### Week 2: Caching

Implemented Redis caching for product catalog, user profiles, and category pages. Achieved 85% cache hit rate.

**Results**: Database queries -85%, CPU usage -70%, cost $8K/month (-47%)

### Week 3: Batching and Aggregation

Fixed N+1 queries in order history (100+ queries → 2 queries). Moved analytics aggregations from application to database. Implemented cursor pagination for product browsing.

**Results**: Query time -80%, network transfer -90%, cost $5K/month (-67%)

### Week 4: Right-Sizing

With optimizations in place, downgraded to db.r5.xlarge (4 vCPUs). Monitored for one week—CPU usage stayed at 30-40%, plenty of headroom.

**Final Results**:
- Instance: db.r5.8xlarge → db.r5.xlarge (8x smaller)
- Cost: $15K/month → $2K/month (87% reduction, $156K/year savings)
- Energy: 2000 kWh/month → 250 kWh/month (87.5% reduction)
- CO2e: 800 kg/month → 100 kg/month (87.5% reduction, 8.4 tons/year)
- Performance: Same or better (avg query time 50ms → 2ms)

### Key Lessons

Start with profiling. They used pg_stat_statements to find the worst queries. The top 10 queries accounted for 80% of database load.

Quick wins matter. Indexing and connection pooling took 2 days and delivered 20% cost reduction immediately.

Caching is powerful. An 85% cache hit rate meant 85% fewer database queries. This was the single biggest impact.

Batching is low-hanging fruit. Finding and fixing N+1 queries took 3 days and delivered massive improvements.

Right-size after optimizing. Don't right-size first. Optimize first, then right-size based on actual usage.

## Key Takeaways

1. **Databases are energy hogs**: They consume 40-60% of backend infrastructure energy through disk I/O, CPU, memory, and network.

2. **The multiplication effect is real**: One inefficient query × millions of executions = catastrophic waste. A single missing index can waste 3.5 tons of CO2e per year.

3. **Profile first, optimize second**: Use EXPLAIN ANALYZE, slow query logs, and pg_stat_statements. Don't guess what's slow—measure it.

4. **Index strategically**: Not everything, just what you query. Composite indexes and covering indexes are your friends.

5. **Pool connections**: Eliminate 50-100ms of overhead per query. Use 10-20 connections for most applications.

6. **Cache aggressively**: 90% cache hit rate = 90% less database load. Start with 5-10 minute TTL for rarely-changing data.

7. **Batch operations**: Fix N+1 queries. Use IN clauses and JOINs. One query instead of 100.

8. **Select precisely**: Only the columns you need. Avoid SELECT * especially with large TEXT/BLOB columns.

9. **Optimize JOINs**: Add indexes on JOIN columns. Filter early. Use EXPLAIN ANALYZE to verify.

10. **Paginate with cursors**: OFFSET is catastrophic for deep pagination. Use WHERE with indexed columns.

11. **Aggregate in the database**: Don't transfer 10,000 rows to count them. Use COUNT, SUM, AVG, GROUP BY.

12. **Right-size after optimizing**: Optimize first, then downgrade your instance. You'll be surprised how much smaller you can go.

The bottom line: database optimization isn't about exotic techniques. It's about eliminating waste. A missing index, an uncached query, or an N+1 problem wastes energy at scale. Fix these fundamental issues and you'll cut costs 70-90% while reducing your carbon footprint.

Start with the quick wins—indexing, connection pooling, fixing SELECT *. These take days, not weeks, and deliver immediate impact. Then move to caching and batching. Finally, right-size your infrastructure based on actual usage.

The patterns are straightforward. The impact is dramatic. And the planet will thank you.

Next in the series: Efficient API design patterns that reduce network overhead and server load.

---

*Have database optimization stories? Share them in the comments. What patterns have you found most effective?*


## Resources

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

---

*This is Part 3 of the Green Coding series. Read [Part 1: Why Your Code's Carbon Footprint Matters](#) and [Part 2: Energy-Efficient Algorithm Patterns](#) for more sustainable software practices.*
