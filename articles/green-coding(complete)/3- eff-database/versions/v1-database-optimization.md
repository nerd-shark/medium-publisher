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

Your database does more work than any other part of your stack. Every query touches disk, memory, CPU, and network. Inefficient queries multiply across millions of executions.

The physics: disk I/O is 1000x more expensive than memory access. A single full table scan can waste more energy than your entire application logic.

Typical database energy breakdown:
- **Disk I/O**: 40-50% (reading data from storage)
- **CPU**: 30-40% (query processing, joins, aggregations)
- **Memory**: 10-15% (caching, buffer pools)
- **Network**: 5-10% (transferring results)

The good news: small changes have massive impact. Let's start with the basics.

## Pattern 1: Index Strategically (Not Everything)

**Skill Level**: 🟢 Basic

### The Problem

No indexes = full table scans = massive waste. But too many indexes = slow writes, wasted storage, index maintenance overhead. Wrong indexes = unused, pure waste.

### The Solution

Index what you query, not what you think you might query.

Use EXPLAIN ANALYZE (PostgreSQL), slow query log (MySQL), or explain() (MongoDB) to find sequential scans.


### Code Example

```sql
-- Before: Full table scan
SELECT * FROM orders WHERE customer_id = 123 AND status = 'pending';
-- Seq Scan on orders (cost=0.00..180000.00 rows=5000)

-- After: Composite index
CREATE INDEX idx_orders_customer_status ON orders(customer_id, status);
-- Index Scan using idx_orders_customer_status (cost=0.43..25.50 rows=5)
```

### Impact

- Query time: 500ms → 2ms (250x faster)
- CPU usage: -60%
- Disk I/O: -95%
- Energy savings: ~50% for read-heavy workloads

The key: profile first, index second. Don't guess.

## Pattern 2: Connection Pooling Done Right

**Skill Level**: 🟢 Basic

### The Problem

Opening/closing connections is expensive. TCP handshake, authentication, session setup—it all adds up. Each idle connection consumes ~10MB memory + CPU for keep-alive.

Too few connections = queuing, slow responses. Too many connections = memory waste, context switching overhead.

### The Solution

Connection pooling with proper sizing.

### Code Example

```python
# Before: New connection per request
def get_user(user_id):
    conn = psycopg2.connect(DATABASE_URL)  # Expensive!
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# After: Connection pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,        # Connections to keep open
    max_overflow=20,     # Additional connections under load
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600    # Recycle connections after 1 hour
)

def get_user(user_id):
    with engine.connect() as conn:  # Reuses pooled connection
        result = conn.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return result.fetchone()
```

### Impact

- Connection overhead: 50ms → 0ms
- Memory usage: -40% (fewer idle connections)
- CPU usage: -20% (less connection churn)
- Throughput: +3x (no connection bottleneck)

Use HikariCP (Java), SQLAlchemy (Python), pg-pool (Node.js), or database/sql (Go).


## Pattern 3: Query Result Caching

**Skill Level**: 🟡 Intermediate

### The Problem

Repeated queries for the same data. The database does the same work over and over. Even fast queries add up at scale.

### The Solution

Cache query results with proper invalidation. Use Redis, Memcached, or database query caches.

### Code Example

```python
import redis
import json
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379)

def cache_query(ttl=300):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key = f"{func.__name__}:{json.dumps(args)}:{json.dumps(kwargs)}"
            
            # Try cache first
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Cache miss - query database
            result = func(*args, **kwargs)
            
            # Store in cache
            redis_client.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator

@cache_query(ttl=600)  # Cache for 10 minutes
def get_user_profile(user_id):
    # Expensive query with joins
    query = """
        SELECT u.*, p.bio, p.avatar_url, COUNT(f.id) as follower_count
        FROM users u
        JOIN profiles p ON u.id = p.user_id
        LEFT JOIN followers f ON u.id = f.following_id
        WHERE u.id = %s
        GROUP BY u.id, p.bio, p.avatar_url
    """
    return execute_query(query, (user_id,))
```

### Impact

- 90% cache hit rate = 90% fewer database queries
- Database CPU: -80%
- Response time: 50ms → 1ms
- Energy savings: Proportional to cache hit rate

The tradeoff: cache invalidation is hard. Start with high TTL for rarely-changing data.

## Pattern 4: Batch Operations

**Skill Level**: 🟢 Basic

### The Problem

N queries in a loop. The N+1 problem. Each query has overhead—parsing, planning, execution, network. 1000 queries = 1000x overhead.

### The Solution

Batch inserts, updates, and queries.

### Code Example

```python
# Before: N queries (N+1 problem)
def update_user_scores_slow(user_scores):
    for user_id, score in user_scores.items():
        execute_query(
            "UPDATE users SET score = %s WHERE id = %s",
            (score, user_id)
        )
    # 1000 users = 1000 queries = ~5 seconds

# After: Single batched query
def update_user_scores_fast(user_scores):
    # Build VALUES clause
    values = [(user_id, score) for user_id, score in user_scores.items()]
    
    # Single query with CASE statement
    query = """
        UPDATE users SET score = v.score
        FROM (VALUES %s) AS v(id, score)
        WHERE users.id = v.id
    """
    execute_values(cursor, query, values)
    # 1000 users = 1 query = ~0.05 seconds
```

### Impact

- 1000 queries → 1 query
- Execution time: 5s → 0.05s (100x faster)
- Database connections: -99%
- Network overhead: -99%

This is low-hanging fruit. Find your N+1 queries and batch them.


## Pattern 5: Avoid SELECT * (Seriously)

**Skill Level**: 🟢 Basic

### The Problem

Fetching columns you don't need. More data = more disk I/O, more network transfer, more memory. Especially bad with TEXT/BLOB columns.

### The Solution

Select only what you need.

### Code Example

```sql
-- Before: Fetching everything (including 5MB blog_content column)
SELECT * FROM blog_posts WHERE author_id = 123;
-- Returns 100 posts × 5MB each = 500MB transferred

-- After: Select only needed columns
SELECT id, title, excerpt, published_at FROM blog_posts WHERE author_id = 123;
-- Returns 100 posts × 1KB each = 100KB transferred
-- 5000x less data!
```

### Impact

- Network transfer: -99%
- Memory usage: -95%
- Disk I/O: -90%
- Query time: 200ms → 5ms

This is the easiest optimization. Stop using SELECT *.

## Pattern 6: Optimize JOINs

**Skill Level**: 🟡 Intermediate

### The Problem

Cartesian products from missing JOIN conditions. Wrong JOIN order. Unnecessary JOINs. The database optimizer doesn't always get it right.

### The Solution

Filter early, JOIN late. Understand JOIN mechanics.

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
-- Scans all orders, then filters

-- After: Filter early, JOIN late
SELECT o.id, o.total, u.name, p.name as product_name
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE u.country = 'US'
  AND o.created_at > '2024-01-01';
-- Filters users first (smaller dataset), then JOINs
```

### Impact

- Rows processed: 10M → 100K (100x reduction)
- Query time: 5s → 0.1s
- CPU usage: -95%

Use EXPLAIN ANALYZE to see what the database is actually doing.

## Pattern 7: Pagination Done Right

**Skill Level**: 🟡 Intermediate

### The Problem

OFFSET pagination scans and discards rows. OFFSET 1000000 LIMIT 10 scans 1,000,010 rows, returns 10. Gets slower as you paginate deeper.

### The Solution

Cursor-based pagination (keyset pagination).

### Code Example

```sql
-- Before: OFFSET pagination (slow for deep pages)
SELECT * FROM posts 
ORDER BY created_at DESC 
OFFSET 1000000 LIMIT 10;
-- Scans 1,000,010 rows, returns 10

-- After: Cursor-based pagination
SELECT * FROM posts 
WHERE created_at < '2024-01-15 10:30:00'  -- Last seen timestamp
ORDER BY created_at DESC 
LIMIT 10;
-- Scans 10 rows, returns 10
-- Requires index on created_at
```

### Impact

- Deep pagination: 5s → 0.01s (500x faster)
- Rows scanned: 1M → 10 (100,000x reduction)
- Consistent performance regardless of page depth

The tradeoff: can't jump to arbitrary pages. But for infinite scroll or "next page" navigation, it's perfect.


## Pattern 8: Aggregate in the Database

**Skill Level**: 🟡 Intermediate

### The Problem

Fetching all rows to your application, aggregating in code. Transferring massive datasets over the network. Doing work that databases are optimized for.

### The Solution

Use database aggregation functions.

### Code Example

```python
# Before: Aggregate in application
def get_order_stats_slow(user_id):
    orders = execute_query(
        "SELECT total, created_at FROM orders WHERE user_id = %s",
        (user_id,)
    )  # Fetches 10,000 orders
    
    total_spent = sum(order['total'] for order in orders)
    order_count = len(orders)
    avg_order = total_spent / order_count if order_count > 0 else 0
    
    return {
        'total_spent': total_spent,
        'order_count': order_count,
        'avg_order': avg_order
    }

# After: Aggregate in database
def get_order_stats_fast(user_id):
    result = execute_query("""
        SELECT 
            SUM(total) as total_spent,
            COUNT(*) as order_count,
            AVG(total) as avg_order
        FROM orders 
        WHERE user_id = %s
    """, (user_id,))
    
    return result[0]  # Single row result
```

### Impact

- Data transferred: 10,000 rows → 1 row
- Network: 5MB → 100 bytes
- Processing time: 500ms → 5ms
- Memory usage: -99%

Let the database do what it's good at.

## Pattern 9: Materialized Views for Complex Queries

**Skill Level**: 🔴 Advanced

### The Problem

Complex aggregations that run frequently. Multi-table JOINs with GROUP BY. Queries that take seconds but results change infrequently.

### The Solution

Materialized views with refresh strategy.

### Code Example

```sql
-- Complex query that runs 1000x/day
SELECT 
    p.category,
    COUNT(*) as product_count,
    AVG(p.price) as avg_price,
    SUM(oi.quantity) as total_sold,
    SUM(oi.quantity * oi.price) as revenue
FROM products p
LEFT JOIN order_items oi ON p.id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.id
WHERE o.created_at > NOW() - INTERVAL '30 days'
GROUP BY p.category;
-- Takes 5 seconds each time

-- Create materialized view
CREATE MATERIALIZED VIEW product_category_stats AS
SELECT 
    p.category,
    COUNT(*) as product_count,
    AVG(p.price) as avg_price,
    SUM(oi.quantity) as total_sold,
    SUM(oi.quantity * oi.price) as revenue
FROM products p
LEFT JOIN order_items oi ON p.id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.id
WHERE o.created_at > NOW() - INTERVAL '30 days'
GROUP BY p.category;

-- Refresh once per hour (scheduled job)
REFRESH MATERIALIZED VIEW product_category_stats;

-- Query the view (instant)
SELECT * FROM product_category_stats WHERE category = 'Electronics';
-- Takes 0.001 seconds
```

### Impact

- Query time: 5s → 0.001s (5000x faster)
- Database load: 1000 expensive queries/day → 24 refresh operations/day
- CPU usage: -99%
- Energy savings: Massive (compute once, read many times)

The tradeoff: stale data between refreshes. Perfect for analytics and dashboards where real-time isn't critical.


## Choosing the Right Database for the Job

**Skill Level**: 🔴 Advanced (Architecture Decision)

### The Problem

Using RDBMS for everything, even when NoSQL would be more efficient. Graph queries in relational databases. Time-series data in general-purpose databases. Wrong database = 10-100x more energy for the same workload.

### The Solution

Match database type to data access patterns.

### Database Types and Energy Characteristics

**Relational (PostgreSQL, MySQL)**
- Best for: Structured data, complex queries, ACID transactions
- Energy profile: Moderate CPU, high disk I/O for joins
- Example: User accounts, orders, inventory

**Document (MongoDB, CouchDB)**
- Best for: Semi-structured data, flexible schemas, nested documents
- Energy profile: Lower CPU (no joins), moderate disk I/O
- Example: Product catalogs, user profiles, content management

**Key-Value (Redis, DynamoDB)**
- Best for: Simple lookups, caching, session storage
- Energy profile: Very low CPU, minimal disk I/O (often in-memory)
- Example: Session storage, rate limiting, real-time leaderboards

**Graph (Neo4j, Amazon Neptune)**
- Best for: Highly connected data, relationship queries
- Energy profile: High CPU for traversals, but efficient for graph queries
- Example: Social networks, recommendation engines, fraud detection

**Time-Series (InfluxDB, TimescaleDB)**
- Best for: Time-stamped data, metrics, IoT data
- Energy profile: Optimized for time-range queries, efficient compression
- Example: Metrics, logs, sensor data, financial data

### Code Example: Graph Queries

```python
# Wrong: Graph query in PostgreSQL (expensive recursive CTE)
query = """
    WITH RECURSIVE friend_network AS (
        SELECT user_id, friend_id, 1 as depth
        FROM friendships
        WHERE user_id = %s
        UNION
        SELECT f.user_id, f.friend_id, fn.depth + 1
        FROM friendships f
        JOIN friend_network fn ON f.user_id = fn.friend_id
        WHERE fn.depth < 3
    )
    SELECT DISTINCT friend_id FROM friend_network;
"""
# Query time: 5 seconds, scans millions of rows

# Right: Same query in Neo4j (native graph traversal)
query = """
    MATCH (user:User {id: $userId})-[:FRIENDS_WITH*1..3]-(friend)
    RETURN DISTINCT friend.id
"""
# Query time: 0.05 seconds, efficient graph traversal
# 100x faster, 95% less energy
```

### Code Example: Time-Series Data

```python
# Wrong: Time-series data in PostgreSQL
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
# Scans 10M rows, takes 3 seconds

# Right: Same query in TimescaleDB (time-series optimized)
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
# Uses time-based partitioning and compression
# Query time: 0.1 seconds, 30x faster
```

### The Embedded Carbon Impact

Different database types have vastly different resource requirements:

- **Key-Value stores**: 10-100x less CPU than RDBMS for simple lookups
- **Document stores**: 2-5x less CPU than RDBMS for document retrieval
- **Graph databases**: 100-1000x faster than RDBMS for relationship queries
- **Time-series**: 10-30x less storage and CPU than RDBMS

Using PostgreSQL for time-series data:
- 10x more disk space (no time-series compression)
- 30x more CPU cycles (full table scans vs time-based partitions)
- 5x more RAM (inefficient caching)
- **Oversized hardware to compensate = wasted embedded carbon**

### Energy Calculation Example

```python
# Scenario: 1 billion time-series data points, 7-day retention
# Query: Average CPU usage per hour for last 7 days

# Wrong: PostgreSQL (general-purpose RDBMS)
# Storage: 1B rows × 100 bytes = 100 GB uncompressed
# Query: Full table scan, 1B rows, 30 seconds
# Hardware: db.r5.4xlarge (16 vCPU, 128 GB RAM)
# Power: 200W
# Queries: 1000/day
# Energy: 200W × 30s × 1000 queries / 3600 = 1.67 kWh/day
# Annual energy: 609 kWh/year
# Embedded carbon: 2,000 kg CO2e (server manufacturing)

# Right: TimescaleDB (time-series optimized)
# Storage: 1B rows × 20 bytes compressed = 20 GB (5x less)
# Query: Time-based partition scan, 0.1 seconds (300x faster)
# Hardware: db.r5.xlarge (4 vCPU, 32 GB RAM) - 4x smaller
# Power: 50W
# Queries: 1000/day
# Energy: 50W × 0.1s × 1000 queries / 3600 = 0.014 kWh/day
# Annual energy: 5 kWh/year (99% reduction)
# Embedded carbon: 500 kg CO2e (4x smaller server)

# Total savings:
# - Operational energy: 604 kWh/year (99% reduction)
# - Embedded carbon: 1,500 kg CO2e (75% reduction)
# - Hardware cost: 75% reduction
# - Query performance: 300x faster
```

### Polyglot Persistence

Using the right database for each workload minimizes total resource consumption:

```python
# Monolithic approach: Everything in PostgreSQL
# Total hardware: 5x db.r5.4xlarge instances (80 vCPU, 640 GB RAM)
# Total power: 1,000W
# Total embedded carbon: 10,000 kg CO2e

# Polyglot approach: Right database for each workload
# - User accounts: PostgreSQL db.r5.large (2 vCPU, 16 GB)
# - Session data: Redis cache.r5.large (2 vCPU, 13 GB)
# - Product catalog: MongoDB db.r5.large (2 vCPU, 16 GB)
# - Recommendations: Neo4j db.r5.large (2 vCPU, 16 GB)
# - Metrics: InfluxDB db.r5.large (2 vCPU, 16 GB)

# Total hardware: 5x db.r5.large instances (10 vCPU, 77 GB RAM)
# Total power: 250W (75% reduction)
# Total embedded carbon: 2,500 kg CO2e (75% reduction)
# Performance: 10-100x better for specialized workloads
```

### The Tradeoff

Operational complexity (managing multiple databases) vs resource efficiency (right tool for the job).

Sweet spot: 2-4 specialized databases for distinct workload types.

### Impact

- Right database for workload: 10-100x performance improvement
- Energy savings: 50-95% for specialized workloads
- Embedded carbon savings: 50-75% (smaller hardware footprint)
- Storage savings: 5-10x (compression and optimization)
- Operational complexity: +20-50% (multiple systems to manage)


## Cloud vs On-Premises Databases

**Skill Level**: 🟡 Intermediate (Infrastructure Decision)

### The Problem

Cloud databases have overhead (virtualization, network, multi-tenancy). On-prem databases require upfront hardware investment. Wrong choice = paying for unused capacity or running inefficiently.

### The Solution

Understand the energy and cost tradeoffs.

### Cloud Databases (RDS, Aurora, Azure SQL, Cloud SQL)

**Advantages:**
- Pay for what you use (no idle hardware)
- Auto-scaling (right-size automatically)
- Managed services (less operational overhead)
- Geographic distribution (place data near users)
- Carbon-aware regions (choose low-carbon locations)

**Disadvantages:**
- Virtualization overhead (~10-20% performance penalty)
- Network latency (not on same physical hardware as app)
- Multi-tenancy (noisy neighbor problem)

**Energy Profile:**
- Better for variable workloads (scale to zero when idle)
- Worse for consistent high-load (virtualization overhead)
- Can choose low-carbon regions (huge impact)
- Shared infrastructure = better hardware utilization across tenants
- No embedded carbon waste = cloud provider amortizes hardware across many customers

### On-Premises Databases

**Advantages:**
- No virtualization overhead (bare metal performance)
- No network latency (same data center as app)
- Full control over hardware and configuration
- Predictable costs for steady workloads

**Disadvantages:**
- Upfront hardware costs
- Idle capacity waste (can't scale to zero)
- Operational overhead (patching, backups, monitoring)
- Fixed location (can't move to low-carbon regions)
- Embedded carbon in hardware = manufacturing emissions locked in

**Energy Profile:**
- Better for consistent high-load (no virtualization overhead)
- Worse for variable workloads (idle capacity waste)
- Stuck with local grid carbon intensity
- Embedded carbon considerations: Hardware manufacturing = 10-50% of total lifetime carbon
- **Idle capacity = wasted embedded carbon**: If server runs at 20% utilization, 80% of embedded carbon is wasted

### The Embedded Carbon Problem

Manufacturing a server generates significant carbon emissions before it's even powered on:
- Server manufacturing: ~1,000-3,000 kg CO2e per server
- Expected lifetime: 3-5 years
- Amortized embedded carbon: ~200-1,000 kg CO2e per year

If your on-prem database server runs at 30% average utilization:
- Wasted embedded carbon: 70% of manufacturing emissions
- Equivalent to: Running the server for 2+ years with zero workload

Cloud providers achieve 60-80% utilization across their fleet by:
- Multi-tenancy: Multiple customers share same hardware
- Workload diversity: Different usage patterns balance out
- Auto-scaling: Consolidate workloads on fewer servers

### Energy Calculation Example

```python
# On-Prem: Fixed capacity, low utilization
# Hardware: 2x database servers (active + standby)
# Utilization: 30% average
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

# Cloud: Auto-scaling, high utilization
# Same workload, but cloud provider achieves 70% utilization
# Shares hardware with other tenants

# Your share of operational carbon:
operational = 300W × 8760 hours × 30% utilization × 400 gCO2e/kWh / 1000
operational = 315 kg CO2e/year

# Your share of embedded carbon (cloud provider amortizes across tenants):
embedded = 2,000 kg CO2e / 4 years × 30% utilization
embedded = 150 kg CO2e/year

# Total carbon: 465 kg CO2e/year
# Savings: 85% less carbon (3,102 → 465 kg CO2e/year)
```

### Code Example

```python
# Cloud: Auto-scaling based on load
# AWS RDS Aurora Serverless v2
{
    "MinCapacity": 0.5,  # Scale down to 0.5 ACU when idle
    "MaxCapacity": 16,   # Scale up to 16 ACU under load
    "AutoPause": True,   # Pause when no connections
    "SecondsUntilAutoPause": 300
}
# Energy savings: 70-90% for variable workloads
# Scales to near-zero during off-hours

# On-prem: Fixed capacity
# Always running at provisioned capacity
# 24/7 operation even if only used 8 hours/day
# Energy waste: 67% (16 hours idle / 24 hours total)
```

### Decision Matrix

| Workload Pattern | Best Choice | Why |
|------------------|-------------|-----|
| Variable load | Cloud | Auto-scaling, pay for usage |
| Consistent high load | On-prem | No virtualization overhead |
| Development/test | Cloud | Scale to zero when not in use |
| Production 24/7 | Depends | Calculate TCO and energy |
| Multi-region | Cloud | Easy geographic distribution |
| Latency-sensitive | On-prem or cloud same-region | Minimize network hops |
| Low-carbon priority | Cloud | Choose low-carbon regions |

### Hybrid Approach

- Production databases on-prem (consistent load, bare metal performance)
- Dev/test databases in cloud (scale to zero when not in use)
- Analytics databases in cloud (variable load, can use spot instances)
- Disaster recovery in cloud (pay only when needed)

### Impact

- Cloud for variable workloads: 70-90% energy savings (auto-scaling)
- On-prem for consistent load: 10-20% better performance (no virtualization)
- Cloud in low-carbon regions: 10-30x lower carbon emissions
- Hybrid approach: Best of both worlds


## Serverless vs Provisioned Databases

**Skill Level**: 🟡 Intermediate (Architecture Decision)

### The Problem

Provisioned databases run 24/7, even when idle. Serverless databases scale to zero but have cold start overhead. Wrong choice = paying for idle capacity or suffering cold starts.

### The Solution

Match database model to usage patterns.

### Provisioned Databases (RDS, Aurora Provisioned, Azure SQL)

**Characteristics:**
- Always running (24/7)
- Fixed capacity (or manual scaling)
- Predictable performance
- No cold starts

**Energy Profile:**
- Constant energy consumption
- Efficient for consistent load
- Wasteful for sporadic usage

**Best For:**
- Production workloads with consistent traffic
- Latency-sensitive applications
- High-throughput workloads
- 24/7 operations

### Serverless Databases (Aurora Serverless, Azure SQL Serverless, Cosmos DB)

**Characteristics:**
- Scales to zero when idle
- Auto-scales based on load
- Pay per request (not per hour)
- Cold start latency (1-30 seconds)

**Energy Profile:**
- Zero energy when idle
- Scales up/down automatically
- Efficient for variable load

**Best For:**
- Development and testing
- Infrequent workloads (batch jobs, scheduled tasks)
- Variable traffic patterns
- Cost-sensitive applications

### The Embedded Carbon Impact

Provisioned databases run 24/7, regardless of actual usage:
- Fixed capacity: Hardware allocated even when idle
- Embedded carbon locked in: Manufacturing emissions for hardware that sits idle
- Utilization waste: Average database utilization is 20-40% in most organizations

### Embedded Carbon Calculation

```python
# Provisioned database: db.r5.xlarge (4 vCPU, 32 GB RAM)
# Server manufacturing: 1,500 kg CO2e
# Expected lifetime: 4 years
# Amortized embedded carbon: 375 kg CO2e/year

# Scenario 1: Development database
# Usage: 8 hours/day, 5 days/week = 40 hours/week
# Total hours: 168 hours/week
# Utilization: 40/168 = 24%
# Wasted embedded carbon: 76% × 375 kg = 285 kg CO2e/year

# Scenario 2: Production database with variable load
# Peak hours: 8 AM - 8 PM (12 hours/day)
# Off-peak: 8 PM - 8 AM (12 hours/day)
# Average utilization: (60% × 12 + 10% × 12) / 24 = 35%
# Wasted embedded carbon: 65% × 375 kg = 244 kg CO2e/year

# Scenario 3: Batch processing database
# Usage: 2 hours/day for nightly batch jobs
# Utilization: 2/24 = 8%
# Wasted embedded carbon: 92% × 375 kg = 345 kg CO2e/year
```

### Energy and Carbon Comparison

```python
# Development database workload
# Usage: 40 hours/week (24% utilization)
# Queries: 1000/day during work hours

# Provisioned: db.r5.xlarge
# Operational energy: 100W × 168 hours/week = 16.8 kWh/week
# Annual operational: 874 kWh/year
# Operational carbon: 874 kWh × 400 gCO2e/kWh = 350 kg CO2e/year
# Embedded carbon: 375 kg CO2e/year (amortized)
# Wasted embedded: 285 kg CO2e/year (76% idle)
# Total carbon: 725 kg CO2e/year

# Serverless: Aurora Serverless v2
# Operational energy: 100W × 40 hours/week = 4 kWh/week
# Annual operational: 208 kWh/year
# Operational carbon: 208 kWh × 400 gCO2e/kWh = 83 kg CO2e/year
# Embedded carbon share: 375 kg × 24% utilization = 90 kg CO2e/year
# Wasted embedded: 0 kg (scales to zero when idle)
# Total carbon: 173 kg CO2e/year

# Savings: 76% reduction (725 → 173 kg CO2e/year)
```

### The Cold Start Tradeoff

Cold starts add latency but eliminate idle capacity waste:
- Cold start penalty: 1-30 seconds (one-time cost per wake-up)
- Idle capacity elimination: 70-90% energy savings for variable workloads
- Embedded carbon savings: No wasted manufacturing emissions

**When Cold Starts Are Acceptable:**
- Development and testing (latency not critical)
- Batch processing (scheduled jobs, not latency-sensitive)
- Infrequent operations (admin tasks, reports)
- Background processing (async jobs, queues)

**When Cold Starts Are Problematic:**
- User-facing APIs (latency-sensitive)
- Real-time applications (sub-second response requirements)
- High-frequency operations (cold start overhead adds up)

### Mitigation Strategy: Selective Keep-Alive

```python
# Hybrid approach: Keep production warm, let dev/test sleep

# Production: Keep-alive ping every 4 minutes
def keep_database_warm():
    """Ping database every 4 minutes to prevent auto-pause"""
    conn = get_connection()
    conn.execute("SELECT 1")
    conn.close()

# Run every 4 minutes (before 5-minute auto-pause)
schedule.every(4).minutes.do(keep_database_warm)

# Tradeoff: Prevents auto-pause, but keeps database warm
# Use only for production, let dev/test databases pause
```

### Real-World Impact Example

```python
# Company with 50 databases:
# - 10 production (24/7 high utilization) → Provisioned
# - 15 staging (business hours only) → Serverless with conditional keep-alive
# - 25 development (sporadic usage) → Serverless with full auto-pause

# Provisioned approach (all 50 databases):
# Hardware: 50 × db.r5.xlarge
# Operational energy: 50 × 874 kWh/year = 43,700 kWh/year
# Embedded carbon: 50 × 375 kg = 18,750 kg CO2e/year
# Wasted embedded: 40 databases × 285 kg = 11,400 kg CO2e/year (61% waste)
# Total carbon: 18,750 kg + (43,700 × 0.4) = 36,230 kg CO2e/year

# Hybrid approach (10 provisioned + 40 serverless):
# Production (provisioned): 10 × 874 kWh = 8,740 kWh/year
# Staging (serverless 50% usage): 15 × 437 kWh = 6,555 kWh/year
# Development (serverless 24% usage): 25 × 208 kWh = 5,200 kWh/year
# Total operational: 20,495 kWh/year (53% reduction)
# Embedded carbon: 10 × 375 kg + 40 × 90 kg = 7,350 kg CO2e/year (61% reduction)
# Wasted embedded: 0 kg (serverless scales to zero)
# Total carbon: 7,350 kg + (20,495 × 0.4) = 15,548 kg CO2e/year

# Savings: 57% reduction (36,230 → 15,548 kg CO2e/year)
# Annual cost savings: $180,000 → $65,000 (64% reduction)
```

### Decision Framework

| Factor | Provisioned | Serverless |
|--------|-------------|------------|
| Utilization | >60% | <40% |
| Traffic pattern | Consistent | Variable |
| Latency requirement | <100ms | >1s acceptable |
| Workload type | Production 24/7 | Dev/test/batch |
| Cost priority | Predictable | Minimize |
| Carbon priority | Performance | Efficiency |
| Embedded carbon waste | High (idle capacity) | Low (scales to zero) |

### Impact

- Serverless for variable workloads: 50-90% energy savings
- Serverless for dev/test: 70-90% cost reduction
- Embedded carbon waste elimination: 100% (no idle capacity)
- Provisioned for production: Predictable performance, no cold starts
- Hybrid approach: 50-60% total carbon reduction across database fleet


## Real-World Case Study

**Scenario**: E-commerce platform, 100K orders/day, PostgreSQL database

### Problems Found (via profiling)

1. No index on orders.customer_id (Pattern 1)
2. N+1 queries loading order items (Pattern 4)
3. SELECT * fetching unused columns (Pattern 5)
4. OFFSET pagination on order history (Pattern 7)
5. No connection pooling (Pattern 2)

### Changes Made

1. Added composite indexes on frequently queried columns
2. Implemented batch loading with single query
3. Selected only needed columns
4. Switched to cursor-based pagination
5. Configured HikariCP connection pool

### Results

- Query time: 200ms → 15ms average (13x faster)
- Database CPU: 80% → 25% utilization
- RDS instance: db.r5.4xlarge → db.r5.xlarge (4x smaller)
- Monthly cost: $8,000 → $2,000 (75% reduction)
- Carbon emissions: -75% (proportional to compute reduction)
- Response time: 300ms → 50ms (6x faster)

**Timeline**: 1 week of profiling and implementation. Immediate impact after deployment.

**Tradeoffs**: Added Redis for caching (operational complexity), more complex pagination logic (development time). Worth it for 75% cost reduction and 6x performance improvement.

## The Tradeoffs

Nothing is free. Every optimization has tradeoffs.

**Indexes**: Use memory and slow down writes. But speed up reads dramatically. Profile to find the right balance.

**Caching**: Adds complexity (cache invalidation, consistency). But eliminates repeated work. Start with high TTL for rarely-changing data.

**Materialized Views**: Stale data between refreshes. But perfect for analytics and dashboards where real-time isn't critical.

**Connection Pooling**: Requires tuning (too few = queuing, too many = waste). But eliminates connection overhead.

**Denormalization**: Violates normal forms, creates data duplication. But can eliminate expensive JOINs. Use sparingly for read-heavy workloads.

**Polyglot Persistence**: Operational complexity (multiple databases to manage). But massive resource savings (right tool for the job).

**Serverless**: Cold start latency. But eliminates idle capacity waste and embedded carbon.

The key: measure, understand the tradeoff, optimize where it matters. Don't optimize everything. Optimize the hot paths.

## Measuring Impact

### Tools for Database Profiling

**PostgreSQL:**
- pg_stat_statements (query statistics)
- EXPLAIN ANALYZE (query execution plans)
- pg_stat_user_tables (table statistics)
- pgBadger (log analyzer)

**MySQL:**
- Slow query log
- EXPLAIN (query execution plans)
- Performance Schema
- mysqldumpslow (log analyzer)

**MongoDB:**
- Database Profiler
- explain() (query execution plans)
- $indexStats (index usage)
- MongoDB Compass (GUI profiler)

**General:**
- Datadog, New Relic, CloudWatch RDS Insights
- Database monitoring tools

### Metrics That Matter

- Query execution time
- Rows scanned vs rows returned (scan efficiency)
- Index usage statistics
- Connection pool utilization
- Cache hit rates
- Disk I/O operations
- CPU usage per query type

### Energy Measurement

- Cloud provider database metrics (RDS, Aurora, etc.)
- Correlate query patterns with CPU/memory usage
- Track database costs as proxy for energy consumption
- Monitor instance size changes (smaller = less energy)

## What's Next

Database optimization is foundational, but it's just one piece. In the next article, we'll look at building carbon-aware applications—systems that respond to real-time carbon intensity data, shift workloads to cleaner regions, and schedule compute during low-carbon hours.

For now, pick one pattern from this article. Profile your slowest queries. Apply the pattern. Measure the impact. I guarantee you'll find something worth optimizing.

## Key Takeaways

1. **The database is often your biggest energy consumer** - optimize here first
2. **Indexes are your best friend** - but only index what you query
3. **Connection pooling is non-negotiable** - eliminate connection overhead
4. **Cache query results** - compute once, read many times
5. **Batch operations** - eliminate N+1 queries
6. **Select only what you need** - avoid SELECT *
7. **Optimize JOINs** - filter early, join late
8. **Use cursor-based pagination** - OFFSET is a trap
9. **Aggregate in the database** - don't fetch and process in code
10. **Materialized views for complex queries** - pre-compute expensive aggregations
11. **Choose the right database for the job** - RDBMS, NoSQL, Graph, Time-Series
12. **Cloud vs on-prem tradeoffs** - auto-scaling vs bare metal performance
13. **Serverless vs provisioned** - scale to zero vs predictable performance
14. **Measure everything** - you can't optimize what you don't measure
15. **Idle capacity = wasted embedded carbon** - manufacturing emissions locked in unused hardware

## Resources

**Profiling Tools:**
- PostgreSQL: pg_stat_statements, pgBadger, EXPLAIN ANALYZE
- MySQL: Slow Query Log, mysqldumpslow, EXPLAIN
- MongoDB: Database Profiler, explain(), Compass
- General: Datadog, New Relic, CloudWatch RDS Insights

**Connection Pooling:**
- Java: HikariCP (https://github.com/brettwooldridge/HikariCP)
- Python: SQLAlchemy (https://www.sqlalchemy.org/)
- Node.js: pg-pool (https://node-postgres.com/)
- Go: database/sql (built-in)

**Caching:**
- Redis: https://redis.io/
- Memcached: https://memcached.org/
- Database query caches (built-in)

**Books:**
- "High Performance MySQL" by Baron Schwartz
- "PostgreSQL: Up and Running" by Regina Obe
- "Designing Data-Intensive Applications" by Martin Kleppmann

**Previous Articles:**
- [Why Your Code's Carbon Footprint Matters](#)
- [Energy-Efficient Algorithm Patterns](#)

**Coming Up**: Building Carbon-Aware Applications

---

*This is Part 3 of the Green Coding Series. If you found this useful, follow for more articles on sustainable software development.*
