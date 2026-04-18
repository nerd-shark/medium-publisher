# v3 Changelog - Energy-Efficient Algorithm Patterns

## Version: v3
**Date**: 2025-01-29
**Changes**: Added Rust profiling tools and examples

## Summary of Changes

### 1. Added Rust Profiling Example Section
**Location**: "Measuring Impact: Profile Before You Optimize" section

Added comprehensive Rust profiling example including:
- Criterion benchmarking setup and code example
- Command-line examples for:
  - `cargo bench` - Running benchmarks
  - `cargo flamegraph` - Generating flamegraphs
  - `perf` - CPU profiling on Linux
  - `valgrind` - Memory profiling with DHAT
  - `perf stat` - Energy measurement with Intel RAPL

### 2. Updated Tools List (Measuring Impact Section)
**Before**:
```
- **Go**: pprof
- **Linux**: perf, flamegraphs
```

**After**:
```
- **Go**: pprof
- **Rust**: cargo-flamegraph, perf, valgrind (DHAT), criterion (benchmarking)
- **Linux**: perf, flamegraphs
```

### 3. Updated Resources Section
**Before**:
```
- Go: pprof
```

**After**:
```
- Go: pprof
- Rust: cargo-flamegraph, perf, valgrind, criterion, heaptrack
- Linux: perf, flamegraphs
```

### 4. Updated "What's Next" Section
**Changes**:
- Changed next article from "Building Carbon-Aware Applications" to "Database Optimization Strategies"
- Removed "Then:" paragraph about Sustainable Microservices Architecture
- Removed "After that:" paragraph about Green DevOps Practices
- Updated "Coming Up" line to prioritize Database Optimization Strategies first

## Rationale

The article covers energy-efficient algorithms across multiple languages (Python, Java, Node.js, Go) but was missing Rust profiling tools. Given that:
1. Rust is increasingly used for performance-critical systems
2. The workspace uses Rust for infrastructure components (Nagara-Kozo)
3. Rust's zero-cost abstractions make it ideal for energy-efficient code
4. Readers interested in green coding would benefit from Rust profiling guidance

Adding Rust profiling tools provides complete coverage for developers working on energy-efficient systems.

## Files Modified
- `for-approval/medium/green-coding/ee-algo-patterns/versions/v3-ee-algo-patterns.md` (created from v2)

## Next Steps
- Review v3 for accuracy
- Consider adding Rust-specific algorithm examples in future versions
- Potentially add C++ profiling tools for completeness
