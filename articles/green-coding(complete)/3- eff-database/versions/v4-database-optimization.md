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

Every database query touches four major subsystems, each with its own energy cost. Disk I/O is the biggest drain at 40-50% of total energy consumption. An SSD read takes about 100 microseconds and consumes 0.1 watts per operation. Memory access is 1000x faster at 100 nanoseconds and uses 0.0001 watts. When you do a full table scan on 10 million rows, you're performing roughly 10,000 disk operations. At 1000 queries per second, that's 100 kilowatts continuously—the power consumption of 10 homes.

CPU comes next at 30-40% of energy. Query planning alone takes 1-2ms for simple queries and 10-50ms for complex ones. At 1000 queries per second, that's 1-50 CPU cores just doing planning work. A join between two 1 million row tables requires building a 100MB hash table and takes 100-500ms of CPU time.

Memory accounts for 10-15% through the buffer pool that caches frequently accessed pages. A 128GB server with a 100GB buffer pool consumes 100 watts continuously—about 1 watt per GB. Network rounds out the picture at 5-10%, with network interfaces consuming 2-5 watts per 1 Gbps plus switch and router overhead.

### The Multiplication Effect

The real problem isn't a single query—it's the multiplication effect. Consider an e-commerce product search that takes 50ms and runs 1000 times per second. That's 86.4 million queries per day. Each query consumes about 0.263 watt-seconds (disk I/O, CPU, memory, and network combined). Daily energy consumption: 6.3 kWh. Annual: 2,300 kWh, costing $230 and producing 920 kg of CO2e.

That's for ONE query pattern. A typical application has 50-100 different query patterns. Total energy: 115-230 kWh per year, $11,500-$23,000 per year, 46-92 tons of CO2e per year.

An inefficient query doesn't just waste energy—it wastes it at scale. Take a missing index on an email lookup. An efficient query with an index takes 1ms and uses 0.01 watt-seconds. An inefficient full table scan takes 100ms and uses 1 watt-second. That's 100x more energy per query.

If this query runs 1000 times per second, the efficient version uses 10 watts of continuous power. The inefficient version uses 1000 watts—equivalent to running 10 computers continuously. Over a year, that's the difference between 87.6 kWh ($8.76, 35 kg CO2e) and 8,760 kWh ($876, 3,504 kg CO2e). A difference of $867 per year and 3.5 tons of CO2e for a single missing index.

The good news? Small changes have massive impact because queries run millions of times. Fix one query, save millions of executions. Inefficiencies compound, so one missing index affects every query that needs it. Optimizations are multiplicative—index plus caching plus batching equals 100x-1000x improvement. And right-sizing reduces waste since a smaller instance means less idle power consumption.

## Pattern 1: Index Strategically (Not Everything)

When you query a database without an index, it performs a sequential scan—reading every single row from disk to find matches. For a 10 million row table, that's 10 million disk reads every time. Disk I/O is expensive. An SSD read takes about 100 microseconds while memory access takes 100 nanoseconds. That's 1000x slower. When you scan 10 million rows, you're doing 10 million slow operations instead of a handful of fast ones.

But indexes aren't free. Every index consumes disk space (often 20-50% of table size), slows down writes since INSERT, UPDATE, and DELETE must update all indexes, requires maintenance through VACUUM and REINDEX operations, and uses memory for buffer pool space. The worst mistake is creating indexes on every column "just in case." I've seen databases with 20+ indexes on a single table where only 3 were ever used. The other 17 were pure waste—slowing down every write, consuming memory, wasting disk space.

The solution is to index what you actually query, not what you think you might query someday. Start by profiling using EXPLAIN ANALYZE in PostgreSQL, slow query log in MySQL, or explain() in MongoDB to find sequential scans. Look for queries that scan thousands or millions of rows but return only a few.

Composite indexes matter. If you query `WHERE customer_id = 123 AND status = 'pending'`, create an index on both columns: `(customer_id, status)`. The order matters—put the most selective column first, the one that filters out the most rows. Some databases can answer queries entirely from the index without touching the table. If you query `SELECT id, email FROM users WHERE email = 'user@example.com'`, an index on `(email, id)` can return the result without reading the table at all.

An index is a sorted data structure, usually a B-tree, that maps column values to row locations. Instead of scanning every row, the database searches the B-tree in logarithmic time. For a 10 million row table, that's about 23 comparisons instead of 10 million disk reads. If your query returns 5 rows, that's 28 disk reads instead of 10 million.

```sql
-- Before: Full table scan
SELECT * FROM orders WHERE customer_id = 123 AND status = 'pending';
-- Seq Scan on orders (cost=0.00..180000.00 rows=5000)
-- Reads all 10M rows from disk, filters in memory

-- After: Composite index
CREATE INDEX idx_orders_customer_status ON orders(customer_id, status);
-- Index Scan using idx_orders_customer_status (cost=0.43..25.50 rows=5)
-- Searches B-tree, reads only matching rows

-- Even better: Covering index
CREATE INDEX idx_orders_covering ON orders(customer_id, status) 
  INCLUDE (id, total, created_at);
-- Index-only scan: doesn't touch table at all
```

To find missing indexes in PostgreSQL, query the statistics:

```sql
SELECT schemaname, tablename, seq_scan, seq_tup_read, 
       idx_scan, seq_tup_read / seq_scan as avg_rows_per_scan
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC
LIMIT 20;
```

Look for high seq_tup_read with low idx_scan. These tables need indexes.

The impact is dramatic. Query time drops from 500ms to 2ms (250x faster). CPU usage drops 60% from less row filtering. Disk I/O drops 95% from reading 28 rows instead of 10 million. Memory usage drops 90% from a smaller working set. Energy savings are around 50% for read-heavy workloads.

The key: profile first, index second. Don't guess. Measure.

## Pattern 2: Connection Pooling Done Right

Every database connection has overhead. When your application opens a new connection, it performs a TCP handshake (1-2 network round trips), authentication with username/password verification and SSL negotiation (2-3 round trips), session setup with session variables and prepared statements (1-2 round trips), and memory allocation for connection buffers and prepared statement cache (about 10MB per connection). Total time: 50-100ms. For a query that takes 1ms, you're spending 50-100x more time on connection overhead than actual work.

Each idle connection also consumes resources. Memory for buffers, caches, and session state runs about 10MB per connection. CPU handles keep-alive packets and connection monitoring. File descriptors are a limited resource on the database server. Most databases have connection limits—PostgreSQL defaults to 100, MySQL to 151. If your application opens a new connection per request and you have 200 concurrent requests, you'll hit the limit and start queuing or failing.

But too many pooled connections is also wasteful. If you configure a pool of 100 connections but only use 10, you're wasting 900MB of memory and CPU cycles on 90 idle connections.

Connection pooling maintains a pool of open connections that are reused across requests. The application borrows a connection from the pool, executes the query, and returns the connection to the pool without closing it. The next request reuses the same connection.

For sizing the pool, start with `pool_size = (CPU cores × 2) + effective_spindle_count`. For cloud databases, 10-20 is usually sufficient. Monitor connection usage and adjust. Configure pool_pre_ping to verify connections are alive before using them, pool_recycle to close and recreate connections after N seconds, and max_overflow to allow temporary connections beyond pool_size during spikes.

Without pooling, three requests take 168ms for 3ms of actual work. With pooling, the same three requests take 3ms total.

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
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
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

Connection overhead drops from 50ms to 0ms. Memory usage drops 40% from using 10 connections instead of 100+ transient ones. CPU usage drops 20% from eliminating connection churn. Throughput increases 3x from removing the connection bottleneck. Database load drops 50% from fewer connection and disconnection events.

## Pattern 3: Query Result Caching

Databases are good at executing queries, but they're not magic. Every query requires parsing the SQL, planning the execution by choosing indexes and join order, executing the plan by reading data and filtering and sorting, formatting results, and transferring over the network. For a simple query that returns the same data repeatedly, you're doing all this work over and over. If 1000 users request the same product page, you're executing the same query 1000 times.

Even with perfect indexes, a query takes time. Index lookup takes 0.1-1ms, row retrieval takes 0.1-1ms per row, and network transfer takes 0.1-1ms. Total: 0.5-5ms per query. At 1000 requests per second, that's 500-5000ms of database CPU time per second—0.5-5 CPU cores just serving repeated queries.

Cache query results. Compute once, serve many times. Use Redis or Memcached at the application level for most cases. For cache invalidation, time-based TTL is simple and works for most cases—cache expires after N seconds. Event-based invalidation happens when data changes but is complex. Lazy invalidation serves stale data while refreshing in the background for the best user experience.

Cache user profiles that change infrequently, product catalogs that change daily or hourly, expensive aggregations, and configuration data that rarely changes. Don't cache real-time data like stock prices or live scores, user-specific sensitive data unless encrypted, or data that changes frequently like shopping carts or inventory.

Without caching, 1000 requests mean 5000ms of database CPU time. With 90% cache hit rate, you get 500ms of database time plus 90ms of cache time for 590ms total. That's 88% less database load.

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

The first call is a cache miss and queries the database in 50ms. The next 1000 calls are cache hits reading from Redis in 0.1ms each. That saves 49.9ms times 1000, which equals 50 seconds of database time.

A 90% cache hit rate means 90% fewer database queries. Database CPU drops 80% since only 10% of queries hit the database. Response time drops from 50ms to 1ms since cache is 50x faster. Database connections drop 90% from fewer concurrent queries. Energy savings are proportional to cache hit rate, typically 80-90%.

The tradeoff is that cache invalidation is hard. Start with high TTL of 5-10 minutes for rarely-changing data. Use event-based invalidation only when necessary. Monitor staleness versus hit rate.

## Pattern 4: Batch Operations

The N+1 query problem is one of the most common performance killers. It happens when you fetch a list of items, then loop through them making individual queries for related data. Loading 100 blog posts with their authors means fetching posts, then for each post fetching the author. That's 101 queries: 1 for posts plus 100 for authors.

Each query has overhead. Network round trip takes 0.5-2ms even on localhost. Query parsing takes 0.1-0.5ms. Query planning takes 0.1-1ms. Execution takes 0.1-1ms. Result formatting takes 0.1-0.5ms. Total per query: 1-5ms. For 100 queries, that's 100-500ms of overhead alone before any actual work. The database also has to acquire and release locks 100 times, update statistics 100 times, log 100 separate operations, and manage 100 separate transactions.

Batch operations fetch or modify multiple rows in a single query. For reads, use IN clause or JOIN. For writes, use multi-row INSERT or UPDATE with VALUES or bulk operations. Batching works because you get a single network round trip instead of 100, single query parse and plan instead of 100, bulk execution where the database can optimize by sorting and batching I/O, and a single transaction with less lock contention.

The N+1 approach takes 112ms total. The batched approach takes 4ms total. That's 96% faster.

```python
# Before: N+1 queries (101 queries, ~5 seconds)
def get_posts_with_authors_slow():
    posts = execute_query("SELECT * FROM posts LIMIT 100")
    for post in posts:
        author = execute_query(
            "SELECT * FROM users WHERE id = %s",
            (post['author_id'],)
        )
        post['author'] = author
    return posts

# After: Batched with IN clause (2 queries, ~0.05 seconds)
def get_posts_with_authors_fast():
    posts = execute_query("SELECT * FROM posts LIMIT 100")
    author_ids = [post['author_id'] for post in posts]
    authors = execute_query(
        "SELECT * FROM users WHERE id IN %s",
        (tuple(author_ids),)
    )
    author_map = {author['id']: author for author in authors}
    for post in posts:
        post['author'] = author_map.get(post['author_id'])
    return posts

# Best: Single query with JOIN (1 query, ~0.02 seconds)
def get_posts_with_authors_best():
    return execute_query("""
        SELECT p.*, u.id as author_id, u.name as author_name
        FROM posts p
        JOIN users u ON p.author_id = u.id
        LIMIT 100
    """)
```

For writes, batch updates instead of individual queries:

```python
# Before: 1000 queries, ~5 seconds
def update_user_scores_slow(user_scores):
    for user_id, score in user_scores.items():
        execute_query(
            "UPDATE users SET score = %s WHERE id = %s",
            (score, user_id)
        )

# After: 1 query, ~0.05 seconds
def update_user_scores_fast(user_scores):
    values = [(user_id, score) for user_id, score in user_scores.items()]
    execute_values(cursor, """
        UPDATE users SET score = v.score
        FROM (VALUES %s) AS v(id, score)
        WHERE users.id = v.id
    """, values)
```

Don't batch too large though. Most databases have max packet size limits (MySQL defaults to 16MB). Large batches consume memory on both client and server. Very large batches hold locks longer. Large transactions can cause replication lag. For reads, batch up to 1000-5000 IDs in an IN clause. For writes, batch 100-1000 rows per INSERT or UPDATE. If you have 10,000 rows, split into 10 batches of 1000.

Going from 1000 queries to 1 query means execution time drops from 5 seconds to 0.05 seconds—100x faster. Network overhead drops 99% from 1 round trip instead of 1000. Database connections drop 99% from 1 connection instead of 1000 concurrent. Lock contention drops 90% from fewer, shorter locks. Transaction log entries drop 99% from 1 transaction instead of 1000.

This is low-hanging fruit. Find your N+1 queries by looking for loops with database calls inside and batch them. The impact is immediate and dramatic.

## Pattern 5: Avoid SELECT * (Seriously)

SELECT * is convenient. You don't have to think about which columns you need. But convenience has a cost. When you SELECT *, the database reads all columns from disk even if you only use 2 out of 50, transfers all data over the network wasting bandwidth, allocates memory for all columns, and serializes all data wasting CPU.

The problem compounds with large columns. A TEXT or BLOB column can be megabytes. If you have a blog_content column that's 5MB and you SELECT * for 100 blog posts, you're transferring 500MB when you might only need 100KB of metadata.

Row-oriented databases like PostgreSQL and MySQL store rows contiguously. Reading a row means reading all columns. If your row is 10KB but you only need 100 bytes, you're reading 100x more data than necessary. Database to application transfer is often the bottleneck. A 1 Gbps network has 125 MB/s theoretical max but in practice delivers 50-80 MB/s with protocol overhead. Transferring 500MB takes 6-10 seconds. The application must allocate memory for all columns, creating garbage collection pressure especially in Java and Python, and filling caches with unused data.

Select only the columns you actually use. Look at your code to see what fields you actually access. If you're returning JSON, only select fields in the JSON. If you're displaying a list, only select fields shown in the list.

SELECT * is okay for small tables with less than 10 columns and less than 1KB per row, when you genuinely need all columns, or in internal admin tools where convenience matters more than performance.

```sql
-- Before: 100 posts × 5MB content = 500MB transfer, ~10 seconds
SELECT * FROM blog_posts WHERE author_id = 123;

-- After: 100 posts × 312 bytes = 31KB transfer, ~0.01 seconds
SELECT id, title, excerpt, created_at 
FROM blog_posts 
WHERE author_id = 123;
```

With SELECT *, you transfer 500MB, allocate 500MB of memory, and take about 10 seconds. With selective columns, you transfer 31KB, allocate 31KB of memory, and take 0.01 seconds. That's 16,000x less data transferred.

Network usage drops 99%. Memory usage drops 99%. Disk I/O drops 95% if using a covering index. Response time drops from 10 seconds to 0.01 seconds.

## Measuring Impact

Before optimization, a database handling 1000 queries per second with 50ms average query time, 80% CPU usage, 90GB memory usage, running on a db.r5.8xlarge with 32 vCPUs costs $15,000 per month, consumes about 2000 kWh per month, and produces about 800 kg of CO2e per month.

After applying all patterns—indexing, connection pooling, caching, batching, and selective columns—the same 1000 queries per second run with 2ms average query time (25x faster), 20% CPU usage, 20GB memory usage, on a db.r5.xlarge with 4 vCPUs, costing $2,000 per month, consuming about 250 kWh per month, and producing about 100 kg of CO2e per month.

The savings: $13,000 per month or $156,000 per year. Energy reduction of 87.5%. CO2e reduction of 87.5%, which is 8.4 tons per year.

## Implementation Strategy

Start with quick wins in week one. Add missing indexes, implement connection pooling, fix SELECT * queries, and batch N+1 queries. These require minimal code changes and deliver immediate impact.

Week two focuses on caching. Set up Redis or Memcached, cache expensive queries, and monitor cache hit rate aiming for 80-95%. This requires more infrastructure but the payoff is substantial.

Week three tackles advanced optimizations. Optimize joins with appropriate algorithms and indexes. Partition large tables by time, geography, or category. Set up read replicas to distribute load.

Week four is about monitoring and tuning. Set up query monitoring, track slow queries, right-size your database instance based on actual usage, and measure energy and cost savings to quantify the impact.

For monitoring, PostgreSQL provides pg_stat_statements to find slow queries and pg_stat_user_tables to find missing indexes. Track queries by total time, number of calls, mean time, and max time. Look for tables with high sequential scan counts and low index scan counts.

## The Bottom Line

Database optimization isn't about exotic techniques. It's about eliminating waste. A missing index, an uncached query, or an N+1 problem wastes energy at scale. Fix these fundamental issues and you'll cut costs 70-90% while reducing your carbon footprint.

The patterns are straightforward. Index what you query. Pool your connections. Cache repeated queries. Batch your operations. Select only what you need. Each pattern alone delivers significant savings. Combined, they transform your database from an energy hog into an efficient workhorse.

The multiplication effect works in your favor once you optimize. Every query you fix saves energy millions of times. Every optimization compounds with others. The result is dramatic: lower costs, better performance, and a smaller environmental footprint.

Next in the series: Efficient API design patterns that reduce network overhead and server load.

---

*Have database optimization stories? Share them in the comments. What patterns have you found most effective?*
