---
inclusion: always
priority: critical
---

# Code Quality and Anti-Patterns

## Core Principle
**Check Before You Code**: Always verify existing infrastructure, patterns, and libraries before implementing new functionality.

## Pre-Implementation Checklist (MANDATORY)

Before writing ANY code, you MUST:

- [ ] **Check for existing config system** - Does a ConfigManager/settings module exist?
- [ ] **Check for similar functionality** - Has this been implemented elsewhere?
- [ ] **Check shared libraries** - Is there reusable code in `shared/libraries/`?
- [ ] **Review existing patterns** - How do other modules solve this?
- [ ] **Check for existing tests** - What testing patterns are used?
- [ ] **Review documentation** - Are there architectural guidelines?

## Configuration Management (MANDATORY)

### Never Hard-Code These Values

**Environment-Specific**:
- ❌ AWS bucket names, regions, account IDs
- ❌ Database connection strings, endpoints
- ❌ API URLs, service endpoints
- ❌ File paths, directory locations
- ❌ AWS profile names, role ARNs

**Operational**:
- ❌ Timeouts, retry counts, delays
- ❌ Batch sizes, page limits
- ❌ Cache durations, TTLs
- ❌ Rate limits, throttle values

**Credentials** (NEVER):
- ❌ Passwords, API keys, tokens
- ❌ Access keys, secret keys
- ❌ Certificates, private keys

### Configuration Pattern

**✅ CORRECT - Use Configuration System**:
```python
# Python
from config import get_config
config = get_config()
bucket = config.get('storage.s3_bucket')
timeout = config.get('api.timeout', 30)
```

```typescript
// TypeScript
import { getConfig } from './config';
const config = getConfig();
const bucket = config.storage.s3Bucket;
const timeout = config.api.timeout ?? 30;
```

```rust
// Rust
use config::Config;
let config = Config::load()?;
let bucket = config.storage.s3_bucket;
let timeout = config.api.timeout.unwrap_or(30);
```

**❌ WRONG - Hard-Coded Values**:
```python
# Python - NEVER DO THIS
bucket = "jabil-alm-standards-library-dev"  # ❌
timeout = 30  # ❌
api_url = "https://api.example.com"  # ❌
```

### Configuration File Structure

**Environment-Specific Configs**:
```
config/
├── defaults.yaml          # Default values
├── development.yaml       # Dev overrides
├── staging.yaml          # Staging overrides
├── production.yaml       # Prod overrides
└── local.yaml           # Local dev (gitignored)
```

**Configuration Loading Priority**:
1. Environment variables (highest)
2. Environment-specific file (prod.yaml, dev.yaml)
3. Defaults file (defaults.yaml)
4. Code defaults (lowest)

## Code Smells Reference

Based on **Refactoring Guru** taxonomy from `ALM-SSDLC-Library/anti-patterns/smells-pdf/`

### Bloaters

Code that has grown so large it's hard to work with.

#### Long Method
**Smell**: Method longer than 10-15 lines
**Fix**: Extract Method, Replace Temp with Query
**Example**:
```python
# ❌ BAD - 50 line method
def process_document(doc):
    # ... 50 lines of mixed concerns
    
# ✅ GOOD - Extracted methods
def process_document(doc):
    validate_document(doc)
    extract_metadata(doc)
    transform_content(doc)
    save_document(doc)
```

#### Large Class
**Smell**: Class with too many fields/methods/responsibilities
**Fix**: Extract Class, Extract Subclass
**Example**:
```python
# ❌ BAD - God class
class DocumentProcessor:
    def validate(self): pass
    def parse(self): pass
    def transform(self): pass
    def save_to_s3(self): pass
    def send_email(self): pass
    def log_metrics(self): pass
    
# ✅ GOOD - Single responsibility
class DocumentValidator: pass
class DocumentParser: pass
class DocumentTransformer: pass
class DocumentStorage: pass
```

#### Primitive Obsession
**Smell**: Using primitives instead of small objects
**Fix**: Replace Data Value with Object, Replace Type Code with Class
**Example**:
```python
# ❌ BAD - Primitive obsession
def create_user(name: str, email: str, phone: str, zip: str):
    pass

# ✅ GOOD - Value objects
@dataclass
class Email:
    value: str
    def __post_init__(self):
        if '@' not in self.value:
            raise ValueError("Invalid email")

@dataclass
class PhoneNumber:
    value: str
    def __post_init__(self):
        if not re.match(r'^\d{3}-\d{3}-\d{4}$', self.value):
            raise ValueError("Invalid phone")

def create_user(name: str, email: Email, phone: PhoneNumber):
    pass
```

#### Long Parameter List
**Smell**: Method with more than 3-4 parameters
**Fix**: Replace Parameter with Method Call, Introduce Parameter Object
**Example**:
```python
# ❌ BAD - Too many parameters
def upload_file(bucket, key, file_path, region, profile, timeout, retry_count, metadata):
    pass

# ✅ GOOD - Configuration object
@dataclass
class UploadConfig:
    bucket: str
    region: str
    profile: str
    timeout: int = 30
    retry_count: int = 3
    metadata: Dict[str, str] = field(default_factory=dict)

def upload_file(key: str, file_path: str, config: UploadConfig):
    pass
```

#### Data Clumps
**Smell**: Same group of data items appearing together
**Fix**: Extract Class, Introduce Parameter Object
**Example**:
```python
# ❌ BAD - Data clumps
def create_address(street: str, city: str, state: str, zip: str): pass
def validate_address(street: str, city: str, state: str, zip: str): pass
def format_address(street: str, city: str, state: str, zip: str): pass

# ✅ GOOD - Address object
@dataclass
class Address:
    street: str
    city: str
    state: str
    zip_code: str

def create_address(address: Address): pass
def validate_address(address: Address): pass
def format_address(address: Address): pass
```

### Object-Orientation Abusers

Incomplete or incorrect application of OOP principles.

#### Switch Statements
**Smell**: Complex switch/if-else chains based on type
**Fix**: Replace Conditional with Polymorphism
**Example**:
```python
# ❌ BAD - Type-based conditionals
def process_document(doc_type: str, content: str):
    if doc_type == "pdf":
        # PDF processing
    elif doc_type == "word":
        # Word processing
    elif doc_type == "markdown":
        # Markdown processing

# ✅ GOOD - Polymorphism
class DocumentProcessor(ABC):
    @abstractmethod
    def process(self, content: str): pass

class PDFProcessor(DocumentProcessor):
    def process(self, content: str): pass

class WordProcessor(DocumentProcessor):
    def process(self, content: str): pass

class MarkdownProcessor(DocumentProcessor):
    def process(self, content: str): pass
```

#### Temporary Field
**Smell**: Field only used in certain circumstances
**Fix**: Extract Class, Replace Method with Method Object
**Example**:
```python
# ❌ BAD - Temporary fields
class Calculator:
    def __init__(self):
        self.temp_result = None  # Only used during calculation
        
    def calculate(self, x, y):
        self.temp_result = x + y
        return self.temp_result

# ✅ GOOD - Local variables or separate class
class Calculator:
    def calculate(self, x, y):
        result = x + y  # Local variable
        return result
```

#### Refused Bequest
**Smell**: Subclass uses only some inherited methods
**Fix**: Replace Inheritance with Delegation
**Example**:
```python
# ❌ BAD - Inheritance misuse
class Stack(list):  # Inherits all list methods
    def push(self, item):
        self.append(item)
    # But we don't want insert, extend, etc.

# ✅ GOOD - Composition
class Stack:
    def __init__(self):
        self._items = []  # Composition
    
    def push(self, item):
        self._items.append(item)
    
    def pop(self):
        return self._items.pop()
```

#### Alternative Classes with Different Interfaces
**Smell**: Classes do the same thing but have different method names
**Fix**: Rename Method, Extract Superclass
**Example**:
```python
# ❌ BAD - Different interfaces
class S3Storage:
    def put_file(self, key, data): pass

class LocalStorage:
    def save_file(self, path, data): pass

# ✅ GOOD - Common interface
class Storage(ABC):
    @abstractmethod
    def store(self, key: str, data: bytes): pass

class S3Storage(Storage):
    def store(self, key: str, data: bytes): pass

class LocalStorage(Storage):
    def store(self, key: str, data: bytes): pass
```

### Change Preventers

Changes require many small changes in many places.

#### Divergent Change
**Smell**: One class changed for different reasons
**Fix**: Extract Class
**Example**:
```python
# ❌ BAD - Multiple reasons to change
class User:
    def validate_email(self): pass
    def hash_password(self): pass
    def save_to_database(self): pass
    def send_welcome_email(self): pass
    def log_activity(self): pass

# ✅ GOOD - Single responsibility
class User:
    email: str
    password_hash: str

class UserValidator:
    def validate_email(self, email: str): pass

class UserRepository:
    def save(self, user: User): pass

class UserNotifier:
    def send_welcome_email(self, user: User): pass
```

#### Shotgun Surgery
**Smell**: One change requires many small changes everywhere
**Fix**: Move Method, Move Field, Inline Class
**Example**:
```python
# ❌ BAD - Scattered logic
class OrderProcessor:
    def calculate_tax(self, amount):
        return amount * 0.08  # Tax rate scattered

class InvoiceGenerator:
    def add_tax(self, amount):
        return amount * 0.08  # Duplicated

class ReportBuilder:
    def include_tax(self, amount):
        return amount * 0.08  # Duplicated

# ✅ GOOD - Centralized
class TaxCalculator:
    TAX_RATE = 0.08
    
    @classmethod
    def calculate(cls, amount):
        return amount * cls.TAX_RATE

class OrderProcessor:
    def calculate_tax(self, amount):
        return TaxCalculator.calculate(amount)
```

#### Parallel Inheritance Hierarchies
**Smell**: Creating subclass in one hierarchy requires creating subclass in another
**Fix**: Move Method, Move Field
**Example**:
```python
# ❌ BAD - Parallel hierarchies
class Employee: pass
class Manager(Employee): pass
class Developer(Employee): pass

class EmployeeReport: pass
class ManagerReport(EmployeeReport): pass
class DeveloperReport(EmployeeReport): pass

# ✅ GOOD - Single hierarchy with composition
class Employee:
    def generate_report(self) -> Report: pass

class Manager(Employee):
    def generate_report(self) -> Report:
        return ManagerReport(self)

class Report:
    def __init__(self, employee: Employee): pass
```

### Dispensables

Unnecessary code that should be removed.

#### Comments
**Smell**: Comments explaining what code does (not why)
**Fix**: Extract Method, Rename Method, Introduce Assertion
**Example**:
```python
# ❌ BAD - Explaining what
# Check if user is admin and has permission
if user.role == "admin" and user.permissions.get("delete"):
    delete_item()

# ✅ GOOD - Self-documenting
def can_delete_item(user: User) -> bool:
    return user.is_admin() and user.has_permission("delete")

if can_delete_item(user):
    delete_item()
```

#### Duplicate Code
**Smell**: Same code structure in multiple places
**Fix**: Extract Method, Pull Up Method, Form Template Method
**Example**:
```python
# ❌ BAD - Duplication
def process_pdf(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    # Process PDF
    return result

def process_word(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    # Process Word
    return result

# ✅ GOOD - Extract common code
def read_file(file_path: str) -> bytes:
    with open(file_path, 'rb') as f:
        return f.read()

def process_pdf(file_path):
    data = read_file(file_path)
    # Process PDF
    return result

def process_word(file_path):
    data = read_file(file_path)
    # Process Word
    return result
```

#### Lazy Class
**Smell**: Class doesn't do enough to justify existence
**Fix**: Inline Class, Collapse Hierarchy
**Example**:
```python
# ❌ BAD - Lazy class
class EmailValidator:
    def validate(self, email: str) -> bool:
        return '@' in email

# ✅ GOOD - Inline or enhance
def is_valid_email(email: str) -> bool:
    return '@' in email and '.' in email.split('@')[1]
```

#### Data Class
**Smell**: Class with only fields and getters/setters
**Fix**: Move Method, Extract Method, Hide Method
**Example**:
```python
# ❌ BAD - Anemic model
@dataclass
class Order:
    items: List[Item]
    total: float
    tax: float
    
# Behavior lives elsewhere
def calculate_order_total(order: Order):
    order.total = sum(item.price for item in order.items)
    order.tax = order.total * 0.08

# ✅ GOOD - Rich model
@dataclass
class Order:
    items: List[Item]
    
    def calculate_total(self) -> float:
        return sum(item.price for item in self.items)
    
    def calculate_tax(self) -> float:
        return self.calculate_total() * 0.08
    
    @property
    def total_with_tax(self) -> float:
        return self.calculate_total() + self.calculate_tax()
```

#### Dead Code
**Smell**: Unused variables, parameters, methods, classes
**Fix**: Delete it
**Example**:
```python
# ❌ BAD - Dead code
def process_document(doc, legacy_flag=False):  # legacy_flag never used
    result = parse_document(doc)
    old_result = legacy_parse(doc)  # Never used
    return result

# ✅ GOOD - Removed
def process_document(doc):
    return parse_document(doc)
```

#### Speculative Generality
**Smell**: Code created "just in case" for future needs
**Fix**: Collapse Hierarchy, Inline Class, Remove Parameter
**Example**:
```python
# ❌ BAD - Over-engineered
class DocumentProcessor(ABC):
    @abstractmethod
    def process(self, doc): pass
    
    @abstractmethod
    def process_async(self, doc): pass  # Not needed yet
    
    @abstractmethod
    def process_batch(self, docs): pass  # Not needed yet

# ✅ GOOD - YAGNI (You Aren't Gonna Need It)
class DocumentProcessor(ABC):
    @abstractmethod
    def process(self, doc): pass
```

### Couplers

Excessive coupling between classes.

#### Feature Envy
**Smell**: Method uses data from another class more than its own
**Fix**: Move Method, Extract Method
**Example**:
```python
# ❌ BAD - Feature envy
class Order:
    def __init__(self, customer):
        self.customer = customer
    
    def get_discount(self):
        if self.customer.loyalty_points > 100:
            return 0.1
        elif self.customer.years_member > 5:
            return 0.05
        return 0

# ✅ GOOD - Move to Customer
class Customer:
    def get_discount(self):
        if self.loyalty_points > 100:
            return 0.1
        elif self.years_member > 5:
            return 0.05
        return 0

class Order:
    def __init__(self, customer):
        self.customer = customer
    
    def get_discount(self):
        return self.customer.get_discount()
```

#### Inappropriate Intimacy
**Smell**: Classes access each other's internal fields/methods
**Fix**: Move Method, Move Field, Change Bidirectional Association to Unidirectional
**Example**:
```python
# ❌ BAD - Too intimate
class Order:
    def __init__(self):
        self.customer = None
    
    def finalize(self):
        self.customer._internal_credit -= self.total  # Accessing private field

# ✅ GOOD - Use public interface
class Customer:
    def deduct_credit(self, amount):
        self._internal_credit -= amount

class Order:
    def finalize(self):
        self.customer.deduct_credit(self.total)
```

#### Message Chains
**Smell**: Long chain of method calls
**Fix**: Hide Delegate
**Example**:
```python
# ❌ BAD - Message chain
customer = order.get_customer().get_address().get_city().get_name()

# ✅ GOOD - Hide delegate
class Order:
    def get_customer_city(self):
        return self.customer.get_city_name()

customer_city = order.get_customer_city()
```

#### Middle Man
**Smell**: Class delegates most work to another class
**Fix**: Remove Middle Man, Inline Method
**Example**:
```python
# ❌ BAD - Useless middle man
class OrderManager:
    def __init__(self):
        self.order_repository = OrderRepository()
    
    def get_order(self, id):
        return self.order_repository.get_order(id)
    
    def save_order(self, order):
        return self.order_repository.save_order(order)

# ✅ GOOD - Use repository directly
order_repository = OrderRepository()
order = order_repository.get_order(id)
```

## Dependency Injection Pattern

**Always inject dependencies, never instantiate inside classes**.

### ❌ WRONG - Hard Dependencies
```python
class DocumentProcessor:
    def __init__(self):
        self.storage = S3Storage()  # ❌ Hard-coded dependency
        self.config = ConfigManager()  # ❌ Hard-coded dependency
```

### ✅ CORRECT - Dependency Injection
```python
class DocumentProcessor:
    def __init__(self, storage: Storage, config: ConfigManager):
        self.storage = storage  # ✅ Injected
        self.config = config  # ✅ Injected

# Usage
config = get_config()
storage = S3Storage(config) if config.use_s3 else LocalStorage(config)
processor = DocumentProcessor(storage, config)
```

## SOLID Principles

### Single Responsibility Principle (SRP)
**A class should have one, and only one, reason to change.**

```python
# ❌ BAD - Multiple responsibilities
class User:
    def save_to_database(self): pass
    def send_email(self): pass
    def generate_report(self): pass

# ✅ GOOD - Single responsibility
class User:
    pass  # Just data

class UserRepository:
    def save(self, user: User): pass

class UserNotifier:
    def send_email(self, user: User): pass

class UserReportGenerator:
    def generate(self, user: User): pass
```

### Open/Closed Principle (OCP)
**Open for extension, closed for modification.**

```python
# ❌ BAD - Modifying existing code
def calculate_discount(customer_type: str, amount: float):
    if customer_type == "regular":
        return amount * 0.05
    elif customer_type == "premium":
        return amount * 0.10
    # Adding new type requires modifying this function

# ✅ GOOD - Extension without modification
class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float: pass

class RegularDiscount(DiscountStrategy):
    def calculate(self, amount: float) -> float:
        return amount * 0.05

class PremiumDiscount(DiscountStrategy):
    def calculate(self, amount: float) -> float:
        return amount * 0.10

# Add new discount types without modifying existing code
class VIPDiscount(DiscountStrategy):
    def calculate(self, amount: float) -> float:
        return amount * 0.20
```

### Liskov Substitution Principle (LSP)
**Subtypes must be substitutable for their base types.**

```python
# ❌ BAD - Violates LSP
class Rectangle:
    def set_width(self, width): self.width = width
    def set_height(self, height): self.height = height

class Square(Rectangle):
    def set_width(self, width):
        self.width = width
        self.height = width  # Breaks LSP

# ✅ GOOD - Separate hierarchies
class Shape(ABC):
    @abstractmethod
    def area(self) -> float: pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height

class Square(Shape):
    def __init__(self, side):
        self.side = side
    
    def area(self) -> float:
        return self.side * self.side
```

### Interface Segregation Principle (ISP)
**Clients shouldn't depend on interfaces they don't use.**

```python
# ❌ BAD - Fat interface
class Worker(ABC):
    @abstractmethod
    def work(self): pass
    @abstractmethod
    def eat(self): pass
    @abstractmethod
    def sleep(self): pass

class Robot(Worker):
    def work(self): pass
    def eat(self): pass  # Robots don't eat!
    def sleep(self): pass  # Robots don't sleep!

# ✅ GOOD - Segregated interfaces
class Workable(ABC):
    @abstractmethod
    def work(self): pass

class Eatable(ABC):
    @abstractmethod
    def eat(self): pass

class Sleepable(ABC):
    @abstractmethod
    def sleep(self): pass

class Human(Workable, Eatable, Sleepable):
    def work(self): pass
    def eat(self): pass
    def sleep(self): pass

class Robot(Workable):
    def work(self): pass
```

### Dependency Inversion Principle (DIP)
**Depend on abstractions, not concretions.**

```python
# ❌ BAD - Depends on concrete class
class OrderProcessor:
    def __init__(self):
        self.email_service = GmailService()  # Concrete dependency

# ✅ GOOD - Depends on abstraction
class EmailService(ABC):
    @abstractmethod
    def send(self, to: str, subject: str, body: str): pass

class GmailService(EmailService):
    def send(self, to: str, subject: str, body: str): pass

class OrderProcessor:
    def __init__(self, email_service: EmailService):
        self.email_service = email_service  # Abstract dependency
```

## Testing Anti-Patterns

### Test Smells to Avoid

#### Mystery Guest
**Smell**: Test depends on external resources not visible in test
**Fix**: Make dependencies explicit
```python
# ❌ BAD
def test_upload():
    uploader = S3Uploader()  # Reads config from file
    uploader.upload("test.txt")

# ✅ GOOD
def test_upload():
    config = TestConfig(bucket="test-bucket")
    uploader = S3Uploader(config)
    uploader.upload("test.txt")
```

#### Test Code Duplication
**Smell**: Same setup code in multiple tests
**Fix**: Use fixtures/setup methods
```python
# ❌ BAD
def test_upload():
    config = create_config()
    storage = S3Storage(config)
    # test code

def test_download():
    config = create_config()
    storage = S3Storage(config)
    # test code

# ✅ GOOD
@pytest.fixture
def storage():
    config = create_config()
    return S3Storage(config)

def test_upload(storage):
    # test code

def test_download(storage):
    # test code
```

## Code Review Checklist

Before submitting code for review:

- [ ] No hard-coded configuration values
- [ ] Dependencies injected, not instantiated
- [ ] Methods under 15 lines
- [ ] Classes have single responsibility
- [ ] No duplicate code
- [ ] No dead code or commented-out code
- [ ] Self-documenting code (minimal comments)
- [ ] Proper error handling
- [ ] Tests included
- [ ] No code smells from this document

## References

- **Code Smells**: `ALM-SSDLC-Library/anti-patterns/smells-pdf/`
- **Refactoring Guru**: https://refactoring.guru/refactoring/smells
- **Clean Code**: Robert C. Martin
- **Refactoring**: Martin Fowler

---

**Status**: Active | **Priority**: Critical | **Updated**: 2025-11-30 | **Owner**: Platform Architecture Team
