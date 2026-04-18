# Architecture Diagrams: Cell-Based Architecture with Circuit Breakers

## Diagram 1: Cell-Based Architecture Overview

```mermaid
graph TB
    subgraph "Client Layer"
        Client[Client Requests]
    end
    
    subgraph "Routing Layer"
        Router[Consistent Hash Router<br/>borrower_id % num_cells]
    end
    
    subgraph "Cell 1: Borrowers 1-10,000"
        subgraph "Compute Layer 1"
            EKS1[EKS Pods<br/>3 replicas]
        end
        subgraph "Data Layer 1"
            RDS1[(RDS Instance<br/>Dedicated)]
            Cache1[(ElastiCache<br/>Dedicated)]
        end
        subgraph "Network Layer 1"
            ALB1[Application<br/>Load Balancer]
        end
    end
    
    subgraph "Cell 2: Borrowers 10,001-20,000"
        subgraph "Compute Layer 2"
            EKS2[EKS Pods<br/>3 replicas]
        end
        subgraph "Data Layer 2"
            RDS2[(RDS Instance<br/>Dedicated)]
            Cache2[(ElastiCache<br/>Dedicated)]
        end
        subgraph "Network Layer 2"
            ALB2[Application<br/>Load Balancer]
        end
    end
    
    subgraph "Cell 3: Borrowers 20,001-30,000"
        subgraph "Compute Layer 3"
            EKS3[EKS Pods<br/>3 replicas]
        end
        subgraph "Data Layer 3"
            RDS3[(RDS Instance<br/>Dedicated)]
            Cache3[(ElastiCache<br/>Dedicated)]
        end
        subgraph "Network Layer 3"
            ALB3[Application<br/>Load Balancer]
        end
    end
    
    subgraph "Shared Infrastructure"
        Kafka[Kafka/MSK<br/>Event Stream]
        CloudWatch[CloudWatch<br/>Monitoring]
        IAM[IAM/KMS<br/>Security]
    end
    
    Client --> Router
    Router -->|Hash: 0-33%| ALB1
    Router -->|Hash: 34-66%| ALB2
    Router -->|Hash: 67-100%| ALB3
    
    ALB1 --> EKS1
    EKS1 --> RDS1
    EKS1 --> Cache1
    
    ALB2 --> EKS2
    EKS2 --> RDS2
    EKS2 --> Cache2
    
    ALB3 --> EKS3
    EKS3 --> RDS3
    EKS3 --> Cache3
    
    EKS1 -.-> Kafka
    EKS2 -.-> Kafka
    EKS3 -.-> Kafka
    
    EKS1 -.-> CloudWatch
    EKS2 -.-> CloudWatch
    EKS3 -.-> CloudWatch
    
    style Cell1 fill:#e1f5e1
    style Cell2 fill:#e1f5e1
    style Cell3 fill:#e1f5e1
    style RDS1 fill:#ff9999
    style RDS2 fill:#99ff99
    style RDS3 fill:#99ff99
    style Cache1 fill:#ff9999
    
    classDef failedCell fill:#ffcccc,stroke:#ff0000,stroke-width:3px
    class Cell1 failedCell
```

**Key Points:**
- Each cell is completely isolated with dedicated resources
- Consistent hashing routes requests deterministically
- Cell 1 failure (red) doesn't affect Cell 2 and Cell 3 (green)
- Shared infrastructure sits below cells for cross-cutting concerns

---

## Diagram 2: Circuit Breaker State Machine

```mermaid
stateDiagram-v2
    [*] --> Closed
    
    Closed --> Open: Failure threshold exceeded<br/>(e.g., 5 failures)
    Closed --> Closed: Request succeeds<br/>(failure_count = 0)
    Closed --> Closed: Request fails<br/>(failure_count++)
    
    Open --> HalfOpen: Recovery timeout elapsed<br/>(e.g., 60 seconds)
    Open --> Open: Requests blocked<br/>(route to Plan B)
    
    HalfOpen --> Closed: Test request succeeds<br/>(service recovered)
    HalfOpen --> Open: Test request fails<br/>(service still down)
    
    note right of Closed
        Normal Operation
        - All requests flow through
        - Monitor failure rate
        - Track failure count
    end note
    
    note right of Open
        Failure Mode
        - Block requests to primary
        - Route to Plan B
        - Wait for recovery timeout
    end note
    
    note right of HalfOpen
        Testing Recovery
        - Allow limited requests
        - Test if service recovered
        - Decide: close or reopen
    end note
```

**State Transitions:**
- **Closed → Open**: Too many failures (threshold exceeded)
- **Open → Half-Open**: Recovery timeout elapsed, test if service recovered
- **Half-Open → Closed**: Test successful, service recovered
- **Half-Open → Open**: Test failed, service still down

---

## Diagram 3: Circuit Breaker with Fallback Routing (Plan B)

```mermaid
graph TB
    Request[Incoming Request<br/>Credit Score Calculation]
    
    subgraph "Circuit Breaker"
        CB{Circuit<br/>State?}
    end
    
    subgraph "Primary Path"
        Primary[SageMaker ML Model<br/>Full Feature Set]
        PrimaryResult[850-point score<br/>+ risk factors]
    end
    
    subgraph "Plan B1"
        Backup[Backup ML Model<br/>Different AZ]
        BackupResult[850-point score<br/>Reduced features]
    end
    
    subgraph "Plan B2"
        Rules[Rules-Based Engine<br/>Business Logic]
        RulesResult[850-point score<br/>Logic only]
    end
    
    subgraph "Plan B3"
        Cache[Cached Historical Score<br/>Last Calculation]
        CacheResult[Last score<br/>+ staleness indicator]
    end
    
    subgraph "Plan B4"
        Manual[Manual Review Queue<br/>Human Underwriter]
        ManualResult[Queued for<br/>manual review]
    end
    
    Request --> CB
    
    CB -->|Closed<br/>Normal| Primary
    CB -->|Open<br/>Primary Failed| Backup
    
    Primary -->|Success| PrimaryResult
    Primary -->|Failure| Backup
    
    Backup -->|Success| BackupResult
    Backup -->|Failure| Rules
    
    Rules -->|Success| RulesResult
    Rules -->|Failure| Cache
    
    Cache -->|Success| CacheResult
    Cache -->|Failure| Manual
    
    Manual --> ManualResult
    
    PrimaryResult --> Response[Response to Client]
    BackupResult --> Response
    RulesResult --> Response
    CacheResult --> Response
    ManualResult --> Response
    
    style Primary fill:#99ff99
    style Backup fill:#ffff99
    style Rules fill:#ffcc99
    style Cache fill:#ffaa99
    style Manual fill:#ff9999
    style CB fill:#9999ff
```

**Fallback Hierarchy:**
1. **Primary**: Full ML model (best accuracy, highest latency)
2. **Plan B1**: Backup ML model (good accuracy, medium latency)
3. **Plan B2**: Rules engine (acceptable accuracy, low latency)
4. **Plan B3**: Cached score (stale but fast)
5. **Plan B4**: Manual queue (slowest but always works)

**Key Principle**: Never return an error. Always provide *something*.

---

## Diagram 4: Complete System - Cells + Circuit Breakers

```mermaid
graph TB
    Client[Client Request<br/>Borrower ID: 12345]
    
    subgraph "Routing Layer"
        Router[Consistent Hash Router<br/>hash % 3 = Cell 2]
    end
    
    subgraph "Cell 2: Borrowers 10,001-20,000"
        ALB2[Load Balancer]
        
        subgraph "Application Layer"
            App2[Credit Risk Service<br/>EKS Pod]
        end
        
        subgraph "Circuit Breakers"
            CB_ML{ML Circuit<br/>3 failures<br/>30s timeout}
            CB_DB{DB Circuit<br/>5 failures<br/>60s timeout}
            CB_Cache{Cache Circuit<br/>2 failures<br/>15s timeout}
        end
        
        subgraph "Primary Dependencies"
            ML2[SageMaker<br/>Endpoint]
            DB2[(RDS<br/>Instance)]
            Cache2[(ElastiCache<br/>Cluster)]
        end
        
        subgraph "Fallback Dependencies"
            ML_Backup[Backup ML<br/>Model]
            DB_Replica[(Read<br/>Replica)]
            DB_Direct[(Direct DB<br/>No Cache)]
        end
    end
    
    subgraph "Cell 1: Borrowers 1-10,000"
        Cell1[Cell 1<br/>Healthy ✓]
    end
    
    subgraph "Cell 3: Borrowers 20,001-30,000"
        Cell3[Cell 3<br/>Healthy ✓]
    end
    
    Client --> Router
    Router --> ALB2
    ALB2 --> App2
    
    App2 --> CB_ML
    App2 --> CB_DB
    App2 --> CB_Cache
    
    CB_ML -->|Closed| ML2
    CB_ML -->|Open| ML_Backup
    
    CB_DB -->|Closed| DB2
    CB_DB -->|Open| DB_Replica
    
    CB_Cache -->|Closed| Cache2
    CB_Cache -->|Open| DB_Direct
    
    style Cell2 fill:#e1f5e1
    style Cell1 fill:#e1f5e1
    style Cell3 fill:#e1f5e1
    style CB_ML fill:#ffff99
    style CB_DB fill:#99ff99
    style CB_Cache fill:#99ff99
    style ML2 fill:#ff9999
    style ML_Backup fill:#ffff99
    
    classDef openCircuit fill:#ffcccc,stroke:#ff0000,stroke-width:2px
    class CB_ML openCircuit
```

**System Behavior:**
- Request routed to Cell 2 via consistent hashing
- ML Circuit is OPEN (red) → routes to backup ML model
- DB Circuit is CLOSED (green) → uses primary database
- Cache Circuit is CLOSED (green) → uses primary cache
- Cell 1 and Cell 3 unaffected by Cell 2's ML issues

---

## Diagram 5: Cascading Failure Prevention

```mermaid
sequenceDiagram
    participant Client
    participant Cell2 as Cell 2 Service
    participant CB as Circuit Breaker
    participant Primary as Primary ML Model
    participant Backup as Backup ML Model
    
    Note over Client,Backup: Normal Operation (Circuit Closed)
    Client->>Cell2: Request 1
    Cell2->>CB: Check circuit
    CB->>Primary: Forward request
    Primary-->>CB: Success
    CB-->>Cell2: Result
    Cell2-->>Client: 200 OK
    
    Note over Client,Backup: Primary Starts Failing
    Client->>Cell2: Request 2
    Cell2->>CB: Check circuit
    CB->>Primary: Forward request
    Primary--xCB: Timeout (failure 1/3)
    CB-->>Cell2: Error
    Cell2-->>Client: 500 Error
    
    Client->>Cell2: Request 3
    Cell2->>CB: Check circuit
    CB->>Primary: Forward request
    Primary--xCB: Timeout (failure 2/3)
    CB-->>Cell2: Error
    Cell2-->>Client: 500 Error
    
    Client->>Cell2: Request 4
    Cell2->>CB: Check circuit
    CB->>Primary: Forward request
    Primary--xCB: Timeout (failure 3/3)
    CB->>CB: OPEN CIRCUIT
    CB-->>Cell2: Circuit Open
    Cell2-->>Client: 500 Error
    
    Note over Client,Backup: Circuit Open - Route to Backup
    Client->>Cell2: Request 5
    Cell2->>CB: Check circuit
    CB->>CB: Circuit is OPEN
    CB->>Backup: Route to backup
    Backup-->>CB: Success
    CB-->>Cell2: Result (degraded)
    Cell2-->>Client: 200 OK (Plan B)
    
    Note over Client,Backup: Subsequent Requests Use Backup
    Client->>Cell2: Request 6
    Cell2->>CB: Check circuit
    CB->>Backup: Route to backup
    Backup-->>CB: Success
    CB-->>Cell2: Result (degraded)
    Cell2-->>Client: 200 OK (Plan B)
    
    Note over Client,Backup: Recovery Timeout - Test Primary
    CB->>CB: 30s timeout elapsed
    CB->>CB: Enter HALF-OPEN
    Client->>Cell2: Request 7
    Cell2->>CB: Check circuit
    CB->>Primary: Test request
    Primary-->>CB: Success!
    CB->>CB: CLOSE CIRCUIT
    CB-->>Cell2: Result
    Cell2-->>Client: 200 OK
    
    Note over Client,Backup: Back to Normal Operation
    Client->>Cell2: Request 8
    Cell2->>CB: Check circuit
    CB->>Primary: Forward request
    Primary-->>CB: Success
    CB-->>Cell2: Result
    Cell2-->>Client: 200 OK
```

**Timeline:**
1. **Requests 1**: Normal operation, circuit closed
2. **Requests 2-4**: Primary fails, circuit tracks failures, opens after threshold
3. **Requests 5-6**: Circuit open, all requests route to backup (no cascading failure!)
4. **Request 7**: Recovery timeout, circuit tests primary, succeeds, closes circuit
5. **Request 8+**: Back to normal operation

**Key Insight**: Circuit breaker prevents cascading failures by stopping requests to failing service and routing to backup. System stays available throughout.

---

## Usage in Article

Insert these diagrams at the following sections:

1. **Diagram 1** → After "What Makes a Cell?" section
2. **Diagram 2** → After "The Three States" section
3. **Diagram 3** → After "Plan B: Never Shut Down, Always Route" section
4. **Diagram 4** → After "Real-World Application: Credit Risk Assessment" section
5. **Diagram 5** → After "The Problem: Cascading Failures Are Expensive" section

## Rendering

These diagrams use Mermaid syntax and can be rendered:
- **Medium**: Use image export from Mermaid Live Editor (https://mermaid.live)
- **GitHub**: Native Mermaid rendering in markdown
- **Documentation**: Most modern doc platforms support Mermaid

## Export Instructions

1. Copy diagram code to https://mermaid.live
2. Adjust styling/colors as needed
3. Export as PNG or SVG
4. Upload to Medium article
5. Add alt text describing the diagram for accessibility
