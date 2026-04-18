# Energy-Efficient Algorithm Patterns Every Developer Should Know

*Part 2 of my series on [Sustainable Software Engineering](https://medium.com/@diverdan326/why-your-codes-carbon-footprint-matters-and-how-to-measure-it-9b51b1c418ab). Last time we covered why your code's carbon footprint matters. This time: the specific algorithm patterns that actually move the needle. Follow along for more deep dives into green coding practices.*

---

There's a production service I worked on that was burning through $100K a year in cloud costs. The code looked fine in review—it had a caching layer, proper permission checks, even used database views for "optimization." The problem wasn't obvious until we hit scale.

The permission system checked user access by querying a database view that joined three tables. "It's cached!" the original developer said. True—but the cache key was just the user ID. Every API endpoint checked different permissions. Cache hit rate: 12%. The database was getting hammered with 50,000 queries per second, each doing a three-table join.

We added a Bloom filter as a negative cache. 99.9% of requests were for permissions users *didn't* have. The Bloom filter answered those in microseconds with zero database load. For the remaining 0.1%, we restructured the cache to include permission type in the key. Cache hit rate jumped to 94%. Database queries dropped from 50,000/sec to 3,000/sec.

CPU usage dropped 60%. Database load dropped 75%. Energy consumption dropped proportionally. Same functionality, fraction of the cost.

This isn't about micro-optimizations. This is about patterns that matter at scale.

## Why Algorithm Efficiency = Energy Efficiency

Every CPU cycle consumes energy. At small scale, it doesn't matter. At large scale, algorithmic complexity dominates everything else—language choice, hardware efficiency, all of it.

Here's the math: A typical server CPU consumes about 0.5 watts per core under load. If your algorithm does 1 million unnecessary operations per second, that's continuous CPU load. Over a day, that's 43 kWh. Over a year, that's 15,700 kWh. At typical data center carbon intensity (400 gCO2e/kWh), that's 6.3 tons of CO2 per year. From one inefficient algorithm.

The algorithm you choose has more impact than the language you write it in. A well-written Python service with O(n log n) algorithms will use less energy than a poorly-written C++ service with O(n²) algorithms.

There's actual physics behind this. Landauer's Principle states that erasing information requires a minimum amount of energy—about 3×10⁻²¹ joules per bit at room temperature. When your algorithm destroys information (overwrites variables, discards intermediate results), it dissipates energy. More operations = more information destruction = more energy. MIT researchers have formalized this into energy complexity models for algorithms, but you don't need to understand the physics to apply the patterns.

The practical takeaway: algorithmic complexity directly translates to energy consumption. O(n²) doesn't just mean slower—it means exponentially more energy at scale.

Let's look at patterns that actually matter.

## Pattern 1: Replace Linear Search with Hash-Based Lookup

**Skill Level**: 🟢 **Basic** (No-brainer optimization)

**The Problem**: You're checking if an item exists in a collection. You're using a List or Array and iterating through it. Every check is O(n). You're doing this thousands of times per second.

Real example: User permission checking. Every API call checks if the user has permission. The permission list has 1,000 items. You're doing 10,000 requests per second. That's 10 million iterations per second. Completely unnecessary.

**The Solution**: Use a HashMap, HashSet, or Dictionary. Lookups are O(1). Same functionality, constant time instead of linear time.

**Python Example with Timing**:

```python
import time

# Before: O(n) lookup - iterates through entire list
allowed_users = ["user1", "user2", "user3", ..., "user1000"]  # 1000 items

def check_permission_slow(user_id):
    return user_id in allowed_users  # O(n) - checks each item

# After: O(1) lookup - hash table lookup
allowed_users_set = {"user1", "user2", "user3", ..., "user1000"}  # Set

def check_permission_fast(user_id):
    return user_id in allowed_users_set  # O(1) - hash lookup

# Measure the difference
start = time.perf_counter()
for _ in range(10000):
    check_permission_slow("user999")  # Near end of list
slow_time = time.perf_counter() - start

start = time.perf_counter()
for _ in range(10000):
    check_permission_fast("user999")
fast_time = time.perf_counter() - start

print(f"List lookup: {slow_time:.4f}s")  # ~0.5s
print(f"Set lookup: {fast_time:.4f}s")   # ~0.001s
print(f"Speedup: {slow_time/fast_time:.0f}x")  # ~500x
```

**Java Example**:

```java
// Before: O(n) lookup with ArrayList
List<String> allowedUsers = new ArrayList<>(Arrays.asList(
    "user1", "user2", ..., "user1000"
));

public boolean checkPermissionSlow(String userId) {
    return allowedUsers.contains(userId);  // O(n)
}

// After: O(1) lookup with HashSet
Set<String> allowedUsersSet = new HashSet<>(Arrays.asList(
    "user1", "user2", ..., "user1000"
));

public boolean checkPermissionFast(String userId) {
    return allowedUsersSet.contains(userId);  // O(1)
}
```

**Impact**:

- For 100-item collection: 100x faster
- For 1,000-item collection: 1,000x faster
- At 10K requests/sec: CPU usage drops 40-60%
- Energy savings: ~50 kWh/day for typical service
- Cost savings: ~$500/month in cloud costs

**When to Use**: Any time you're doing repeated membership testing. Permission checks, validation against allowed values, duplicate detection, filtering.

## Pattern 2: Batch Operations Instead of Individual Calls

**Skill Level**: 🟢 **Basic** (No-brainer optimization)

**The Problem**: You're making N database queries in a loop. Or N API calls when one would work. Or processing items one at a time when you could batch them.

Every database query has overhead: network round-trip, connection setup, query parsing, result serialization. If you're doing 1,000 queries, you're paying that overhead 1,000 times.

**The Solution**: Batch your operations. One query with 1,000 IDs instead of 1,000 queries with one ID each.

**Python Example with Real Database**:

```python
import psycopg2
import time

# Before: N queries - one per user
def get_users_slow(user_ids):
    conn = psycopg2.connect("dbname=mydb")
    cursor = conn.cursor()
    users = []
  
    start = time.time()
    for user_id in user_ids:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        users.append(user)
    elapsed = time.time() - start
  
    conn.close()
    print(f"Individual queries: {elapsed:.2f}s for {len(user_ids)} users")
    return users

# After: 1 query - batch all users
def get_users_fast(user_ids):
    conn = psycopg2.connect("dbname=mydb")
    cursor = conn.cursor()
  
    start = time.time()
    cursor.execute(
        "SELECT * FROM users WHERE id = ANY(%s)", 
        (user_ids,)
    )
    users = cursor.fetchall()
    elapsed = time.time() - start
  
    conn.close()
    print(f"Batched query: {elapsed:.2f}s for {len(user_ids)} users")
    return users

# Test with 100 user IDs
user_ids = list(range(1, 101))
get_users_slow(user_ids)  # ~2.5s (25ms per query)
get_users_fast(user_ids)  # ~0.03s (single query)
# 83x faster!
```

**Node.js/TypeScript Example**:

```typescript
// Before: N queries
async function getUsersSlow(userIds: number[]): Promise<User[]> {
    const users: User[] = [];
    for (const userId of userIds) {
        const user = await db.query(
            'SELECT * FROM users WHERE id = $1',
            [userId]
        );
        users.push(user.rows[0]);
    }
    return users;
}

// After: 1 batched query
async function getUsersFast(userIds: number[]): Promise<User[]> {
    const result = await db.query(
        'SELECT * FROM users WHERE id = ANY($1)',
        [userIds]
    );
    return result.rows;
}
```

**Impact**:

- Reduces database connections by 100x
- Eliminates network round-trip overhead (typically 1-5ms per query)
- At 1,000 items: 99% reduction in query overhead
- Database CPU usage drops 70-80%
- Energy savings: Proportional to reduction in queries

**Real Example**: An e-commerce service was loading product details for shopping carts. Each cart had 10-20 items. They were making 10-20 database queries per cart view. Changed to one batched query. Response time dropped from 200ms to 30ms. Database load dropped 85%.

**When to Use**: Any time you're doing repeated I/O operations. Database queries, API calls, file reads, cache lookups.

## Pattern 3: Cache Expensive Computations

**Skill Level**: 🟡 **Intermediate** (Requires cache strategy understanding)

**The Problem**: You're computing the same result over and over. Maybe it's an expensive calculation—cryptographic operations, ML inference, complex database queries. Maybe it's just called frequently. Either way, you're doing unnecessary work.

**The Solution**: Cache it. Compute once, reuse many times.

**Python Example with Metrics**:

```python
import time
from functools import lru_cache
import hashlib

# Simulate expensive computation
def expensive_computation(data):
    time.sleep(0.1)  # Simulates 100ms of work
    return hashlib.sha256(data.encode()).hexdigest()

# Before: Recompute every time
def get_user_hash_slow(user_id):
    user_data = f"user_{user_id}_data"
    return expensive_computation(user_data)

# After: Cache with LRU
@lru_cache(maxsize=1000)
def get_user_hash_fast(user_id):
    user_data = f"user_{user_id}_data"
    return expensive_computation(user_data)

# Measure impact
user_ids = [1, 2, 3, 1, 2, 3, 1, 2, 3] * 100  # Repeated IDs

start = time.time()
for uid in user_ids:
    get_user_hash_slow(uid)
slow_time = time.time() - start
print(f"Without cache: {slow_time:.2f}s")  # ~90s (900 calls × 100ms)

start = time.time()
for uid in user_ids:
    get_user_hash_fast(uid)
fast_time = time.time() - start
print(f"With cache: {fast_time:.2f}s")  # ~0.3s (3 unique × 100ms)

print(f"Speedup: {slow_time/fast_time:.0f}x")  # ~300x
print(f"Cache hit rate: {(1 - 3/900) * 100:.1f}%")  # 99.7%
```

**Redis Caching Example**:

```python
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379)

# Before: Always compute
def get_user_recommendations_slow(user_id):
    user_features = extract_features(user_id)  # 50ms
    recommendations = ml_model.predict(user_features)  # 100ms
    return recommendations

# After: Cache in Redis for 1 hour
def get_user_recommendations_fast(user_id):
    cache_key = f"recommendations:{user_id}"
  
    # Try cache first
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
  
    # Cache miss - compute and store
    user_features = extract_features(user_id)
    recommendations = ml_model.predict(user_features)
  
    redis_client.setex(
        cache_key,
        3600,  # 1 hour TTL
        json.dumps(recommendations)
    )
    return recommendations
```

**Impact**:

- 90%+ cache hit rate = 90% less computation
- ML inference: 100ms → 1ms response time
- Energy savings: Directly proportional to cache hit rate
- Real example: 95% cache hit rate = 20x reduction in compute

**Tradeoff**: Caching uses memory. A 10,000-item cache might use 100MB-1GB depending on object size. But memory is cheap compared to CPU. And you're trading memory (static cost) for CPU (per-request cost).

**When to Use**:

- Expensive operations (ML inference, complex calculations, heavy queries)
- Repeated inputs (user profiles, product details, configuration)
- Acceptable staleness (data doesn't need to be real-time)

**Cache Strategies**:

- **In-memory**: Fast, but lost on restart (LRU cache, application cache)
- **Distributed**: Shared across instances (Redis, Memcached)
- **CDN**: For static content (CloudFront, Cloudflare)
- **Database**: Computed columns, materialized views

## Pattern 4: Use Lazy Evaluation and Streaming

**Skill Level**: 🟡 **Intermediate** (Requires understanding of generators and memory management)

**The Problem**: You're loading an entire dataset into memory. Processing all of it. Then returning a small subset. You're doing way more work than necessary.

**The Solution**: Stream the data. Process one item at a time. Stop when you have what you need. Don't materialize intermediate results unless you have to.

**Python Example with Memory Profiling**:

```python
import sys

# Before: Load everything into memory
def get_active_users_slow():
    # Simulates loading 1M user records
    users = [{"id": i, "is_active": i % 2 == 0} for i in range(1_000_000)]
    print(f"Memory used: {sys.getsizeof(users) / 1024 / 1024:.1f} MB")
  
    active_users = [u for u in users if u["is_active"]]
    return active_users[:10]

# After: Stream and limit
def get_active_users_fast():
    # Generator - yields one at a time
    def user_generator():
        for i in range(1_000_000):
            if i % 2 == 0:  # is_active
                yield {"id": i, "is_active": True}
  
    # Take first 10
    result = []
    for user in user_generator():
        result.append(user)
        if len(result) >= 10:
            break
  
    print(f"Memory used: {sys.getsizeof(result) / 1024:.1f} KB")
    return result

get_active_users_slow()  # Memory: ~85 MB
get_active_users_fast()  # Memory: ~1 KB
# 85,000x less memory!
```

**Database Streaming Example**:

```python
# Before: Load all rows into memory
def process_large_table_slow():
    conn = psycopg2.connect("dbname=mydb")
    cursor = conn.cursor()
  
    # Loads ALL rows into memory
    cursor.execute("SELECT * FROM large_table")  # 10M rows
    rows = cursor.fetchall()  # ~10GB in memory
  
    for row in rows:
        if should_process(row):
            process_row(row)
  
    conn.close()

# After: Stream with cursor
def process_large_table_fast():
    conn = psycopg2.connect("dbname=mydb")
    cursor = conn.cursor(name='streaming_cursor')  # Server-side cursor
  
    # Streams rows one at a time
    cursor.execute("SELECT * FROM large_table")
  
    for row in cursor:  # Fetches in batches of 2000
        if should_process(row):
            process_row(row)
  
    conn.close()
```

**File Processing Example**:

```python
# Before: Load entire file
def process_log_file_slow(filename):
    with open(filename) as f:
        lines = f.readlines()  # Loads entire file (10GB)
  
    errors = [line for line in lines if 'ERROR' in line]
    return errors

# After: Stream line by line
def process_log_file_fast(filename):
    errors = []
    with open(filename) as f:
        for line in f:  # Reads one line at a time
            if 'ERROR' in line:
                errors.append(line)
    return errors
```

**Impact**:

- Memory usage: 1GB → 10MB (100x reduction)
- CPU usage: Process 1M rows → Process 10 rows (100,000x reduction)
- Network transfer: 1M rows → 10 rows
- Energy savings: 100x reduction in work done

**When to Use**:

- Large datasets (millions of rows)
- ETL pipelines
- Log processing
- Data transformations
- Any time you don't need all the data at once

## Pattern 5: Choose the Right Data Structure

**Skill Level**: 🟡 **Intermediate** (Requires understanding of data structure tradeoffs)

**The Problem**: You're using the wrong data structure for the operation. Array when you need fast insertion. Linked list when you need random access. Unsorted data when you need range queries.

Data structure choice determines algorithmic complexity. Wrong choice means O(n) or O(n²) when you could have O(1) or O(log n).

**Data Structure Cheat Sheet**:

| Operation               | Best Structure  | Complexity |
| ----------------------- | --------------- | ---------- |
| Lookup by key           | HashMap         | O(1)       |
| Membership test         | HashSet         | O(1)       |
| Maintain order          | TreeMap/TreeSet | O(log n)   |
| Range queries           | TreeMap         | O(log n)   |
| Fast insertion (end)    | ArrayList       | O(1)       |
| Fast insertion (middle) | LinkedList      | O(1)       |
| Priority queue          | Heap            | O(log n)   |
| Approximate membership  | Bloom Filter    | O(1)       |

**Real-World Example with Timing**:

```python
import time

# Before: Checking duplicates with List - O(n²)
def deduplicate_slow(items):
    seen = []
    unique = []
  
    start = time.time()
    for item in items:
        if item not in seen:  # O(n) check
            seen.append(item)  # O(1) append
            unique.append(item)
    elapsed = time.time() - start
  
    print(f"List-based: {elapsed:.4f}s")
    return unique

# After: Checking duplicates with Set - O(n)
def deduplicate_fast(items):
    seen = set()
    unique = []
  
    start = time.time()
    for item in items:
        if item not in seen:  # O(1) check
            seen.add(item)  # O(1) add
            unique.append(item)
    elapsed = time.time() - start
  
    print(f"Set-based: {elapsed:.4f}s")
    return unique

# Test with 10,000 items (50% duplicates)
test_data = list(range(5000)) * 2
import random
random.shuffle(test_data)

deduplicate_slow(test_data)  # ~2.5s (O(n²))
deduplicate_fast(test_data)  # ~0.002s (O(n))
# 1,250x faster!
```

**Priority Queue Example**:

```python
import heapq
import time

# Before: Finding top K items with sorting - O(n log n)
def get_top_k_slow(items, k):
    start = time.time()
    sorted_items = sorted(items, reverse=True)  # O(n log n)
    result = sorted_items[:k]
    elapsed = time.time() - start
    print(f"Sorting approach: {elapsed:.4f}s")
    return result

# After: Using heap - O(n log k)
def get_top_k_fast(items, k):
    start = time.time()
    result = heapq.nlargest(k, items)  # O(n log k)
    elapsed = time.time() - start
    print(f"Heap approach: {elapsed:.4f}s")
    return result

# Test with 1M items, finding top 10
test_data = list(range(1_000_000))
random.shuffle(test_data)

get_top_k_slow(test_data, 10)  # ~0.15s
get_top_k_fast(test_data, 10)  # ~0.08s
# 2x faster, and scales better as n grows
```

**Impact**:

- At 10,000 items: 10,000x fewer operations (O(n²) → O(n))
- CPU usage: 99% reduction
- Energy savings: Proportional to CPU reduction

**When to Use**: Always. Data structure choice is fundamental. Profile your code, identify hot paths, check if you're using the right structure.

## Pattern 6: Avoid Premature Materialization

**Skill Level**: 🟡 **Intermediate** (Requires understanding of data transformation pipelines)

**The Problem**: You're converting data formats unnecessarily. Serializing and deserializing multiple times. Creating intermediate objects that aren't needed. Every conversion costs CPU and memory.

**The Solution**: Keep data in its most efficient format as long as possible. Avoid unnecessary conversions. Use views instead of copies. Stream transformations instead of materializing.

**Python Example with Profiling**:

```python
import json
import pandas as pd
import time

# Before: Multiple conversions
def process_api_response_slow(response_text):
    start = time.time()
  
    # Conversion 1: string → dict
    data = json.loads(response_text)
  
    # Conversion 2: dict → DataFrame
    df = pd.DataFrame(data)
  
    # Conversion 3: DataFrame → dict
    result = df.to_dict('records')
  
    elapsed = time.time() - start
    print(f"Multiple conversions: {elapsed:.4f}s")
    return result

# After: Direct conversion
def process_api_response_fast(response_text):
    start = time.time()
  
    # One conversion: string → dict
    result = json.loads(response_text)
  
    elapsed = time.time() - start
    print(f"Direct conversion: {elapsed:.4f}s")
    return result

# Test with 10,000 records
test_data = json.dumps([{"id": i, "value": i*2} for i in range(10000)])

process_api_response_slow(test_data)  # ~0.15s
process_api_response_fast(test_data)  # ~0.01s
# 15x faster!
```

**Generator Pipeline Example**:

```python
# Before: Creating intermediate copies
def filter_and_transform_slow(data):
    # Copy 1: Filter
    filtered = [x for x in data if x > 0]
  
    # Copy 2: Square
    squared = [x**2 for x in filtered]
  
    # Copy 3: Filter again
    result = [x for x in squared if x < 1000]
  
    return result

# After: Generator pipeline (no intermediate copies)
def filter_and_transform_fast(data):
    # Lazy evaluation - no intermediate lists
    return [x**2 for x in data if x > 0 and x**2 < 1000]

# Or with explicit generator for clarity
def filter_and_transform_generator(data):
    return (x**2 for x in data if x > 0 and x**2 < 1000)
```

**Impact**:

- Eliminates 3 unnecessary conversions
- Reduces memory allocations by 75%
- Energy savings: 30-50% for data-heavy pipelines

**When to Use**: Data pipelines, ETL processes, API integrations, any time you're transforming data through multiple steps.

## Pattern 7: Parallelize Wisely (Not Always)

**Skill Level**: 🔴 **Advanced** (Requires understanding of concurrency, overhead, and profiling)

**The Problem**: You assume parallel is always faster and more efficient. It's not. Parallelization has overhead: thread/process creation, context switching, synchronization. Sometimes sequential is more efficient.

**When Parallel Helps**:

- CPU-intensive tasks (image processing, ML training, video encoding)
- Independent operations (no shared state, no synchronization)
- Large enough workload to justify overhead (seconds, not milliseconds)

**When Sequential is Better**:

- I/O-bound tasks (already waiting on network/disk, parallelism doesn't help)
- Small tasks (overhead dominates actual work)
- Shared state requiring locks (synchronization overhead kills performance)

**CPU-Bound Example (Parallel Wins)**:

```python
from multiprocessing import Pool
import time

def cpu_intensive_task(n):
    # Simulate CPU-heavy work
    result = 0
    for i in range(n):
        result += i ** 2
    return result

# Sequential
def process_sequential(tasks):
    start = time.time()
    results = [cpu_intensive_task(t) for t in tasks]
    elapsed = time.time() - start
    print(f"Sequential: {elapsed:.2f}s")
    return results

# Parallel
def process_parallel(tasks):
    start = time.time()
    with Pool(processes=8) as pool:
        results = pool.map(cpu_intensive_task, tasks)
    elapsed = time.time() - start
    print(f"Parallel: {elapsed:.2f}s")
    return results

tasks = [1_000_000] * 16
process_sequential(tasks)  # ~8.5s
process_parallel(tasks)    # ~1.2s
# 7x faster with 8 cores!
```

**I/O-Bound Example (Async Wins, Not Parallel)**:

```python
import asyncio
import aiohttp
import requests
import time

# Sequential (slow)
def fetch_urls_sequential(urls):
    start = time.time()
    results = []
    for url in urls:
        response = requests.get(url)
        results.append(response.json())
    elapsed = time.time() - start
    print(f"Sequential: {elapsed:.2f}s")
    return results

# Async (fast)
async def fetch_urls_async(urls):
    start = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    elapsed = time.time() - start
    print(f"Async: {elapsed:.2f}s")
    return results

async def fetch_one(session, url):
    async with session.get(url) as response:
        return await response.json()

urls = ["https://api.example.com/data"] * 20
fetch_urls_sequential(urls)  # ~10s (20 × 500ms)
asyncio.run(fetch_urls_async(urls))  # ~0.5s (parallel I/O)
# 20x faster!
```

**Impact**:

- Right choice: 2-8x speedup, proportional energy savings
- Wrong choice: Slower + more energy due to overhead

**When to Use**: Profile first. If you're CPU-bound and tasks are independent, parallelize. If you're I/O-bound, use async. If tasks are small or require synchronization, stay sequential.

## Pattern 8: Use Probabilistic Data Structures

**Skill Level**: 🔴 **Advanced** (Requires understanding of probabilistic algorithms and tradeoffs)

**The Problem**: You need to check membership in a massive set (billions of items), but exact accuracy isn't critical. Traditional hash sets would consume terabytes of memory. Or you need to count distinct items in a stream without storing everything.

**The Solution**: Use probabilistic data structures. They trade perfect accuracy for massive space savings. Bloom filters for membership testing, HyperLogLog for cardinality estimation, Count-Min Sketch for frequency counting.

**Bloom Filter Example (Python)**:

```python
from pybloom_live import BloomFilter
import time

# Real-world scenario: URL deduplication in web crawler
# 100M URLs, need to check if we've seen them before

# Before: HashSet - exact but memory-intensive
def check_url_visited_exact(url, visited_urls):
    return url in visited_urls  # 100M URLs = ~8GB memory

visited_exact = set()  # Will grow to 8GB for 100M URLs

# After: Bloom Filter - probabilistic but space-efficient
def check_url_visited_bloom(url, bloom):
    return url in bloom  # 100M URLs = ~120MB memory (1% false positive rate)

# Create Bloom filter for 100M items with 1% false positive rate
bloom = BloomFilter(capacity=100_000_000, error_rate=0.01)

# Test performance
test_urls = [f"https://example.com/page{i}" for i in range(10000)]

# Add URLs to both structures
start = time.time()
for url in test_urls:
    visited_exact.add(url)
exact_time = time.time() - start

start = time.time()
for url in test_urls:
    bloom.add(url)
bloom_time = time.time() - start

print(f"HashSet add time: {exact_time:.4f}s, Memory: ~8GB for 100M items")
print(f"Bloom filter add time: {bloom_time:.4f}s, Memory: ~120MB for 100M items")
print(f"Space savings: {8000/120:.0f}x less memory")
print(f"Tradeoff: 1% false positive rate (99% accuracy)")
```

**HyperLogLog Example (Cardinality Estimation)**:

```python
from hyperloglog import HyperLogLog
import random

# Real-world: Count unique visitors without storing all IPs
# Traditional approach: Store every IP in a set

# Before: Exact count with Set
def count_unique_visitors_exact(visitor_ips):
    unique_ips = set(visitor_ips)
    return len(unique_ips)
    # 10M unique IPs = ~160MB memory

# After: HyperLogLog - approximate count
def count_unique_visitors_approx(visitor_ips):
    hll = HyperLogLog(0.01)  # 1% error rate
    for ip in visitor_ips:
        hll.add(ip)
    return len(hll)
    # 10M unique IPs = ~12KB memory

# Simulate 10M visitor IPs (with duplicates)
visitor_stream = [f"192.168.{random.randint(0,255)}.{random.randint(0,255)}" 
                  for _ in range(10_000_000)]

# Exact count
start = time.time()
exact_count = count_unique_visitors_exact(visitor_stream)
exact_time = time.time() - start

# HyperLogLog count
start = time.time()
approx_count = count_unique_visitors_approx(visitor_stream)
approx_time = time.time() - start

print(f"Exact count: {exact_count}, Time: {exact_time:.2f}s, Memory: ~160MB")
print(f"HyperLogLog: {approx_count}, Time: {approx_time:.2f}s, Memory: ~12KB")
print(f"Error: {abs(exact_count - approx_count) / exact_count * 100:.2f}%")
print(f"Space savings: {160000/12:.0f}x less memory")
```

**Real-World Use Cases**:

- **Bloom Filters**: Web crawlers (URL deduplication), CDN caching (negative cache), spam filtering, database query optimization
- **HyperLogLog**: Analytics (unique visitors), database cardinality estimation, network traffic analysis
- **Count-Min Sketch**: Heavy hitter detection, frequency analysis, DDoS detection

**Impact**:

- Memory reduction: 100-10,000x less memory
- Speed: Often faster than exact structures (smaller memory footprint = better cache locality)
- Energy savings: Proportional to memory and CPU reduction
- Tradeoff: Small error rate (typically 0.1-2%)

**When to Use**:

- Massive datasets (billions of items)
- Acceptable error rate (analytics, caching, filtering)
- Memory constraints (embedded systems, edge computing)
- Real-time streaming data

**When NOT to Use**:

- Financial transactions (need exact accuracy)
- Security-critical decisions (false positives unacceptable)
- Small datasets (overhead not worth it)

## Pattern 9: Optimize Memory Layout and Access Patterns

**Skill Level**: 🔴 **Advanced** (Requires understanding of CPU cache, memory hierarchy, and data-oriented design)

**The Problem**: Your data structures are cache-unfriendly. You're accessing memory randomly, causing cache misses. You're using arrays of objects (AoS) when you should use structs of arrays (SoA). Every cache miss costs 100-300 CPU cycles and energy.

**The Solution**: Organize data for sequential access. Use cache-friendly data structures. Leverage CPU cache lines (typically 64 bytes). Apply data-oriented design principles.

**Array of Structs vs Struct of Arrays (Python with NumPy)**:

```python
import numpy as np
import time

# Scenario: Processing 10M particles in a physics simulation
# Only need to update positions, not other attributes

# Before: Array of Structs (AoS) - cache-unfriendly
class Particle:
    def __init__(self, x, y, z, vx, vy, vz, mass, charge):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.mass = mass
        self.charge = charge

def update_positions_aos(particles, dt):
    for particle in particles:
        particle.x += particle.vx * dt
        particle.y += particle.vy * dt
        particle.z += particle.vz * dt

# Create 1M particles (AoS)
particles_aos = [Particle(0, 0, 0, 1, 1, 1, 1.0, 1.0) for _ in range(1_000_000)]

start = time.time()
update_positions_aos(particles_aos, 0.01)
aos_time = time.time() - start
print(f"AoS update time: {aos_time:.4f}s")

# After: Struct of Arrays (SoA) - cache-friendly
class ParticlesSoA:
    def __init__(self, count):
        self.x = np.zeros(count, dtype=np.float32)
        self.y = np.zeros(count, dtype=np.float32)
        self.z = np.zeros(count, dtype=np.float32)
        self.vx = np.ones(count, dtype=np.float32)
        self.vy = np.ones(count, dtype=np.float32)
        self.vz = np.ones(count, dtype=np.float32)
        self.mass = np.ones(count, dtype=np.float32)
        self.charge = np.ones(count, dtype=np.float32)

def update_positions_soa(particles, dt):
    particles.x += particles.vx * dt
    particles.y += particles.vy * dt
    particles.z += particles.vz * dt

# Create 1M particles (SoA)
particles_soa = ParticlesSoA(1_000_000)

start = time.time()
update_positions_soa(particles_soa, 0.01)
soa_time = time.time() - start
print(f"SoA update time: {soa_time:.4f}s")
print(f"Speedup: {aos_time/soa_time:.0f}x")

# Why SoA is faster:
# - Sequential memory access (better cache utilization)
# - SIMD vectorization (process multiple items per instruction)
# - No pointer chasing (all data contiguous)
```

**Cache-Friendly Iteration (C++ Example)**:

```cpp
#include <vector>
#include <chrono>
#include <iostream>

// Before: Random access - cache-unfriendly
void process_random_access(std::vector<int>& data, const std::vector<int>& indices) {
    for (int idx : indices) {
        data[idx] = data[idx] * 2 + 1;  // Random memory access
    }
}

// After: Sequential access - cache-friendly
void process_sequential_access(std::vector<int>& data) {
    for (size_t i = 0; i < data.size(); ++i) {
        data[i] = data[i] * 2 + 1;  // Sequential memory access
    }
}

int main() {
    const int SIZE = 10'000'000;
    std::vector<int> data(SIZE, 1);
    std::vector<int> random_indices(SIZE);
  
    // Generate random indices
    for (int i = 0; i < SIZE; ++i) {
        random_indices[i] = rand() % SIZE;
    }
  
    // Random access
    auto start = std::chrono::high_resolution_clock::now();
    process_random_access(data, random_indices);
    auto end = std::chrono::high_resolution_clock::now();
    auto random_time = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
  
    // Sequential access
    start = std::chrono::high_resolution_clock::now();
    process_sequential_access(data);
    end = std::chrono::high_resolution_clock::now();
    auto sequential_time = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
  
    std::cout << "Random access: " << random_time << "ms (many cache misses)" << std::endl;
    std::cout << "Sequential access: " << sequential_time << "ms (cache-friendly)" << std::endl;
    std::cout << "Speedup: " << (random_time / sequential_time) << "x" << std::endl;
  
    return 0;
}
```

**Impact**:

- CPU cache hit rate: 50% → 95%+ (2-10x speedup)
- Memory bandwidth: Better utilization (fewer wasted cache line loads)
- Energy efficiency: Fewer memory accesses = less energy
- SIMD opportunities: Sequential data enables vectorization

**When to Use**:

- High-performance computing (physics simulations, game engines)
- Data processing pipelines (analytics, ETL)
- Real-time systems (low-latency requirements)
- Large datasets (millions of items)

**Key Principles**:

- **Sequential > Random**: Access memory sequentially when possible
- **SoA > AoS**: When processing one field across many items
- **Cache line awareness**: Align hot data to cache line boundaries (64 bytes)
- **Data locality**: Keep related data close in memory

## Pattern 10: Algorithm Selection Based on Input Characteristics

**Skill Level**: 🔴 **Advanced** (Requires deep algorithmic knowledge and adaptive optimization)

**The Problem**: You're using the same algorithm regardless of input characteristics. Quicksort for nearly-sorted data. Binary search on small arrays. Hash table for 5 items. The "best" algorithm depends on the data.

**The Solution**: Adaptively select algorithms based on input size, distribution, and characteristics. Use hybrid approaches that switch strategies based on runtime analysis.

**Adaptive Sorting Example (Python)**:

```python
import time
import random

def insertion_sort(arr):
    """O(n²) but fast for small/nearly-sorted arrays"""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def quicksort(arr):
    """O(n log n) average, good for random data"""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

def timsort_wrapper(arr):
    """O(n log n) worst case, optimized for real-world data"""
    return sorted(arr)  # Python's built-in uses Timsort

def adaptive_sort(arr):
    """Selects algorithm based on input characteristics"""
    n = len(arr)
  
    # Small arrays: insertion sort (low overhead)
    if n < 20:
        return insertion_sort(arr.copy())
  
    # Check if nearly sorted (measure inversions in sample)
    sample_size = min(100, n)
    sample = arr[:sample_size]
    inversions = sum(1 for i in range(len(sample)-1) if sample[i] > sample[i+1])
    sortedness = 1 - (inversions / (sample_size - 1))
  
    # Nearly sorted: insertion sort or Timsort
    if sortedness > 0.9:
        if n < 1000:
            return insertion_sort(arr.copy())
        else:
            return timsort_wrapper(arr.copy())
  
    # Random data: quicksort or Timsort
    if n < 10000:
        return quicksort(arr.copy())
    else:
        return timsort_wrapper(arr.copy())

# Test with different input characteristics
test_cases = {
    "Small random": random.sample(range(1000), 15),
    "Nearly sorted": list(range(1000)) + [999, 998],
    "Large random": random.sample(range(100000), 10000),
    "Reverse sorted": list(range(1000, 0, -1)),
}

for name, data in test_cases.items():
    # Adaptive sort
    start = time.time()
    adaptive_sort(data)
    adaptive_time = time.time() - start
  
    # Always quicksort
    start = time.time()
    quicksort(data.copy())
    quicksort_time = time.time() - start
  
    # Always Timsort
    start = time.time()
    timsort_wrapper(data.copy())
    timsort_time = time.time() - start
  
    print(f"\n{name} (n={len(data)}):")
    print(f"  Adaptive: {adaptive_time*1000:.2f}ms")
    print(f"  Quicksort: {quicksort_time*1000:.2f}ms")
    print(f"  Timsort: {timsort_time*1000:.2f}ms")
    print(f"  Best choice: {min(adaptive_time, quicksort_time, timsort_time)*1000:.2f}ms")
```

**Adaptive Search Example**:

```python
def linear_search(arr, target):
    """O(n) - best for small arrays"""
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

def binary_search(arr, target):
    """O(log n) - best for large sorted arrays"""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def adaptive_search(arr, target):
    """Selects search algorithm based on array size"""
    # For small arrays, linear search is faster (no branch mispredictions)
    if len(arr) < 32:
        return linear_search(arr, target)
    else:
        return binary_search(arr, target)

# Benchmark
for size in [10, 50, 100, 1000, 10000]:
    arr = list(range(size))
    target = size - 1  # Worst case for linear search
  
    start = time.perf_counter()
    for _ in range(1000):
        linear_search(arr, target)
    linear_time = time.perf_counter() - start
  
    start = time.perf_counter()
    for _ in range(1000):
        binary_search(arr, target)
    binary_time = time.perf_counter() - start
  
    start = time.perf_counter()
    for _ in range(1000):
        adaptive_search(arr, target)
    adaptive_time = time.perf_counter() - start
  
    print(f"Size {size}: Linear={linear_time*1000:.2f}ms, "
          f"Binary={binary_time*1000:.2f}ms, "
          f"Adaptive={adaptive_time*1000:.2f}ms")
```

**Real-World Example: Database Query Optimization**:

```python
class QueryOptimizer:
    """Adaptively selects query execution strategy"""
  
    def execute_query(self, table, predicate, estimated_selectivity):
        """
        Selects execution strategy based on data characteristics
      
        estimated_selectivity: fraction of rows matching predicate (0.0 to 1.0)
        """
        row_count = len(table)
      
        # Very selective (< 1%): Index scan
        if estimated_selectivity < 0.01:
            return self.index_scan(table, predicate)
      
        # Moderately selective (1-20%): Index scan with prefetch
        elif estimated_selectivity < 0.20:
            return self.index_scan_with_prefetch(table, predicate)
      
        # Not selective (> 20%): Full table scan (index overhead not worth it)
        else:
            return self.full_table_scan(table, predicate)
  
    def index_scan(self, table, predicate):
        """Use index for highly selective queries"""
        # Simulated index lookup
        return [row for row in table if predicate(row)]
  
    def index_scan_with_prefetch(self, table, predicate):
        """Use index with memory prefetching"""
        # Simulated index with prefetch
        return [row for row in table if predicate(row)]
  
    def full_table_scan(self, table, predicate):
        """Sequential scan for non-selective queries"""
        return [row for row in table if predicate(row)]
```

**Impact**:

- Performance: 2-10x improvement by choosing right algorithm
- Energy efficiency: Avoid unnecessary work (e.g., index overhead for full scans)
- Adaptability: Handles diverse workloads efficiently

**When to Use**:

- Variable input characteristics (size, distribution, sortedness)
- Performance-critical code paths
- Systems handling diverse workloads
- When profiling shows algorithm choice matters

**Key Principles**:

- **Measure first**: Profile to understand input characteristics
- **Threshold tuning**: Benchmark to find optimal switching points
- **Hybrid approaches**: Combine algorithms (e.g., Timsort = merge + insertion)
- **Runtime adaptation**: Analyze data during execution

## Measuring Impact: Profile Before You Optimize

Don't guess. Measure. Focus on hot paths—the 20% of code that runs 80% of the time.

**Quick Profiling in Python**:

```python
import cProfile
import pstats

# Profile your code
cProfile.run('your_function()', 'profile_stats')

# Analyze results
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 functions by time
```

**Line-by-Line Profiling**:

```python
from line_profiler import LineProfiler

def my_function():
    # Your code here
    pass

profiler = LineProfiler()
profiler.add_function(my_function)
profiler.run('my_function()')
profiler.print_stats()
```

**What to Look For**:

- Functions called most frequently
- Functions consuming most CPU time
- Unexpected O(n²) behavior (nested loops, repeated lookups)
- Unnecessary allocations (creating objects in loops)

**Rust Profiling Example**:

```rust
// Add to Cargo.toml for benchmarking
[dev-dependencies]
criterion = "0.5"

// Benchmark example
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn fibonacci(n: u64) -> u64 {
    match n {
        0 => 1,
        1 => 1,
        n => fibonacci(n-1) + fibonacci(n-2),
    }
}

fn criterion_benchmark(c: &mut Criterion) {
    c.bench_function("fib 20", |b| b.iter(|| fibonacci(black_box(20))));
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
```

```bash
# Run benchmarks
cargo bench

# Generate flamegraph (install: cargo install flamegraph)
cargo flamegraph --bin your-binary

# Profile with perf (Linux)
perf record --call-graph dwarf ./target/release/your-binary
perf report

# Memory profiling with valgrind
cargo build
valgrind --tool=dhat ./target/debug/your-binary

# Energy measurement with perf (Intel RAPL)
perf stat -e power/energy-pkg/ ./target/release/your-binary
```

**Tools**:

- **Python**: cProfile, line_profiler, memory_profiler
- **Java**: JProfiler, YourKit, VisualVM
- **Node.js**: clinic.js, 0x
- **Go**: pprof
- **Rust**: cargo-flamegraph, perf, valgrind (DHAT), criterion (benchmarking)
- **Linux**: perf, flamegraphs

**Energy Measurement**:

- **CodeCarbon**: Python library for tracking energy consumption
- **Cloud Carbon Footprint**: For cloud workloads
- **PowerTOP**: Linux tool for power consumption analysis

## Real-World Case Study: API Optimization

**Scenario**: REST API serving user data, 5,000 requests/second, running on 20 EC2 instances.

**Problems Found** (via profiling):

1. Permission checking using List (Pattern 1)
2. N+1 database queries for user data (Pattern 2)
3. No caching of user profiles (Pattern 3)
4. Loading full user objects when only ID and name needed (Pattern 4)

**Changes Made**:

1. Converted permission list to Set (5,000 items)
2. Batched database queries (one query instead of N)
3. Added Redis cache with 1-hour TTL (95% hit rate)
4. Used database projections (SELECT id, name instead of SELECT *)

**Results**:

- Response time: 200ms → 50ms (4x improvement)
- CPU usage: -60% (from 80% to 32% average)
- Database load: -75% (from 400 queries/sec to 100 queries/sec)
- Memory usage: +200MB for Redis cache
- Energy consumption: -55% (measured with Cloud Carbon Footprint)
- Cost savings: $8,000/month (reduced from 20 to 8 instances)
- Carbon emissions: -55% (from 2.4 tons CO2/month to 1.1 tons)

**Timeline**: 2 days of profiling and implementation. Immediate impact after deployment.

**Tradeoffs**: Added Redis dependency (operational complexity), increased memory usage (200MB), cache invalidation logic (development time). Worth it for 4x performance improvement and 55% energy reduction.

## The Tradeoffs

Nothing is free. Every optimization has tradeoffs.

**Caching**: Uses memory. Adds complexity (cache invalidation, consistency). But saves massive CPU.

**Hash tables**: Use more memory than arrays (overhead for hash structure). But O(1) lookups vs O(n).

**Batching**: Adds latency (wait for batch to fill). But reduces total work dramatically.

**Streaming**: More complex code (generators, iterators). But uses constant memory instead of O(n).

**Optimization**: Takes developer time. Adds complexity. But pays off at scale.

The key: measure, understand the tradeoff, optimize where it matters. Don't optimize everything. Optimize the hot paths.

## Quick Reference: Pattern Selection Guide

| Problem              | Pattern                    | Skill Level     | Complexity Change    | Impact      | Tradeoff                  |
| -------------------- | -------------------------- | --------------- | -------------------- | ----------- | ------------------------- |
| Repeated lookups     | HashMap/Set                | 🟢 Basic        | O(n) → O(1)         | High        | More memory               |
| Multiple I/O calls   | Batching                   | 🟢 Basic        | N calls → 1 call    | High        | Added latency             |
| Repeated computation | Caching                    | 🟡 Intermediate | Recompute → Lookup  | High        | Memory + complexity       |
| Large datasets       | Streaming                  | 🟡 Intermediate | O(n) memory → O(1)  | Medium      | Code complexity           |
| Wrong data structure | Choose right one           | 🟡 Intermediate | Varies               | High        | None (just better)        |
| Unnecessary work     | Lazy evaluation            | 🟡 Intermediate | Do less              | Medium      | Code complexity           |
| CPU-bound tasks      | Parallelize                | 🔴 Advanced     | Faster               | Medium      | Overhead + complexity     |
| Massive sets         | Probabilistic structures   | 🔴 Advanced     | Exact → Approximate | Very High   | Small error rate          |
| Cache misses         | Memory layout optimization | 🔴 Advanced     | Random → Sequential | High        | Code complexity           |
| Variable inputs      | Adaptive algorithms        | 🔴 Advanced     | Fixed → Dynamic     | Medium-High | Implementation complexity |

## What's Next

These patterns are foundational. They apply to almost every codebase. But they're just the beginning.

Next up: **Database Optimization Strategies**. We'll dive into query optimization, index strategies, connection pooling, and database-specific patterns that dramatically reduce energy consumption at the data layer.

For now, pick one pattern from this article. Profile your hottest code path. Apply the pattern. Measure the impact. I guarantee you'll find something worth optimizing.

---

**Resources**:

- **Profiling Tools**:

  - Python: cProfile, line_profiler, memory_profiler
  - Java: JProfiler, YourKit, VisualVM
  - Node.js: clinic.js, 0x
  - Go: pprof
  - Rust: cargo-flamegraph, perf, valgrind, criterion, heaptrack
  - Linux: perf, flamegraphs
- **Energy Measurement**:

  - CodeCarbon: https://codecarbon.io/
  - Cloud Carbon Footprint: https://www.cloudcarbonfootprint.org/
  - Green Software Foundation: https://greensoftware.foundation/
- **Algorithm Complexity**:

  - Big-O Cheat Sheet: https://www.bigocheatsheet.com/
  - Algorithm Visualizations: https://visualgo.net/
- **Research Foundation** (for interested readers):

  - Energy-Efficient Algorithms (MIT): https://arxiv.org/abs/1605.08448
  - Landauer's Principle: https://en.wikipedia.org/wiki/Landauer%27s_principle
  - Green Machine Learning (Ekkono): https://ekkono.ai/
  - Energy-Efficient Design Patterns: Academic research on software patterns
- **Previous Article**: [Why Your Code&#39;s Carbon Footprint Matters](#)

**Coming Up**: Database Optimization Strategies, Building Carbon-Aware Applications, Sustainable Microservices Architecture, Green DevOps Practices

---

*What's your biggest algorithmic inefficiency? Have you profiled your hot paths? What patterns have you applied that made a real difference? Drop a comment—I want to hear about your optimization wins.*
