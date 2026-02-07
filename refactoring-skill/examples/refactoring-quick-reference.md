# Refactoring Quick Reference

## Common Code Smells & Fixes

### 1. Long Method/Function
**Smell**: Function > 50 lines, does multiple things, hard to name clearly
**Fix**: Extract Method - break into smaller, well-named functions
```python
# BEFORE
def process_order(order):
    # validate (10 lines)
    # calculate totals (15 lines)
    # apply discounts (20 lines)
    # save to database (10 lines)
    # send confirmation (10 lines)

# AFTER  
def process_order(order):
    validate_order(order)
    totals = calculate_order_totals(order)
    totals = apply_discounts(totals, order.customer)
    save_order(order, totals)
    send_confirmation_email(order)
```

### 2. Duplicated Code
**Smell**: Same or very similar code in multiple places
**Fix**: Extract Method, Pull Up Method, or Template Method Pattern
```cpp
// BEFORE
void drawCircle() {
    setupCanvas();
    setColor(BLUE);
    // draw circle logic
    cleanup();
}

void drawSquare() {
    setupCanvas();
    setColor(RED);
    // draw square logic
    cleanup();
}

// AFTER
void draw(Shape shape, Color color) {
    setupCanvas();
    setColor(color);
    shape.draw();
    cleanup();
}
```

### 3. Long Parameter List
**Smell**: Function takes > 3-4 parameters
**Fix**: Introduce Parameter Object or Builder Pattern
```java
// BEFORE
void createUser(String name, String email, int age, 
                String address, String phone, String role)

// AFTER
class UserData {
    String name, email, address, phone, role;
    int age;
}
void createUser(UserData data)
```

### 4. Complex Conditional
**Smell**: Nested ifs, long boolean expressions, multiple && and ||
**Fix**: Extract Method, Decompose Conditional, Guard Clauses
```javascript
// BEFORE
if ((user.role === 'admin' || user.role === 'moderator') && 
    user.verified && 
    (subscription.active && subscription.level > 2) &&
    !user.banned) {
    // do something
}

// AFTER
if (canAccessFeature(user, subscription)) {
    // do something
}

function canAccessFeature(user, subscription) {
    if (!hasRequiredRole(user)) return false;
    if (!user.verified) return false;
    if (!hasActiveSubscription(subscription)) return false;
    if (user.banned) return false;
    return true;
}
```

### 5. Primitive Obsession
**Smell**: Using primitives instead of domain types
**Fix**: Replace Data Value with Object
```rust
// BEFORE
fn validate_email(email: &str) -> bool { ... }
fn send_to(email: &str) { ... }

// AFTER
struct Email(String);

impl Email {
    fn new(s: String) -> Result<Email, ValidationError> {
        // validation here ensures Email is always valid
        if is_valid_email(&s) {
            Ok(Email(s))
        } else {
            Err(ValidationError)
        }
    }
}

fn send_to(email: &Email) { ... }
```

### 6. Data Clumps
**Smell**: Same group of data items appears together repeatedly
**Fix**: Extract Class
```go
// BEFORE
func drawLine(x1, y1, x2, y2 int)
func distance(x1, y1, x2, y2 int) float64

// AFTER
type Point struct {
    X, Y int
}

func drawLine(start, end Point)
func distance(start, end Point) float64
```

### 7. Switch/Case Statements
**Smell**: Switch on type code, same switch in multiple places
**Fix**: Replace Type Code with Polymorphism
```typescript
// BEFORE
function calculateBonus(employee: Employee): number {
    switch(employee.type) {
        case 'engineer':
            return employee.salary * 0.1;
        case 'manager':
            return employee.salary * 0.2 + employee.teamSize * 1000;
        case 'executive':
            return employee.salary * 0.3 + companyProfit * 0.01;
    }
}

// AFTER
abstract class Employee {
    abstract calculateBonus(): number;
}

class Engineer extends Employee {
    calculateBonus(): number {
        return this.salary * 0.1;
    }
}

class Manager extends Employee {
    calculateBonus(): number {
        return this.salary * 0.2 + this.teamSize * 1000;
    }
}
```

### 8. Temporary Field
**Smell**: Field only used in certain circumstances
**Fix**: Extract Class or Replace Method with Method Object
```python
# BEFORE
class OrderProcessor:
    def __init__(self):
        self.temp_total = 0  # Only used during calculate()
        self.temp_discount = 0
        
    def calculate(self, order):
        self.temp_total = sum(item.price for item in order.items)
        self.temp_discount = self.temp_total * 0.1
        return self.temp_total - self.temp_discount

# AFTER
class OrderCalculation:
    def __init__(self, order):
        self.total = sum(item.price for item in order.items)
        self.discount = self.total * 0.1
        
    def final_total(self):
        return self.total - self.discount

class OrderProcessor:
    def calculate(self, order):
        calc = OrderCalculation(order)
        return calc.final_total()
```

### 9. Message Chains
**Smell**: `a.getB().getC().getD().doSomething()`
**Fix**: Hide Delegate
```cpp
// BEFORE
customer.getAddress().getCity().getRegion().getTaxRate()

// AFTER
class Customer {
    float getTaxRate() {
        return address.getTaxRate();
    }
};

class Address {
    float getTaxRate() {
        return city.getTaxRate();
    }
};
```

### 10. Comments Explaining Code
**Smell**: Comment needed to explain what code does
**Fix**: Extract Method with descriptive name, or Rename Variable
```c
// BEFORE
// Check if customer is eligible for discount
if (c.orders > 10 && c.total > 1000 && c.years > 2) {
    // ...
}

// AFTER
if (isEligibleForLoyaltyDiscount(customer)) {
    // ...
}

bool isEligibleForLoyaltyDiscount(Customer c) {
    return c.orders > 10 && 
           c.total > 1000 && 
           c.years > 2;
}
```

## Performance Patterns

### 1. Cache Expensive Computations
```python
# BEFORE
class Circle:
    def area(self):
        return 3.14159 * self.radius * self.radius

# AFTER
class Circle:
    def __init__(self, radius):
        self._radius = radius
        self._area = None
    
    def area(self):
        if self._area is None:
            self._area = 3.14159 * self._radius * self._radius
        return self._area
```

### 2. Avoid Repeated Allocation
```c++
// BEFORE - allocates string every iteration
for (int i = 0; i < 1000000; i++) {
    std::string msg = "Processing: " + std::to_string(i);
    process(msg);
}

// AFTER - reuse buffer
std::string buffer;
buffer.reserve(256);
for (int i = 0; i < 1000000; i++) {
    buffer = "Processing: ";
    buffer += std::to_string(i);
    process(buffer);
}
```

### 3. Use Appropriate Data Structure
```python
# BEFORE - O(n) lookup
items = []
if item in items:  # Linear search
    ...

# AFTER - O(1) lookup
items = set()
if item in items:  # Hash lookup
    ...
```

### 4. Batch Database Operations
```javascript
// BEFORE - N queries
for (const user of users) {
    await db.update('users', { lastSeen: now }, { id: user.id });
}

// AFTER - 1 query
const ids = users.map(u => u.id);
await db.update('users', { lastSeen: now }, { id: { $in: ids } });
```

### 5. Lazy Initialization
```java
// BEFORE - always loads even if not used
public class Report {
    private Data data = loadExpensiveData();
}

// AFTER - load only when needed
public class Report {
    private Data data = null;
    
    public Data getData() {
        if (data == null) {
            data = loadExpensiveData();
        }
        return data;
    }
}
```

## Readability Patterns

### 1. Guard Clauses vs Nested Ifs
```go
// BEFORE
func processPayment(payment Payment) error {
    if payment.Amount > 0 {
        if payment.Account != nil {
            if payment.Account.Balance >= payment.Amount {
                // main logic here
            } else {
                return errors.New("insufficient funds")
            }
        } else {
            return errors.New("no account")
        }
    } else {
        return errors.New("invalid amount")
    }
}

// AFTER
func processPayment(payment Payment) error {
    if payment.Amount <= 0 {
        return errors.New("invalid amount")
    }
    if payment.Account == nil {
        return errors.New("no account")
    }
    if payment.Account.Balance < payment.Amount {
        return errors.New("insufficient funds")
    }
    
    // main logic here - no nesting!
}
```

### 2. Explain Complex Boolean with Function
```rust
// BEFORE
if (date.day() == 1 && date.month() == 1) || 
   (date.day() == 4 && date.month() == 7) ||
   (date.day() == 25 && date.month() == 12) {
    // ...
}

// AFTER
if is_holiday(date) {
    // ...
}

fn is_holiday(date: Date) -> bool {
    matches!((date.day(), date.month()),
        (1, 1) | (4, 7) | (25, 12))
}
```

### 3. Replace Magic Numbers with Named Constants
```c
// BEFORE
if (status == 3) {
    discount = price * 0.15;
}

// AFTER
const int STATUS_GOLD_MEMBER = 3;
const float GOLD_DISCOUNT_RATE = 0.15;

if (status == STATUS_GOLD_MEMBER) {
    discount = price * GOLD_DISCOUNT_RATE;
}
```

### 4. Positive Conditionals
```python
# BEFORE - double negative
if not is_invalid(user):
    process(user)

# AFTER - positive condition
if is_valid(user):
    process(user)
```

### 5. Consistent Naming Conventions
```typescript
// BEFORE - inconsistent
function get_user(id: number) { ... }
function FetchOrders(userId: number) { ... }
function LoadFromDB(table: string) { ... }

// AFTER - consistent
function getUser(id: number) { ... }
function getOrders(userId: number) { ... }
function loadFromDatabase(table: string) { ... }
```

## Architecture Patterns

### 1. Dependency Injection vs Tight Coupling
```java
// BEFORE - tight coupling
class UserService {
    private MySQLDatabase db = new MySQLDatabase();
}

// AFTER - dependency injection
class UserService {
    private Database db;
    
    UserService(Database db) {
        this.db = db;
    }
}
```

### 2. Strategy Pattern for Algorithm Selection
```python
# BEFORE
def calculate_shipping(weight, method):
    if method == "standard":
        return weight * 0.5
    elif method == "express":
        return weight * 1.5
    elif method == "overnight":
        return weight * 3.0

# AFTER
class ShippingStrategy:
    def calculate(self, weight): pass

class StandardShipping(ShippingStrategy):
    def calculate(self, weight): return weight * 0.5

class ExpressShipping(ShippingStrategy):
    def calculate(self, weight): return weight * 1.5

strategies = {
    "standard": StandardShipping(),
    "express": ExpressShipping(),
}

def calculate_shipping(weight, method):
    return strategies[method].calculate(weight)
```

### 3. Factory Pattern for Object Creation
```cpp
// BEFORE
Monster* createMonster(string type) {
    if (type == "goblin") {
        Monster* m = new Monster();
        m->health = 50;
        m->damage = 10;
        return m;
    }
    // ... repeated for each type
}

// AFTER
class MonsterFactory {
public:
    static unique_ptr<Monster> createGoblin() {
        auto m = make_unique<Goblin>();
        m->health = 50;
        m->damage = 10;
        return m;
    }
};
```

## Testing Patterns

### 1. Arrange-Act-Assert
```csharp
// BEFORE - unclear structure
[Test]
public void TestUserCreation() {
    var user = new User("John");
    Assert.AreEqual("John", user.Name);
    user.SetEmail("john@example.com");
    Assert.IsTrue(user.IsValid());
}

// AFTER - clear AAA structure
[Test]
public void CreateUser_WithValidData_SetsNameCorrectly() {
    // Arrange
    string expectedName = "John";
    
    // Act
    var user = new User(expectedName);
    
    // Assert
    Assert.AreEqual(expectedName, user.Name);
}
```

### 2. One Assertion Per Test (when practical)
```javascript
// BEFORE - multiple concerns
test('user validation', () => {
    const user = new User('John', 'john@example.com');
    expect(user.name).toBe('John');
    expect(user.email).toBe('john@example.com');
    expect(user.isValid()).toBe(true);
});

// AFTER - focused tests
test('user stores name correctly', () => {
    const user = new User('John', 'john@example.com');
    expect(user.name).toBe('John');
});

test('user stores email correctly', () => {
    const user = new User('John', 'john@example.com');
    expect(user.email).toBe('john@example.com');
});

test('user with valid data is valid', () => {
    const user = new User('John', 'john@example.com');
    expect(user.isValid()).toBe(true);
});
```

## Red Flags Checklist

When reviewing code, watch for:
- [ ] Function/method > 50 lines
- [ ] Function with > 3 parameters
- [ ] Nesting depth > 3
- [ ] Duplicate code blocks
- [ ] Magic numbers without names
- [ ] Boolean flags passed to functions
- [ ] Comments explaining "what" not "why"
- [ ] Classes with > 10 methods
- [ ] Global mutable state
- [ ] Exceptions used for flow control
- [ ] Empty catch blocks
- [ ] Overly clever code
- [ ] Inconsistent naming
- [ ] Mixed abstraction levels

## Refactoring Safety Net

Before refactoring:
1. ✓ Tests exist and pass
2. ✓ You understand what the code does
3. ✓ You have version control
4. ✓ Changes are small and incremental
5. ✓ You can explain why it's better

After refactoring:
1. ✓ All tests still pass
2. ✓ Performance hasn't regressed
3. ✓ Code is simpler or measurably faster
4. ✓ Diff is reviewable
5. ✓ You'd be happy debugging this at 2 AM
