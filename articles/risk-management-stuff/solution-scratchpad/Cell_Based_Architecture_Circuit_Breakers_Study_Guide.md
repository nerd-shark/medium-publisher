# Cell-Based Architecture & Circuit Breakers for Resilient Risk Systems

## Executive Summary

This study guide provides comprehensive guidance on implementing cell-based architecture and circuit breaker patterns to achieve design for resiliency in Freddie Mac's enterprise risk management solutions. These patterns are essential for building fault-tolerant, scalable systems that can gracefully handle failures while maintaining business continuity across credit risk, market risk, operational risk, and compliance domains.

## Cell-Based Architecture Fundamentals

### What is Cell-Based Architecture?

Cell-based architecture is a resilience pattern that partitions system resources into independent, self-contained units called "cells." Each cell operates autonomously and can continue functioning even when other cells fail, preventing cascading failures across the entire system.

**Key Characteristics:**
- **Isolation:** Each cell is independent with its own resources
- **Autonomy:** Cells can operate without dependencies on other cells
- **Fault Containment:** Failures are contained within individual cells
- **Horizontal Scaling:** Add capacity by adding more cells
- **Graceful Degradation:** System continues operating with reduced capacity

### Cell Design Principles for Risk Systems

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           RISK SYSTEM CELL ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐            │
│  │  Credit Risk    │    │  Market Risk    │    │ Operational     │            │
│  │     Cell        │    │     Cell        │    │  Risk Cell      │            │
│  │                 │    │                 │    │                 │            │
│  │ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │            │
│  │ │Compute Layer│ │    │ │Compute Layer│ │    │ │Compute Layer│ │            │
│  │ │• EKS Pods   │ │    │ │• EKS Pods   │ │    │ │• EKS Pods   │ │            │
│  │ │• Lambda     │ │    │ │• Lambda     │ │    │ │• Lambda     │ │            │
│  │ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │            │
│  │                 │    │                 │    │                 │            │
│  │ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │            │
│  │ │ Data Layer  │ │    │ │ Data Layer  │ │    │ │ Data Layer  │ │            │
│  │ │• RDS        │ │    │ │• RDS        │ │    │ │• DynamoDB   │ │            │
│  │ │• ElastiCache│ │    │ │• ElastiCache│ │    │ │• ElastiCache│ │            │
│  │ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │            │
│  │                 │    │                 │    │                 │            │
│  │ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │            │
│  │ │Network Layer│ │    │ │Network Layer│ │    │ │Network Layer│ │            │
│  │ │• Load Bal.  │ │    │ │• Load Bal.  │ │    │ │• Load Bal.  │ │            │
│  │ │• API Gateway│ │    │ │• API Gateway│ │    │ │• API Gateway│ │            │
│  │ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │            │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘            │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │                        SHARED INFRASTRUCTURE                                ││
│  │                                                                             ││
│  │ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          ││
│  │ │Unified Data │ │Event Stream │ │Monitoring   │ │Security     │          ││
│  │ │Platform     │ │(MSK)        │ │(CloudWatch) │ │(IAM/KMS)    │          ││
│  │ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘          ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Circuit Breaker Pattern Fundamentals

### What is a Circuit Breaker?

A circuit breaker is a design pattern that prevents cascading failures by monitoring service calls and automatically routing to "Plan B" alternatives when failure rates exceed thresholds. **CRITICAL: Circuit breakers should never shut down services - they enable graceful degradation through fallback routing.** It provides three states: Closed (normal operation), Open (routing to fallbacks), and Half-Open (testing recovery).

**Circuit Breaker States:**
```
┌─────────────────────────────────────────────────────────────────┐
│                    CIRCUIT BREAKER STATES                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    Failure Rate    ┌─────────────┐            │
│  │   CLOSED    │    Exceeds         │    OPEN     │            │
│  │             │    Threshold       │             │            │
│  │ • Normal    │───────────────────▶│ • Route to  │            │
│  │   Operation │                    │   Plan B    │            │
│  │ • Monitor   │                    │ • Fallback  │            │
│  │   Failures  │                    │   Services  │            │
│  │ • Primary   │                    │ • Cached    │            │
│  │   Path      │                    │   Responses │            │
│  └─────────────┘                    └─────────────┘            │
│         ▲                                   │                  │
│         │                                   │ Timeout          │
│         │ Success                           │ Expires          │
│         │                                   ▼                  │
│  ┌─────────────┐                    ┌─────────────┐            │
│  │ HALF-OPEN   │                    │ HALF-OPEN   │            │
│  │             │                    │             │            │
│  │ • Test      │◀───────────────────│ • Allow     │            │
│  │   Recovery  │                    │   Limited   │            │
│  │ • Limited   │                    │   Primary   │            │
│  │   Primary   │                    │   Calls     │            │
│  │   Calls     │                    │ • Monitor   │            │
│  │ • Maintain  │                    │   Results   │            │
│  │   Fallbacks │                    │ • Keep Plan │            │
│  │             │                    │   B Ready   │            │
│  └─────────────┘                    └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

## "Plan B" Routing Strategies for Circuit Breakers

### Core Principle: Never Shut Down, Always Route

**The Golden Rule:** When a circuit breaker opens, the service MUST continue operating by routing to alternative paths. Circuit breakers enable resilience through intelligent routing, not service termination.

### Plan B Routing Patterns

**1. Fallback Service Routing:**
```python
class PlanBRouter:
    def __init__(self):
        self.primary_service = "primary-credit-scoring-service"
        self.fallback_services = [
            "backup-credit-scoring-service",
            "simplified-credit-scoring-service",
            "cached-credit-scoring-service"
        ]
        self.circuit_breaker = RiskServiceCircuitBreaker(self.primary_service)
    
    def route_credit_score_request(self, request):
        """Route request with Plan B fallbacks"""
        
        # Try primary service first
        if self.circuit_breaker.state == CircuitState.CLOSED:
            try:
                return self.circuit_breaker.call(
                    self._call_primary_service, request
                )
            except CircuitBreakerOpenException:
                # Circuit just opened, route to Plan B
                pass
        
        # Circuit is open - execute Plan B routing
        return self._execute_plan_b_routing(request)
    
    def _execute_plan_b_routing(self, request):
        """Execute Plan B routing strategies in priority order"""
        
        # Plan B1: Route to backup service in different AZ
        try:
            return self._call_backup_service(request)
        except Exception as e:
            print(f"Backup service failed: {e}")
        
        # Plan B2: Route to simplified scoring service
        try:
            return self._call_simplified_service(request)
        except Exception as e:
            print(f"Simplified service failed: {e}")
        
        # Plan B3: Return cached/historical score
        try:
            return self._get_cached_score(request)
        except Exception as e:
            print(f"Cache lookup failed: {e}")
        
        # Plan B4: Return rule-based score (last resort)
        return self._calculate_rule_based_score(request)
    
    def _call_backup_service(self, request):
        """Call backup service in different availability zone"""
        # Implementation routes to geographically separate service
        return {"score": 720, "source": "backup_service", "confidence": "high"}
    
    def _call_simplified_service(self, request):
        """Call simplified scoring service with reduced features"""
        # Implementation uses simpler model with fewer data dependencies
        return {"score": 700, "source": "simplified_model", "confidence": "medium"}
    
    def _get_cached_score(self, request):
        """Get previously calculated score from cache"""
        # Implementation retrieves cached score with staleness check
        return {"score": 715, "source": "cache", "confidence": "medium", "age_hours": 2}
    
    def _calculate_rule_based_score(self, request):
        """Calculate score using business rules (no ML dependencies)"""
        # Implementation uses simple business rules as absolute fallback
        return {"score": 650, "source": "rules_engine", "confidence": "low"}
```

**2. Geographic Routing:**
```python
class GeographicPlanBRouter:
    def __init__(self):
        self.regions = {
            'primary': 'us-east-1',
            'secondary': 'us-west-2',
            'tertiary': 'us-central-1'
        }
        self.circuit_breakers = {
            region: RiskServiceCircuitBreaker(f"risk-service-{region}")
            for region in self.regions.values()
        }
    
    def route_with_geographic_fallback(self, request):
        """Route request with geographic Plan B fallbacks"""
        
        # Try primary region
        primary_cb = self.circuit_breakers[self.regions['primary']]
        if primary_cb.state == CircuitState.CLOSED:
            try:
                return primary_cb.call(self._call_region_service, 
                                     self.regions['primary'], request)
            except CircuitBreakerOpenException:
                pass
        
        # Plan B: Route to secondary region
        secondary_cb = self.circuit_breakers[self.regions['secondary']]
        if secondary_cb.state != CircuitState.OPEN:
            try:
                return secondary_cb.call(self._call_region_service,
                                       self.regions['secondary'], request)
            except CircuitBreakerOpenException:
                pass
        
        # Plan C: Route to tertiary region
        tertiary_cb = self.circuit_breakers[self.regions['tertiary']]
        return tertiary_cb.call(self._call_region_service,
                              self.regions['tertiary'], request)
    
    def _call_region_service(self, region, request):
        """Call service in specific region"""
        # Implementation calls service in specified AWS region
        return {"result": "success", "region": region}
```

**3. Capability-Based Routing:**
```python
class CapabilityPlanBRouter:
    def __init__(self):
        self.capabilities = {
            'full_ml_model': {
                'service': 'sagemaker-full-model',
                'features': ['credit_score', 'risk_grade', 'probability_default', 'explanations'],
                'latency': 'high',
                'accuracy': 'highest'
            },
            'fast_ml_model': {
                'service': 'sagemaker-fast-model', 
                'features': ['credit_score', 'risk_grade'],
                'latency': 'medium',
                'accuracy': 'high'
            },
            'rules_engine': {
                'service': 'business-rules-engine',
                'features': ['credit_score'],
                'latency': 'low', 
                'accuracy': 'medium'
            },
            'lookup_table': {
                'service': 'score-lookup-service',
                'features': ['credit_score'],
                'latency': 'very_low',
                'accuracy': 'low'
            }
        }
        
        self.circuit_breakers = {
            name: RiskServiceCircuitBreaker(cap['service'])
            for name, cap in self.capabilities.items()
        }
    
    def route_by_capability_degradation(self, request, required_features=None):
        """Route request with capability-based Plan B degradation"""
        
        required_features = required_features or ['credit_score']
        
        # Try capabilities in order of preference
        for capability_name, capability in self.capabilities.items():
            
            # Check if capability provides required features
            if not all(feature in capability['features'] for feature in required_features):
                continue
            
            circuit_breaker = self.circuit_breakers[capability_name]
            
            # Skip if circuit is open
            if circuit_breaker.state == CircuitState.OPEN:
                continue
            
            try:
                result = circuit_breaker.call(
                    self._call_capability_service, capability_name, request
                )
                result['capability_used'] = capability_name
                result['degradation_level'] = self._get_degradation_level(capability_name)
                return result
                
            except CircuitBreakerOpenException:
                continue
        
        # All capabilities failed - return error with guidance
        return {
            'error': 'All capabilities unavailable',
            'retry_after': 60,
            'fallback_available': False
        }
    
    def _call_capability_service(self, capability_name, request):
        """Call specific capability service"""
        capability = self.capabilities[capability_name]
        # Implementation calls the specific service
        return {
            'credit_score': 700,
            'service': capability['service'],
            'latency': capability['latency'],
            'accuracy': capability['accuracy']
        }
    
    def _get_degradation_level(self, capability_name):
        """Get degradation level for capability"""
        degradation_map = {
            'full_ml_model': 'none',
            'fast_ml_model': 'low', 
            'rules_engine': 'medium',
            'lookup_table': 'high'
        }
        return degradation_map.get(capability_name, 'unknown')
```

**4. Data Source Plan B Routing:**
```python
class DataSourcePlanBRouter:
    def __init__(self):
        self.data_sources = {
            'primary_db': {
                'type': 'real_time',
                'latency': 'low',
                'completeness': 'high',
                'endpoint': 'primary-rds-cluster'
            },
            'replica_db': {
                'type': 'near_real_time', 
                'latency': 'medium',
                'completeness': 'high',
                'endpoint': 'read-replica-cluster'
            },
            'data_warehouse': {
                'type': 'batch',
                'latency': 'high',
                'completeness': 'very_high',
                'endpoint': 'redshift-cluster'
            },
            'cache': {
                'type': 'cached',
                'latency': 'very_low',
                'completeness': 'variable',
                'endpoint': 'elasticache-cluster'
            }
        }
        
        self.circuit_breakers = {
            name: RiskServiceCircuitBreaker(f"data-source-{name}")
            for name in self.data_sources.keys()
        }
    
    def get_borrower_data_with_fallbacks(self, borrower_id):
        """Get borrower data with Plan B data source routing"""
        
        # Plan A: Primary database (real-time data)
        primary_cb = self.circuit_breakers['primary_db']
        if primary_cb.state != CircuitState.OPEN:
            try:
                data = primary_cb.call(self._get_from_primary_db, borrower_id)
                data['data_source'] = 'primary_db'
                data['freshness'] = 'real_time'
                return data
            except CircuitBreakerOpenException:
                pass
        
        # Plan B: Read replica (near real-time data)
        replica_cb = self.circuit_breakers['replica_db']
        if replica_cb.state != CircuitState.OPEN:
            try:
                data = replica_cb.call(self._get_from_replica_db, borrower_id)
                data['data_source'] = 'replica_db'
                data['freshness'] = 'near_real_time'
                return data
            except CircuitBreakerOpenException:
                pass
        
        # Plan C: Data warehouse (batch data, but complete)
        warehouse_cb = self.circuit_breakers['data_warehouse']
        if warehouse_cb.state != CircuitState.OPEN:
            try:
                data = warehouse_cb.call(self._get_from_warehouse, borrower_id)
                data['data_source'] = 'data_warehouse'
                data['freshness'] = 'batch'
                return data
            except CircuitBreakerOpenException:
                pass
        
        # Plan D: Cache (potentially stale but available)
        cache_cb = self.circuit_breakers['cache']
        try:
            data = cache_cb.call(self._get_from_cache, borrower_id)
            data['data_source'] = 'cache'
            data['freshness'] = 'cached'
            return data
        except CircuitBreakerOpenException:
            pass
        
        # All data sources failed - return minimal data for processing
        return {
            'borrower_id': borrower_id,
            'data_source': 'minimal',
            'freshness': 'none',
            'error': 'All data sources unavailable',
            'can_process': False
        }
    
    def _get_from_primary_db(self, borrower_id):
        """Get data from primary database"""
        # Implementation queries primary RDS cluster
        return {'borrower_id': borrower_id, 'credit_history': 'complete'}
    
    def _get_from_replica_db(self, borrower_id):
        """Get data from read replica"""
        # Implementation queries read replica
        return {'borrower_id': borrower_id, 'credit_history': 'complete'}
    
    def _get_from_warehouse(self, borrower_id):
        """Get data from data warehouse"""
        # Implementation queries Redshift
        return {'borrower_id': borrower_id, 'credit_history': 'historical'}
    
    def _get_from_cache(self, borrower_id):
        """Get data from cache"""
        # Implementation queries ElastiCache
        return {'borrower_id': borrower_id, 'credit_history': 'cached'}
```

### Plan B Routing for Freddie Mac Risk Solutions

**1. Credit Risk Assessment Plan B:**
```
Primary Path: SageMaker ML Model → Full Risk Assessment
Plan B1: Backup ML Model in Different AZ → Reduced Feature Set
Plan B2: Rules-Based Scoring → Business Logic Only
Plan B3: Historical Score Lookup → Cached Previous Results
Plan B4: Manual Review Queue → Human Intervention
```

**2. Market Risk Calculation Plan B:**
```
Primary Path: Real-time Market Data → Full VaR Calculation
Plan B1: 15-minute Delayed Data → Approximate VaR
Plan B2: End-of-Day Data → Historical VaR
Plan B3: Stress Test Results → Conservative Estimates
Plan B4: Regulatory Minimums → Compliance Floor
```

**3. Real-Time Risk Monitoring Plan B:**
```
Primary Path: Live Event Stream → Immediate Alerts
Plan B1: Batch Processing → Delayed Alerts (5-min)
Plan B2: Threshold Monitoring → Simple Rule-Based Alerts
Plan B3: Dashboard Updates → Manual Monitoring
Plan B4: Email Notifications → Basic Communication
```

**4. Regulatory Reporting Plan B:**
```
Primary Path: Automated Report Generation → Full Compliance
Plan B1: Template-Based Reports → Standard Formats
Plan B2: Manual Data Entry → Human Backup
Plan B3: Previous Period Data → Historical Baseline
Plan B4: Estimated Reporting → Regulatory Communication
```

### Implementation Guidelines for Plan B Routing

**1. Never Return Errors Without Alternatives:**
```python
# BAD: Circuit breaker that just fails
def bad_circuit_breaker_example(request):
    if circuit_breaker.state == CircuitState.OPEN:
        raise Exception("Service unavailable")  # ❌ WRONG!

# GOOD: Circuit breaker with Plan B routing
def good_circuit_breaker_example(request):
    if circuit_breaker.state == CircuitState.OPEN:
        return execute_plan_b_routing(request)  # ✅ CORRECT!
```

**2. Always Indicate Service Degradation:**
```python
def indicate_degradation_example(request):
    result = execute_plan_b_routing(request)
    result['service_status'] = 'DEGRADED'
    result['degradation_reason'] = 'Primary service unavailable'
    result['expected_recovery'] = '5 minutes'
    result['confidence_level'] = 'MEDIUM'  # Lower than primary
    return result
```

**3. Maintain Service Level Agreements:**
```python
def maintain_sla_example(request):
    # Even with Plan B, maintain minimum SLA requirements
    start_time = time.time()
    
    result = execute_plan_b_routing(request)
    
    # Ensure response time SLA is met
    if time.time() - start_time > SLA_RESPONSE_TIME:
        # Use even faster fallback if needed
        result = execute_emergency_fallback(request)
    
    return result
```

## Implementation Strategies for Freddie Mac Risk Solutions

### 1. Cell-Based Architecture for Microservices Risk Assessment Engine

**Credit Risk Cell Implementation:**
```yaml
# Credit Risk Cell Configuration
apiVersion: v1
kind: Namespace
metadata:
  name: credit-risk-cell-1
  labels:
    cell: credit-risk-cell-1
    risk-domain: credit
    cell-capacity: "10000-borrowers"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: credit-scoring-service
  namespace: credit-risk-cell-1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: credit-scoring-service
      cell: credit-risk-cell-1
  template:
    metadata:
      labels:
        app: credit-scoring-service
        cell: credit-risk-cell-1
    spec:
      affinity:
        # Ensure pods are distributed across AZs within the cell
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - credit-scoring-service
              topologyKey: kubernetes.io/hostname
      containers:
      - name: credit-scoring
        image: credit-scoring:v1.0.0
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        env:
        - name: CELL_ID
          value: "credit-risk-cell-1"
        - name: MAX_BORROWERS_PER_CELL
          value: "10000"
        - name: CIRCUIT_BREAKER_ENABLED
          value: "true"
        - name: DATABASE_ENDPOINT
          value: "credit-risk-cell-1-db.cluster-xyz.us-east-1.rds.amazonaws.com"
        - name: CACHE_ENDPOINT
          value: "credit-risk-cell-1-cache.abc123.cache.amazonaws.com"
```

**Cell Routing Strategy:**
```python
# Cell Router Implementation
import hashlib
import boto3
from typing import Dict, List, Optional

class RiskCellRouter:
    def __init__(self):
        self.cells = {
            'credit-risk': [
                {'id': 'credit-risk-cell-1', 'capacity': 10000, 'healthy': True},
                {'id': 'credit-risk-cell-2', 'capacity': 10000, 'healthy': True},
                {'id': 'credit-risk-cell-3', 'capacity': 10000, 'healthy': True}
            ],
            'market-risk': [
                {'id': 'market-risk-cell-1', 'capacity': 5000, 'healthy': True},
                {'id': 'market-risk-cell-2', 'capacity': 5000, 'healthy': True}
            ]
        }
        self.circuit_breakers = {}
    
    def route_request(self, risk_domain: str, entity_id: str) -> Optional[str]:
        """Route request to appropriate cell based on entity ID"""
        
        available_cells = [
            cell for cell in self.cells[risk_domain] 
            if cell['healthy'] and not self.is_circuit_open(cell['id'])
        ]
        
        if not available_cells:
            # All cells are unhealthy or circuits are open
            return self.get_fallback_cell(risk_domain)
        
        # Use consistent hashing to route to same cell for same entity
        cell_index = self.consistent_hash(entity_id, len(available_cells))
        selected_cell = available_cells[cell_index]
        
        return selected_cell['id']
    
    def consistent_hash(self, key: str, num_cells: int) -> int:
        """Consistent hashing for stable cell assignment"""
        hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
        return hash_value % num_cells
    
    def mark_cell_unhealthy(self, cell_id: str):
        """Mark a cell as unhealthy"""
        for domain_cells in self.cells.values():
            for cell in domain_cells:
                if cell['id'] == cell_id:
                    cell['healthy'] = False
                    break
    
    def is_circuit_open(self, cell_id: str) -> bool:
        """Check if circuit breaker is open for a cell"""
        return self.circuit_breakers.get(cell_id, {}).get('state') == 'OPEN'
    
    def get_fallback_cell(self, risk_domain: str) -> Optional[str]:
        """Get fallback cell when all primary cells are unavailable"""
        # Implement fallback logic - could be a dedicated fallback cell
        # or degraded service mode
        return f"{risk_domain}-fallback-cell"

# Usage Example
router = RiskCellRouter()

# Route credit scoring request
borrower_id = "BORROWER_12345"
cell_id = router.route_request('credit-risk', borrower_id)
print(f"Routing borrower {borrower_id} to cell: {cell_id}")
```
### 2. Circuit Breaker Implementation for Risk Services

**Service-Level Circuit Breaker:**
```python
import time
import threading
from enum import Enum
from typing import Callable, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5  # Number of failures before opening
    recovery_timeout: int = 60  # Seconds before attempting recovery
    success_threshold: int = 3  # Successes needed to close circuit
    timeout: int = 30  # Request timeout in seconds

class RiskServiceCircuitBreaker:
    def __init__(self, service_name: str, config: CircuitBreakerConfig):
        self.service_name = service_name
        self.config = config
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.lock = threading.Lock()
        
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection"""
        
        with self.lock:
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self.state = CircuitState.HALF_OPEN
                    self.success_count = 0
                else:
                    raise CircuitBreakerOpenException(
                        f"Circuit breaker is OPEN for {self.service_name}"
                    )
            
            if self.state == CircuitState.HALF_OPEN:
                if self.success_count >= self.config.success_threshold:
                    self._reset_circuit()
        
        try:
            # Execute the actual service call
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Check for timeout
            if execution_time > self.config.timeout:
                raise TimeoutError(f"Service call timed out after {execution_time}s")
            
            self._on_success()
            return result
            
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        """Handle successful service call"""
        with self.lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.config.success_threshold:
                    self._reset_circuit()
            elif self.state == CircuitState.CLOSED:
                self.failure_count = 0
    
    def _on_failure(self):
        """Handle failed service call"""
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = datetime.now()
            
            if self.failure_count >= self.config.failure_threshold:
                self.state = CircuitState.OPEN
                print(f"Circuit breaker OPENED for {self.service_name}")
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if self.last_failure_time is None:
            return True
        
        time_since_failure = datetime.now() - self.last_failure_time
        return time_since_failure.total_seconds() >= self.config.recovery_timeout
    
    def _reset_circuit(self):
        """Reset circuit breaker to closed state"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        print(f"Circuit breaker CLOSED for {self.service_name}")
    
    def get_state(self) -> dict:
        """Get current circuit breaker state"""
        return {
            'service_name': self.service_name,
            'state': self.state.value,
            'failure_count': self.failure_count,
            'success_count': self.success_count,
            'last_failure_time': self.last_failure_time.isoformat() if self.last_failure_time else None
        }

class CircuitBreakerOpenException(Exception):
    pass

# Risk Service with Circuit Breaker Integration
class CreditScoringService:
    def __init__(self):
        self.sagemaker_circuit = RiskServiceCircuitBreaker(
            'sagemaker-credit-model',
            CircuitBreakerConfig(failure_threshold=3, recovery_timeout=30)
        )
        self.database_circuit = RiskServiceCircuitBreaker(
            'credit-database',
            CircuitBreakerConfig(failure_threshold=5, recovery_timeout=60)
        )
        self.cache_circuit = RiskServiceCircuitBreaker(
            'redis-cache',
            CircuitBreakerConfig(failure_threshold=2, recovery_timeout=15)
        )
    
    def calculate_credit_score(self, borrower_id: str) -> dict:
        """Calculate credit score with circuit breaker protection"""
        
        try:
            # Try cache first (fastest path)
            cached_score = self.cache_circuit.call(
                self._get_cached_score, borrower_id
            )
            if cached_score:
                return cached_score
        except CircuitBreakerOpenException:
            print("Cache circuit is open, skipping cache lookup")
        except Exception as e:
            print(f"Cache lookup failed: {e}")
        
        try:
            # Get borrower data from database
            borrower_data = self.database_circuit.call(
                self._get_borrower_data, borrower_id
            )
        except CircuitBreakerOpenException:
            # Plan B: Use simplified data or cached borrower profile
            borrower_data = self._get_fallback_borrower_data(borrower_id)
            if not borrower_data:
                return self._get_fallback_response(borrower_id, "Database unavailable")
        
        try:
            # Calculate score using ML model
            score = self.sagemaker_circuit.call(
                self._invoke_ml_model, borrower_data
            )
            
            # Try to cache the result
            try:
                self.cache_circuit.call(
                    self._cache_score, borrower_id, score
                )
            except:
                pass  # Cache failure shouldn't affect the response
            
            return score
            
        except CircuitBreakerOpenException:
            # Plan B: Use rules-based scoring when ML model is unavailable
            return self._calculate_rules_based_score(borrower_id, borrower_data)
    
    def _get_fallback_borrower_data(self, borrower_id: str) -> Optional[dict]:
        """Get fallback borrower data when primary database is unavailable"""
        # Try alternative data sources
        try:
            # Option 1: Read replica database
            return self._get_from_read_replica(borrower_id)
        except:
            try:
                # Option 2: Data warehouse (batch data)
                return self._get_from_data_warehouse(borrower_id)
            except:
                try:
                    # Option 3: Cached borrower profile
                    return self._get_cached_borrower_profile(borrower_id)
                except:
                    # Option 4: Minimal data for basic processing
                    return {'borrower_id': borrower_id, 'data_source': 'minimal'}
    
    def _calculate_rules_based_score(self, borrower_id: str, borrower_data: dict) -> dict:
        """Calculate credit score using business rules when ML model is unavailable"""
        # Implement rules-based scoring as Plan B
        base_score = 650  # Conservative baseline
        
        # Apply simple business rules
        if borrower_data.get('payment_history') == 'excellent':
            base_score += 50
        elif borrower_data.get('payment_history') == 'good':
            base_score += 25
        
        if borrower_data.get('debt_to_income', 1.0) < 0.3:
            base_score += 30
        
        return {
            'borrower_id': borrower_id,
            'credit_score': min(base_score, 850),  # Cap at maximum
            'status': 'DEGRADED',
            'reason': 'ML model unavailable - using rules-based scoring',
            'confidence': 'MEDIUM',
            'fallback_used': True,
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_from_read_replica(self, borrower_id: str) -> dict:
        """Get borrower data from read replica"""
        # Implementation would connect to read replica
        pass
    
    def _get_from_data_warehouse(self, borrower_id: str) -> dict:
        """Get borrower data from data warehouse"""
        # Implementation would connect to Redshift
        pass
    
    def _get_cached_borrower_profile(self, borrower_id: str) -> dict:
        """Get cached borrower profile"""
        # Implementation would get cached profile
        pass
        """Get score from cache"""
        # Implementation would connect to Redis
        pass
    
    def _get_borrower_data(self, borrower_id: str) -> dict:
        """Get borrower data from database"""
        # Implementation would connect to RDS
        pass
    
    def _invoke_ml_model(self, borrower_data: dict) -> dict:
        """Invoke SageMaker model"""
        # Implementation would call SageMaker endpoint
        pass
    
    def _cache_score(self, borrower_id: str, score: dict):
        """Cache the calculated score"""
        # Implementation would store in Redis
        pass
    
    def _get_fallback_response(self, borrower_id: str, reason: str) -> dict:
        """Return fallback response when services are unavailable"""
        return {
            'borrower_id': borrower_id,
            'credit_score': None,
            'status': 'DEGRADED',
            'reason': reason,
            'fallback_used': True,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_health_status(self) -> dict:
        """Get health status of all circuit breakers"""
        return {
            'sagemaker': self.sagemaker_circuit.get_state(),
            'database': self.database_circuit.get_state(),
            'cache': self.cache_circuit.get_state()
        }

# Usage Example
credit_service = CreditScoringService()

# Calculate credit score with circuit breaker protection
try:
    result = credit_service.calculate_credit_score("BORROWER_12345")
    print(f"Credit score result: {result}")
except Exception as e:
    print(f"Service call failed: {e}")

# Check health status
health = credit_service.get_health_status()
print(f"Service health: {health}")
```
### 3. Cell-Based Architecture for Real-Time Risk Monitoring

**Event Processing Cell Design:**
```python
# Event Processing Cell for Real-Time Risk Monitoring
import asyncio
import json
from typing import Dict, List
from kafka import KafkaConsumer, KafkaProducer
from dataclasses import dataclass

@dataclass
class RiskEvent:
    event_id: str
    event_type: str
    risk_domain: str
    severity: str
    data: dict
    timestamp: str

class RiskMonitoringCell:
    def __init__(self, cell_id: str, risk_domains: List[str]):
        self.cell_id = cell_id
        self.risk_domains = risk_domains
        self.circuit_breakers = {}
        self.event_processors = {}
        self.health_status = "HEALTHY"
        
        # Initialize circuit breakers for each dependency
        self.init_circuit_breakers()
        
        # Initialize event processors for each risk domain
        self.init_event_processors()
    
    def init_circuit_breakers(self):
        """Initialize circuit breakers for external dependencies"""
        dependencies = [
            'alert-service',
            'notification-service',
            'risk-database',
            'ml-anomaly-detector'
        ]
        
        for dep in dependencies:
            self.circuit_breakers[dep] = RiskServiceCircuitBreaker(
                f"{self.cell_id}-{dep}",
                CircuitBreakerConfig(failure_threshold=3, recovery_timeout=30)
            )
    
    def init_event_processors(self):
        """Initialize event processors for each risk domain"""
        for domain in self.risk_domains:
            self.event_processors[domain] = RiskEventProcessor(
                domain, self.cell_id, self.circuit_breakers
            )
    
    async def process_risk_events(self):
        """Main event processing loop"""
        consumer = KafkaConsumer(
            *[f'risk.events.{domain}' for domain in self.risk_domains],
            bootstrap_servers=['msk-cluster:9092'],
            group_id=f'{self.cell_id}-consumer-group',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        
        for message in consumer:
            try:
                event = RiskEvent(**message.value)
                
                # Route event to appropriate processor
                processor = self.event_processors.get(event.risk_domain)
                if processor:
                    await processor.process_event(event)
                else:
                    print(f"No processor found for domain: {event.risk_domain}")
                    
            except Exception as e:
                print(f"Error processing event in cell {self.cell_id}: {e}")
                # Implement dead letter queue logic here
    
    def get_cell_health(self) -> dict:
        """Get health status of the entire cell"""
        circuit_states = {
            name: cb.get_state() 
            for name, cb in self.circuit_breakers.items()
        }
        
        # Determine overall cell health
        open_circuits = [
            name for name, state in circuit_states.items() 
            if state['state'] == 'OPEN'
        ]
        
        if len(open_circuits) > len(circuit_states) / 2:
            self.health_status = "UNHEALTHY"
        elif open_circuits:
            self.health_status = "DEGRADED"
        else:
            self.health_status = "HEALTHY"
        
        return {
            'cell_id': self.cell_id,
            'health_status': self.health_status,
            'risk_domains': self.risk_domains,
            'circuit_breakers': circuit_states,
            'open_circuits': open_circuits
        }

class RiskEventProcessor:
    def __init__(self, risk_domain: str, cell_id: str, circuit_breakers: dict):
        self.risk_domain = risk_domain
        self.cell_id = cell_id
        self.circuit_breakers = circuit_breakers
    
    async def process_event(self, event: RiskEvent):
        """Process a risk event with circuit breaker protection"""
        
        # Determine event severity and required actions
        actions = self.determine_actions(event)
        
        for action in actions:
            try:
                await self.execute_action(action, event)
            except CircuitBreakerOpenException as e:
                print(f"Circuit breaker open for {action}: {e}")
                await self.handle_degraded_action(action, event)
            except Exception as e:
                print(f"Error executing action {action}: {e}")
    
    def determine_actions(self, event: RiskEvent) -> List[str]:
        """Determine what actions to take based on event"""
        actions = []
        
        if event.severity in ['HIGH', 'CRITICAL']:
            actions.extend(['send-alert', 'notify-stakeholders'])
        
        if event.event_type == 'risk_limit_breach':
            actions.extend(['update-dashboard', 'trigger-escalation'])
        
        if event.event_type == 'anomaly_detected':
            actions.extend(['run-investigation', 'update-ml-model'])
        
        return actions
    
    async def execute_action(self, action: str, event: RiskEvent):
        """Execute a specific action with circuit breaker protection"""
        
        if action == 'send-alert':
            self.circuit_breakers['alert-service'].call(
                self._send_alert, event
            )
        elif action == 'notify-stakeholders':
            self.circuit_breakers['notification-service'].call(
                self._notify_stakeholders, event
            )
        elif action == 'update-dashboard':
            self.circuit_breakers['risk-database'].call(
                self._update_dashboard, event
            )
        elif action == 'run-investigation':
            self.circuit_breakers['ml-anomaly-detector'].call(
                self._run_investigation, event
            )
    
    async def handle_degraded_action(self, action: str, event: RiskEvent):
        """Handle actions when circuit breakers are open"""
        
        # Implement fallback mechanisms
        if action == 'send-alert':
            # Use backup alerting mechanism
            await self._send_backup_alert(event)
        elif action == 'notify-stakeholders':
            # Queue notification for later delivery
            await self._queue_notification(event)
        elif action == 'update-dashboard':
            # Cache update for later processing
            await self._cache_dashboard_update(event)
    
    def _send_alert(self, event: RiskEvent):
        """Send alert through primary alerting service"""
        pass
    
    def _notify_stakeholders(self, event: RiskEvent):
        """Notify stakeholders through primary notification service"""
        pass
    
    def _update_dashboard(self, event: RiskEvent):
        """Update risk dashboard"""
        pass
    
    def _run_investigation(self, event: RiskEvent):
        """Run ML-based investigation"""
        pass
    
    async def _send_backup_alert(self, event: RiskEvent):
        """Send alert through backup mechanism"""
        pass
    
    async def _queue_notification(self, event: RiskEvent):
        """Queue notification for later delivery"""
        pass
    
    async def _cache_dashboard_update(self, event: RiskEvent):
        """Cache dashboard update for later processing"""
        pass

# Cell Deployment Example
async def deploy_risk_monitoring_cells():
    """Deploy multiple risk monitoring cells for fault tolerance"""
    
    cells = [
        RiskMonitoringCell("risk-monitor-cell-1", ["credit-risk", "market-risk"]),
        RiskMonitoringCell("risk-monitor-cell-2", ["operational-risk", "compliance"]),
        RiskMonitoringCell("risk-monitor-cell-3", ["credit-risk", "operational-risk"])  # Overlap for redundancy
    ]
    
    # Start all cells concurrently
    tasks = [cell.process_risk_events() for cell in cells]
    await asyncio.gather(*tasks)

# Usage
if __name__ == "__main__":
    asyncio.run(deploy_risk_monitoring_cells())
```
## Best Practices and Implementation Guidelines

### 1. Cell Design Best Practices

**Cell Sizing Guidelines:**
- **Credit Risk Cells:** 10,000-50,000 borrowers per cell
- **Market Risk Cells:** 5,000-10,000 positions per cell
- **Operational Risk Cells:** 1,000-5,000 incidents per cell
- **Compliance Cells:** By business line or regulatory domain

**Cell Independence Checklist:**
```
✓ Each cell has its own compute resources (EKS nodes, Lambda functions)
✓ Each cell has its own data storage (RDS instances, DynamoDB tables)
✓ Each cell has its own caching layer (ElastiCache clusters)
✓ Cells can operate independently during network partitions
✓ Cell failure does not impact other cells
✓ Cell routing is consistent and deterministic
✓ Cell capacity can be scaled independently
✓ Cell health monitoring is implemented
```

### 2. Circuit Breaker Configuration Guidelines

**Threshold Configuration by Service Type:**
```
┌─────────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│  Service Type   │ Failure     │ Recovery    │ Success     │ Timeout     │
│                 │ Threshold   │ Timeout(s)  │ Threshold   │ (seconds)   │
├─────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ Database        │ 5           │ 60          │ 3           │ 30          │
│ Cache           │ 3           │ 15          │ 2           │ 5           │
│ ML Model        │ 3           │ 30          │ 3           │ 60          │
│ External API    │ 5           │ 120         │ 3           │ 45          │
│ Message Queue   │ 2           │ 30          │ 2           │ 10          │
│ File System     │ 3           │ 45          │ 2           │ 15          │
└─────────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

### 3. Monitoring and Observability

**Key Metrics to Monitor:**
```python
# Monitoring Configuration for Cell-Based Architecture
CELL_METRICS = {
    'cell_health_score': {
        'description': 'Overall health score of the cell (0-100)',
        'threshold_warning': 80,
        'threshold_critical': 60
    },
    'cell_request_rate': {
        'description': 'Requests per second handled by the cell',
        'threshold_warning': 1000,
        'threshold_critical': 1500
    },
    'cell_error_rate': {
        'description': 'Percentage of failed requests',
        'threshold_warning': 5,
        'threshold_critical': 10
    },
    'cell_response_time_p95': {
        'description': '95th percentile response time',
        'threshold_warning': 2000,  # milliseconds
        'threshold_critical': 5000
    }
}

CIRCUIT_BREAKER_METRICS = {
    'circuit_breaker_state': {
        'description': 'Current state of circuit breaker',
        'values': ['CLOSED', 'OPEN', 'HALF_OPEN']
    },
    'circuit_breaker_failure_rate': {
        'description': 'Failure rate that triggered circuit breaker',
        'threshold_warning': 20,
        'threshold_critical': 50
    },
    'circuit_breaker_recovery_time': {
        'description': 'Time taken to recover from open state',
        'threshold_warning': 300,  # seconds
        'threshold_critical': 600
    }
}
```

### 4. Testing Strategies

**Chaos Engineering for Cell-Based Architecture:**
```python
# Chaos Engineering Test Suite
import random
import asyncio
from typing import List

class ChaosEngineeringTests:
    def __init__(self, cells: List[str]):
        self.cells = cells
        self.test_results = {}
    
    async def test_cell_failure_isolation(self):
        """Test that cell failures don't cascade to other cells"""
        
        # Randomly select a cell to fail
        failed_cell = random.choice(self.cells)
        
        print(f"Simulating failure in cell: {failed_cell}")
        
        # Simulate cell failure
        await self.simulate_cell_failure(failed_cell)
        
        # Verify other cells continue operating
        healthy_cells = [cell for cell in self.cells if cell != failed_cell]
        
        for cell in healthy_cells:
            health_status = await self.check_cell_health(cell)
            assert health_status['status'] == 'HEALTHY', f"Cell {cell} affected by {failed_cell} failure"
        
        print("✓ Cell failure isolation test passed")
    
    async def test_circuit_breaker_behavior(self):
        """Test circuit breaker opens and recovers correctly"""
        
        # Simulate high failure rate
        await self.simulate_high_failure_rate('test-service')
        
        # Verify circuit breaker opens
        await asyncio.sleep(5)
        circuit_state = await self.get_circuit_breaker_state('test-service')
        assert circuit_state == 'OPEN', "Circuit breaker should be OPEN"
        
        # Wait for recovery timeout
        await asyncio.sleep(60)
        
        # Simulate successful requests
        await self.simulate_successful_requests('test-service')
        
        # Verify circuit breaker closes
        await asyncio.sleep(10)
        circuit_state = await self.get_circuit_breaker_state('test-service')
        assert circuit_state == 'CLOSED', "Circuit breaker should be CLOSED"
        
        print("✓ Circuit breaker behavior test passed")
    
    async def test_graceful_degradation(self):
        """Test system provides degraded service when dependencies fail"""
        
        # Simulate dependency failures
        dependencies = ['database', 'cache', 'ml-model']
        
        for dep in dependencies:
            await self.simulate_dependency_failure(dep)
            
            # Verify system still responds with degraded service
            response = await self.make_test_request()
            assert response['status'] in ['SUCCESS', 'DEGRADED'], f"System should handle {dep} failure gracefully"
        
        print("✓ Graceful degradation test passed")
    
    async def simulate_cell_failure(self, cell_id: str):
        """Simulate cell failure"""
        # Implementation would actually fail the cell
        pass
    
    async def check_cell_health(self, cell_id: str) -> dict:
        """Check cell health status"""
        # Implementation would check actual cell health
        return {'status': 'HEALTHY'}
    
    async def simulate_high_failure_rate(self, service_name: str):
        """Simulate high failure rate for a service"""
        # Implementation would generate failures
        pass
    
    async def get_circuit_breaker_state(self, service_name: str) -> str:
        """Get circuit breaker state"""
        # Implementation would check actual circuit breaker state
        return 'CLOSED'
    
    async def simulate_successful_requests(self, service_name: str):
        """Simulate successful requests"""
        # Implementation would generate successful requests
        pass
    
    async def simulate_dependency_failure(self, dependency: str):
        """Simulate dependency failure"""
        # Implementation would fail the dependency
        pass
    
    async def make_test_request(self) -> dict:
        """Make a test request to the system"""
        # Implementation would make actual request
        return {'status': 'SUCCESS'}

# Run chaos engineering tests
async def run_chaos_tests():
    cells = ['credit-risk-cell-1', 'credit-risk-cell-2', 'market-risk-cell-1']
    chaos_tests = ChaosEngineeringTests(cells)
    
    await chaos_tests.test_cell_failure_isolation()
    await chaos_tests.test_circuit_breaker_behavior()
    await chaos_tests.test_graceful_degradation()
    
    print("All chaos engineering tests completed successfully!")

# Usage
if __name__ == "__main__":
    asyncio.run(run_chaos_tests())
```

## Application to Freddie Mac Risk Solutions

### 1. Microservices Risk Assessment Engine

**Cell-Based Implementation:**
- **Credit Risk Cell:** Independent credit scoring and portfolio risk services
- **Market Risk Cell:** VaR calculations and scenario analysis services  
- **Operational Risk Cell:** Incident management and KRI monitoring services
- **Compliance Cell:** AML/KYC and regulatory reporting services

**Circuit Breaker Integration:**
- SageMaker model endpoints with 3-failure threshold
- Database connections with 5-failure threshold
- Cache services with 2-failure threshold
- External API calls with 5-failure threshold

### 2. Real-Time Risk Monitoring System

**Event Processing Cells:**
- Each cell processes specific risk domains
- Circuit breakers protect against downstream service failures
- Fallback mechanisms ensure critical alerts are never lost
- Cell overlap provides redundancy for high-priority events

### 3. Unified Risk Data Platform

**Data Processing Cells:**
- Separate cells for different data domains (credit, market, operational)
- Circuit breakers for ETL job dependencies
- Graceful degradation when data sources are unavailable
- Cell-based scaling for varying data volumes

### 4. GenAI Risk Intelligence Platform

**AI Service Cells:**
- Separate cells for different AI workloads
- Circuit breakers for Bedrock and SageMaker endpoints
- Fallback to cached responses when AI services are unavailable
- Cell isolation prevents AI service failures from affecting other capabilities

### 5. API-First Integration Hub

**Integration Cells:**
- Cells organized by external system groups
- Circuit breakers for each integrated system
- Cached responses for degraded service scenarios
- Cell-based routing for load distribution

## Key Principles for Plan B Routing

### 1. Service Continuity Over Perfection
- **Never shut down services** when circuit breakers open
- Always provide some level of functionality, even if degraded
- Communicate service degradation clearly to consumers
- Maintain minimum viable service levels

### 2. Graceful Degradation Hierarchy
```
Level 1: Full Service (Primary path working)
Level 2: Reduced Features (Some dependencies failed)
Level 3: Basic Service (Core functionality only)
Level 4: Cached/Historical (Stale but available data)
Level 5: Manual Fallback (Human intervention)
```

### 3. Plan B Implementation Checklist
```
✓ Multiple fallback options defined for each service
✓ Fallback services tested regularly
✓ Clear degradation levels communicated
✓ Automatic routing to Plan B when circuits open
✓ Monitoring for Plan B usage patterns
✓ Recovery procedures to return to primary path
✓ Business stakeholder awareness of degraded modes
```

### 4. Monitoring Plan B Effectiveness
- Track Plan B activation frequency
- Monitor degraded service performance
- Measure customer impact during Plan B operations
- Analyze recovery times from Plan B to primary
- Validate Plan B services meet minimum SLAs

## Conclusion

Cell-based architecture and circuit breaker patterns are essential for building resilient risk management systems at Freddie Mac. These patterns provide:

**Key Benefits:**
- **Fault Isolation:** Failures are contained within individual cells
- **Graceful Degradation:** Systems continue operating with reduced capacity
- **Independent Scaling:** Each cell can scale based on demand
- **Faster Recovery:** Isolated failures are easier to diagnose and fix
- **Improved Reliability:** Overall system availability increases significantly

**Implementation Success Factors:**
- Proper cell sizing based on business domains and capacity requirements
- Appropriate circuit breaker thresholds for different service types
- Comprehensive monitoring and observability
- Regular chaos engineering testing
- Clear fallback and degradation strategies

**Next Steps:**
1. Start with pilot implementation in one risk domain
2. Establish monitoring and alerting baselines
3. Implement chaos engineering test suite
4. Gradually expand to other risk domains
5. Continuously optimize based on operational experience

This approach will significantly improve the resilience and reliability of Freddie Mac's risk management technology platform while enabling rapid innovation and scaling capabilities.