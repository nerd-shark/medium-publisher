# Database Optimization Patterns - Quick Reference

## 13 Patterns for Energy-Efficient Databases

### 🟢 Basic Patterns (Easy Wins)

#### 1. Index Strategically
**Problem**: Full table scans waste massive energy  
**Solution**: Index what you query, not everything  
**Impact**: 250x faster queries, -60% CPU, -95% disk I/O  
**Example**: `CREATE INDEX idx_users_email ON users(email);`

#### 2. Connection Pooling Done Right
**Problem**: Opening/closing connections is expensive  
**Solution**: Reuse connections with proper pool sizing  
**Impact**: +3x throughput, -40% memory, -20% CPU  
**Tools**: HikariCP (Java), SQLAlchemy (Python), pg-pool (Node.js)

#### 4. Batch Operations
**Problem**: N queries in a loop (N+1 problem)  
**Solution**: Single batched query  
**Impact**: 100x faster, -99% network overhead  
**Example**: `UPDATE ... FROM (VALUES ...) AS v WHERE ...`

#### 5. Avoid SELECT *
**Problem**: Fetching columns you don't need  
**Solution**: Select only required columns  
**Impact**: 5000x less data transfer, -95% memory  
**Example**: `SELECT id, name FROM users` not `SELECT * FROM users`

### 🟡 Intermediate Patterns (Require Understanding)

#### 3. Query Result Caching
**Problem**: Repeated queries for same data  
**Solution**: Cache results with proper TTL  
**Impact**: 90% cache hit = -80% database CPU  
**Tools**: Redis, Memcached, application-level caching

#### 6. Optimize JOINs
**Problem**: Wrong JOIN order, unnecessary JOINs  
**Solution**: Filter early, join late  
**Impact**: 100x fewer rows processed, -95% CPU  
**Example**: Filter on indexed columns before joining

#### 7. Pagination Done Right
**Problem**: OFFSET scans and discards rows  
**Solution**: Cursor-based pagination (keyset)  
**Impact**: 500x faster for deep pages, consistent performance  
**Example**: `WHERE created_at < ? ORDER BY created_at LIMIT 10`

#### 8. Aggregate in Database
**Problem**: Fetching all rows to aggregate in code  
**Solution**: Use database aggregation functions  
**Impact**: -99% data transfer, -99% memory  
**Example**: `SELECT SUM(total), COUNT(*), AVG(total) FROM orders`

### 🔴 Advanced Patterns (Require Expertise)

#### 9. Materialized Views
**Problem**: Complex queries that run frequently  
**Solution**: Pre-compute and refresh periodically  
**Impact**: 5000x faster queries, -99% CPU  
**Example**: `CREATE MATERIALIZED VIEW ... REFRESH ...`

#### 10. Database-Specific Optimizations
**Problem**: Generic configurations waste resources  
**Solution**: Tune for your specific database  
**Impact**: Varies by database and workload  
**Examples**: 
- PostgreSQL: VACUUM, partitioning, parallel queries
- MySQL: InnoDB buffer pool, query cache
- MongoDB: Covered queries, shard key selection

### 🔴 Architecture Decisions (Strategic Choices)

#### 11. Choosing the Right Database
**Problem**: Using wrong database type for workload  
**Solution**: Match database to data access patterns  
**Impact**: 10-100x performance improvement  
**Examples**:
- Relational (PostgreSQL, MySQL): Structured data, ACID
- Document (MongoDB): Semi-structured, flexible schema
- Key-Value (Redis, DynamoDB): Simple lookups, caching
- Graph (Neo4j, Neptune): Highly connected data
- Time-Series (InfluxDB, TimescaleDB): Time-stamped data

### 🟡 Infrastructure Decisions (Deployment Choices)

#### 12. Cloud vs On-Premises
**Problem**: Cloud overhead vs on-prem idle capacity  
**Solution**: Match to workload pattern and carbon goals  
**Impact**: 70-90% energy savings (cloud auto-scaling) or 10-20% better performance (on-prem bare metal)  
**Cloud Advantages**: Auto-scaling, low-carbon regions  
**On-Prem Advantages**: No virtualization overhead, bare metal

#### 13. Serverless vs Provisioned
**Problem**: 24/7 provisioned vs cold start serverless  
**Solution**: Match to usage pattern  
**Impact**: 70-90% energy savings for dev/test (serverless)  
**Serverless**: Best for sporadic workloads, dev/test  
**Provisioned**: Best for 24/7 production, consistent load

## Pattern Selection Guide

### Start Here (Biggest Impact, Easiest Implementation)
1. **Avoid SELECT *** - Immediate impact, zero risk
2. **Index Strategically** - Profile first, add indexes for slow queries
3. **Connection Pooling** - One-time setup, ongoing benefits
4. **Batch Operations** - Find N+1 queries, batch them

### Next Steps (Moderate Effort, High Impact)
5. **Query Result Caching** - Start with high-TTL, rarely-changing data
6. **Optimize JOINs** - Profile slow queries, reorder JOINs
7. **Pagination** - Replace OFFSET with cursor-based
8. **Aggregate in Database** - Move aggregations from code to SQL

### Advanced (High Effort, Specific Use Cases)
9. **Materialized Views** - For analytics, dashboards, complex reports
10. **Database-Specific** - After exhausting generic optimizations

### Architecture Decisions (Strategic, Long-Term Impact)
11. **Right Database Type** - Evaluate during design phase, consider polyglot persistence
12. **Cloud vs On-Prem** - Consider workload patterns, carbon intensity, costs
13. **Serverless vs Provisioned** - Match to usage patterns (dev/test vs production)

## Impact Summary

| Pattern | Difficulty | Typical Impact | Energy Savings |
|---------|-----------|----------------|----------------|
| Index Strategically | 🟢 Easy | 100-1000x faster | 50-70% |
| Connection Pooling | 🟢 Easy | 3x throughput | 20-40% |
| Query Caching | 🟡 Medium | 10-100x faster | 50-90% |
| Batch Operations | 🟢 Easy | 100x faster | 90-99% |
| Avoid SELECT * | 🟢 Easy | 10-5000x less data | 50-95% |
| Optimize JOINs | 🟡 Medium | 10-100x faster | 50-95% |
| Pagination | 🟡 Medium | 100-500x faster | 90-99% |
| Aggregate in DB | 🟡 Medium | 100x faster | 90-99% |
| Materialized Views | 🔴 Hard | 1000-5000x faster | 95-99% |
| DB-Specific | 🔴 Hard | Varies | 10-50% |
| Right Database | 🔴 Hard | 10-100x faster | 50-95% |
| Cloud vs On-Prem | 🟡 Medium | Varies | 70-90% (cloud) |
| Serverless vs Provisioned | 🟡 Medium | Varies | 70-90% (serverless) |

## Common Mistakes to Avoid

### Over-Indexing
- **Problem**: Index every column "just in case"
- **Impact**: Slow writes, wasted storage, maintenance overhead
- **Solution**: Index only what you query, monitor index usage

### Under-Pooling
- **Problem**: Pool size too small, connections queuing
- **Impact**: Slow responses, timeouts
- **Solution**: Monitor pool utilization, size appropriately

### Cache Everything
- **Problem**: Caching data that changes frequently
- **Impact**: Stale data, cache invalidation complexity
- **Solution**: Cache only stable, frequently-accessed data

### Premature Optimization
- **Problem**: Optimizing before measuring
- **Impact**: Wasted effort on non-bottlenecks
- **Solution**: Profile first, optimize hot paths

## Profiling Tools by Database

### PostgreSQL
- `EXPLAIN ANALYZE` - Query execution plan with timing
- `pg_stat_statements` - Query statistics
- `pg_stat_user_tables` - Table access statistics
- `pgBadger` - Log analyzer

### MySQL
- `EXPLAIN` - Query execution plan
- Slow Query Log - Queries exceeding threshold
- Performance Schema - Detailed performance data
- `mysqldumpslow` - Slow query log analyzer

### MongoDB
- `explain()` - Query execution plan
- Database Profiler - Query profiling
- `$indexStats` - Index usage statistics
- MongoDB Compass - Visual profiling

## Metrics to Track

### Query Performance
- Execution time (p50, p95, p99)
- Rows scanned vs rows returned
- Index usage (scans vs seeks)
- Query frequency

### Resource Usage
- CPU utilization
- Memory usage
- Disk I/O operations
- Network transfer

### Connection Management
- Active connections
- Idle connections
- Connection wait time
- Pool utilization

### Cache Effectiveness
- Cache hit rate
- Cache miss rate
- Eviction rate
- Memory usage

## Energy Calculation

### Basic Formula
```
Energy (kWh) = Power (W) × Time (h) / 1000

Example:
- Database CPU: 50W average
- Running 24/7 for 30 days
- Energy = 50W × 720h / 1000 = 36 kWh/month

After optimization (50% CPU reduction):
- Database CPU: 25W average
- Energy = 25W × 720h / 1000 = 18 kWh/month
- Savings: 18 kWh/month = 216 kWh/year
```

### Carbon Calculation
```
Carbon (kg CO2e) = Energy (kWh) × Carbon Intensity (gCO2e/kWh) / 1000

Example (US East region, ~400 gCO2e/kWh):
- Energy savings: 216 kWh/year
- Carbon = 216 × 400 / 1000 = 86.4 kg CO2e/year
```

## Quick Wins Checklist

- [ ] Run `EXPLAIN ANALYZE` on slowest queries
- [ ] Check for missing indexes on WHERE/JOIN columns
- [ ] Verify connection pooling is configured
- [ ] Find and eliminate SELECT * queries
- [ ] Identify N+1 query patterns
- [ ] Review pagination implementation
- [ ] Check cache hit rates
- [ ] Monitor index usage statistics
- [ ] Audit JOIN query performance
- [ ] Review aggregation queries

## Resources

### Documentation
- PostgreSQL Performance Tips: https://wiki.postgresql.org/wiki/Performance_Optimization
- MySQL Optimization: https://dev.mysql.com/doc/refman/8.0/en/optimization.html
- MongoDB Performance: https://docs.mongodb.com/manual/administration/analyzing-mongodb-performance/

### Tools
- HikariCP: https://github.com/brettwooldridge/HikariCP
- SQLAlchemy: https://www.sqlalchemy.org/
- Redis: https://redis.io/
- pgBadger: https://github.com/darold/pgbadger

### Books
- "High Performance MySQL" by Baron Schwartz
- "PostgreSQL: Up and Running" by Regina Obe
- "Designing Data-Intensive Applications" by Martin Kleppmann

---

**Note**: This is a quick reference. See the full article for detailed explanations, code examples, and case studies.
