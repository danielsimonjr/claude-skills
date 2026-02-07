# Real-World Refactoring Examples

## Example 1: The God Function → Composed Functions

### Original Code (The Problem)
```python
def process_customer_order(customer_id, items, payment_info):
    """This function has grown to 200+ lines and does everything"""
    
    # Validate customer (30 lines)
    cursor = db.execute("SELECT * FROM customers WHERE id = ?", customer_id)
    customer = cursor.fetchone()
    if not customer:
        return {"error": "Customer not found"}
    if customer['status'] == 'suspended':
        return {"error": "Account suspended"}
    if customer['credit_score'] < 500 and payment_info['method'] == 'credit':
        return {"error": "Credit not approved"}
    
    # Validate items (40 lines)
    if not items:
        return {"error": "No items"}
    total = 0
    for item in items:
        product = db.execute("SELECT * FROM products WHERE id = ?", item['id']).fetchone()
        if not product:
            return {"error": f"Product {item['id']} not found"}
        if product['stock'] < item['quantity']:
            return {"error": f"Insufficient stock for {product['name']}"}
        if product['status'] != 'active':
            return {"error": f"Product {product['name']} unavailable"}
        total += product['price'] * item['quantity']
    
    # Apply discounts (50 lines)
    discount = 0
    if customer['loyalty_tier'] == 'gold':
        discount = total * 0.15
    elif customer['loyalty_tier'] == 'silver':
        discount = total * 0.10
    elif customer['loyalty_tier'] == 'bronze':
        discount = total * 0.05
    
    if total > 1000:
        discount += 50
    
    if customer['birthday'] and is_birthday_month(customer['birthday']):
        discount += total * 0.05
    
    final_total = total - discount
    
    # Process payment (40 lines)
    if payment_info['method'] == 'credit':
        # 20 lines of credit card processing
        pass
    elif payment_info['method'] == 'paypal':
        # 20 lines of PayPal processing
        pass
    
    # Create order record (20 lines)
    order_id = generate_order_id()
    db.execute("""
        INSERT INTO orders (id, customer_id, total, discount, status)
        VALUES (?, ?, ?, ?, ?)
    """, order_id, customer_id, final_total, discount, 'pending')
    
    for item in items:
        db.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (?, ?, ?, ?)
        """, order_id, item['id'], item['quantity'], item['price'])
    
    # Send confirmation (20 lines)
    send_email(
        customer['email'],
        f"Order {order_id} confirmed",
        f"Thank you for your order of ${final_total}"
    )
    
    return {"success": True, "order_id": order_id, "total": final_total}
```

### Refactored Code (The Solution)

```python
# Main orchestration - crystal clear flow
def process_customer_order(customer_id: int, items: List[OrderItem], 
                          payment_info: PaymentInfo) -> OrderResult:
    """
    Process a customer order through validation, pricing, payment, and confirmation.
    
    This is the main orchestration function - it should read like a recipe.
    """
    customer = validate_customer(customer_id, payment_info)
    validated_items = validate_order_items(items)
    pricing = calculate_order_pricing(customer, validated_items)
    
    payment_result = process_payment(payment_info, pricing.final_total)
    if not payment_result.success:
        return OrderResult.failure(payment_result.error)
    
    order = create_order_record(customer, validated_items, pricing)
    send_order_confirmation(customer, order)
    
    return OrderResult.success(order.id, pricing.final_total)


# Each extracted function is focused and testable
def validate_customer(customer_id: int, payment_info: PaymentInfo) -> Customer:
    """Validate customer exists and is eligible to place orders."""
    customer = Customer.find(customer_id)
    
    if not customer:
        raise ValidationError("Customer not found")
    
    if customer.is_suspended():
        raise ValidationError("Account suspended")
    
    if payment_info.method == PaymentMethod.CREDIT:
        if not customer.is_credit_approved():
            raise ValidationError("Credit not approved")
    
    return customer


def validate_order_items(items: List[OrderItem]) -> List[ValidatedItem]:
    """Validate all items are available and in stock."""
    if not items:
        raise ValidationError("Order must contain at least one item")
    
    validated = []
    for item in items:
        product = Product.find(item.product_id)
        
        if not product:
            raise ValidationError(f"Product {item.product_id} not found")
        
        if not product.is_available():
            raise ValidationError(f"{product.name} is not available")
        
        if not product.has_stock(item.quantity):
            raise ValidationError(f"Insufficient stock for {product.name}")
        
        validated.append(ValidatedItem(product, item.quantity))
    
    return validated


class OrderPricing:
    """Value object representing order pricing breakdown."""
    def __init__(self, subtotal: Decimal, discount: Decimal):
        self.subtotal = subtotal
        self.discount = discount
        self.final_total = subtotal - discount


def calculate_order_pricing(customer: Customer, 
                           items: List[ValidatedItem]) -> OrderPricing:
    """Calculate subtotal, discounts, and final total."""
    subtotal = sum(item.product.price * item.quantity for item in items)
    discount = calculate_total_discount(customer, subtotal)
    return OrderPricing(subtotal, discount)


def calculate_total_discount(customer: Customer, subtotal: Decimal) -> Decimal:
    """Calculate all applicable discounts for this order."""
    discount = Decimal(0)
    
    # Loyalty tier discount
    discount += calculate_loyalty_discount(customer.loyalty_tier, subtotal)
    
    # Large order discount
    if subtotal > 1000:
        discount += Decimal(50)
    
    # Birthday discount
    if customer.is_birthday_month():
        discount += subtotal * Decimal('0.05')
    
    return discount


def calculate_loyalty_discount(tier: LoyaltyTier, subtotal: Decimal) -> Decimal:
    """Calculate discount based on customer loyalty tier."""
    rates = {
        LoyaltyTier.GOLD: Decimal('0.15'),
        LoyaltyTier.SILVER: Decimal('0.10'),
        LoyaltyTier.BRONZE: Decimal('0.05'),
    }
    return subtotal * rates.get(tier, Decimal(0))


# Type-safe payment processing with strategy pattern
class PaymentProcessor:
    """Base class for payment processors."""
    def process(self, amount: Decimal) -> PaymentResult:
        raise NotImplementedError


class CreditCardProcessor(PaymentProcessor):
    def process(self, amount: Decimal) -> PaymentResult:
        # Credit card specific logic
        pass


class PayPalProcessor(PaymentProcessor):
    def process(self, amount: Decimal) -> PaymentResult:
        # PayPal specific logic
        pass


def process_payment(payment_info: PaymentInfo, amount: Decimal) -> PaymentResult:
    """Process payment using appropriate payment method."""
    processors = {
        PaymentMethod.CREDIT: CreditCardProcessor(payment_info.card_details),
        PaymentMethod.PAYPAL: PayPalProcessor(payment_info.paypal_token),
    }
    
    processor = processors.get(payment_info.method)
    if not processor:
        return PaymentResult.failure("Unsupported payment method")
    
    return processor.process(amount)


def create_order_record(customer: Customer, items: List[ValidatedItem], 
                        pricing: OrderPricing) -> Order:
    """Create order and order items records in database."""
    order = Order.create(
        customer_id=customer.id,
        subtotal=pricing.subtotal,
        discount=pricing.discount,
        total=pricing.final_total,
        status=OrderStatus.PENDING
    )
    
    for item in items:
        OrderItem.create(
            order_id=order.id,
            product_id=item.product.id,
            quantity=item.quantity,
            price=item.product.price
        )
    
    return order


def send_order_confirmation(customer: Customer, order: Order):
    """Send order confirmation email to customer."""
    email_service.send(
        to=customer.email,
        subject=f"Order {order.id} Confirmed",
        template="order_confirmation",
        context={
            "customer_name": customer.name,
            "order_id": order.id,
            "total": order.total,
        }
    )
```

**Why This Is Better:**
1. **Readability**: The main function reads like a table of contents
2. **Testability**: Each function can be tested in isolation
3. **Maintainability**: Changes are localized (e.g., discount logic is in one place)
4. **Reusability**: Functions like `validate_customer` can be used elsewhere
5. **Type Safety**: Using domain types catches errors at compile time
6. **Single Responsibility**: Each function does exactly one thing

---

## Example 2: The Performance Disaster → Cache-Friendly Code

### Original Code (The Problem)
```cpp
// Particle system with terrible cache performance
class ParticleSystem {
    struct Particle {
        Vector3 position;
        Vector3 velocity;
        Vector3 acceleration;
        float mass;
        float lifetime;
        float age;
        Color color;
        bool active;
    };
    
    std::vector<Particle> particles;
    
    void update(float dt) {
        // PROBLEM 1: Iterating over all particles, even inactive ones
        for (auto& p : particles) {
            if (!p.active) continue;
            
            // PROBLEM 2: Random memory access pattern
            p.age += dt;
            if (p.age > p.lifetime) {
                p.active = false;
                continue;
            }
            
            // PROBLEM 3: Loading entire particle when we only need position/velocity
            p.velocity += p.acceleration * dt;
            p.position += p.velocity * dt;
            
            // PROBLEM 4: Branching in hot loop
            if (p.position.y < 0) {
                p.position.y = 0;
                p.velocity.y *= -0.5f;
            }
        }
    }
    
    void render() {
        // PROBLEM 5: Iterating again, loading all data again
        for (const auto& p : particles) {
            if (p.active) {
                drawParticle(p.position, p.color);
            }
        }
    }
};
```

### Refactored Code (The Solution)

```cpp
// Structure of Arrays (SoA) for cache-friendly access
class ParticleSystem {
private:
    size_t capacity;
    size_t count;  // Number of active particles
    
    // Hot data (accessed every frame) - tightly packed
    std::vector<Vector3> positions;
    std::vector<Vector3> velocities;
    
    // Warm data (accessed every frame but separate)
    std::vector<Vector3> accelerations;
    
    // Cold data (accessed infrequently) - separate
    std::vector<float> masses;
    std::vector<float> lifetimes;
    std::vector<float> ages;
    std::vector<Color> colors;
    
public:
    ParticleSystem(size_t max_particles) : capacity(max_particles), count(0) {
        // Pre-allocate to avoid reallocations
        positions.reserve(capacity);
        velocities.reserve(capacity);
        accelerations.reserve(capacity);
        masses.reserve(capacity);
        lifetimes.reserve(capacity);
        ages.reserve(capacity);
        colors.reserve(capacity);
    }
    
    void update(float dt) {
        // Process only active particles (first 'count' elements)
        // All active particles are packed at the beginning
        
        // Update ages and remove dead particles
        size_t write_idx = 0;
        for (size_t read_idx = 0; read_idx < count; ++read_idx) {
            ages[read_idx] += dt;
            
            // Keep alive particles, compact array
            if (ages[read_idx] <= lifetimes[read_idx]) {
                if (write_idx != read_idx) {
                    // Swap all data for this particle
                    std::swap(positions[write_idx], positions[read_idx]);
                    std::swap(velocities[write_idx], velocities[read_idx]);
                    std::swap(accelerations[write_idx], accelerations[read_idx]);
                    std::swap(ages[write_idx], ages[read_idx]);
                    std::swap(lifetimes[write_idx], lifetimes[read_idx]);
                    std::swap(colors[write_idx], colors[read_idx]);
                }
                ++write_idx;
            }
        }
        count = write_idx;
        
        // Physics update - operates on contiguous memory
        // Modern CPUs can prefetch this beautifully
        for (size_t i = 0; i < count; ++i) {
            velocities[i] += accelerations[i] * dt;
            positions[i] += velocities[i] * dt;
        }
        
        // Ground collision - separate pass, but still vectorizable
        for (size_t i = 0; i < count; ++i) {
            if (positions[i].y < 0.0f) {
                positions[i].y = 0.0f;
                velocities[i].y *= -0.5f;
            }
        }
    }
    
    void render() {
        // Only iterate over active particles
        // Position and color data are contiguous
        for (size_t i = 0; i < count; ++i) {
            drawParticle(positions[i], colors[i]);
        }
    }
    
    // SIMD-optimized version (even faster)
    void update_simd(float dt) {
        const size_t simd_width = 4;
        const size_t simd_count = count / simd_width;
        
        // Process 4 particles at once using SIMD
        for (size_t i = 0; i < simd_count * simd_width; i += simd_width) {
            __m128 dt_vec = _mm_set1_ps(dt);
            
            // Load 4 velocities and 4 accelerations
            __m128 vx = _mm_loadu_ps(&velocities[i].x);
            __m128 ax = _mm_loadu_ps(&accelerations[i].x);
            
            // v += a * dt (for 4 particles at once)
            vx = _mm_add_ps(vx, _mm_mul_ps(ax, dt_vec));
            _mm_storeu_ps(&velocities[i].x, vx);
            
            // Similar for y and z components...
        }
        
        // Handle remaining particles scalar-style
        for (size_t i = simd_count * simd_width; i < count; ++i) {
            velocities[i] += accelerations[i] * dt;
            positions[i] += velocities[i] * dt;
        }
    }
};
```

**Performance Improvements:**
- **10-100x faster**: Data layout matches access pattern
- **Better cache utilization**: Sequential memory access
- **SIMD-friendly**: Can process 4-8 particles at once
- **No wasted iterations**: Only process active particles
- **Branch prediction**: Branches moved out of hot loops where possible

**Why This Works:**
1. **Data-Oriented Design**: Structure matches how it's used, not how we think about it
2. **Cache Lines**: Modern CPUs load 64 bytes at a time - we use all of it
3. **Prefetching**: Sequential access allows CPU to prefetch correctly
4. **SIMD**: Parallel processing of multiple particles
5. **No Holes**: Compacting array eliminates gaps from dead particles

---

## Example 3: The Clever Abstraction → Simple Code

### Original Code (The Problem)
```java
// Over-engineered "flexible" system that nobody understands
public interface DataProcessor<T, R> {
    R process(T input);
}

public interface DataTransformer<T, U> {
    U transform(T data);
}

public interface DataValidator<T> {
    boolean validate(T data);
}

public class ProcessingPipeline<T, U, R> {
    private DataValidator<T> validator;
    private DataTransformer<T, U> transformer;
    private DataProcessor<U, R> processor;
    
    public ProcessingPipeline(DataValidator<T> validator,
                             DataTransformer<T, U> transformer,
                             DataProcessor<U, R> processor) {
        this.validator = validator;
        this.transformer = transformer;
        this.processor = processor;
    }
    
    public Optional<R> execute(T input) {
        if (!validator.validate(input)) {
            return Optional.empty();
        }
        U transformed = transformer.transform(input);
        R result = processor.process(transformed);
        return Optional.of(result);
    }
}

// Usage requires creating multiple classes and wiring them together
DataValidator<String> validator = new StringValidator();
DataTransformer<String, Integer> transformer = new StringToIntTransformer();
DataProcessor<Integer, String> processor = new IntToStringProcessor();
ProcessingPipeline<String, Integer, String> pipeline = 
    new ProcessingPipeline<>(validator, transformer, processor);
Optional<String> result = pipeline.execute("123");
```

### Refactored Code (The Solution)

```java
// Simple, clear, does exactly what's needed
public class OrderProcessor {
    public Order processOrderRequest(OrderRequest request) {
        // Validation - clear and explicit
        if (request.items().isEmpty()) {
            throw new InvalidOrderException("Order must contain items");
        }
        if (request.customerId() <= 0) {
            throw new InvalidOrderException("Invalid customer ID");
        }
        
        // Transformation - obvious what's happening
        List<OrderLine> lines = request.items().stream()
            .map(this::createOrderLine)
            .collect(toList());
        
        // Processing - straightforward
        BigDecimal total = calculateTotal(lines);
        
        return new Order(
            generateOrderId(),
            request.customerId(),
            lines,
            total,
            OrderStatus.PENDING
        );
    }
    
    private OrderLine createOrderLine(OrderRequestItem item) {
        Product product = productRepository.find(item.productId());
        return new OrderLine(product, item.quantity(), product.price());
    }
    
    private BigDecimal calculateTotal(List<OrderLine> lines) {
        return lines.stream()
            .map(line -> line.price().multiply(BigDecimal.valueOf(line.quantity())))
            .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
}
```

**Why This Is Better:**
1. **Obviousness**: Anyone can understand what this does in 30 seconds
2. **Debuggability**: Can step through with a debugger easily
3. **Modifiability**: Changes are straightforward
4. **No Premature Abstraction**: Solves the problem at hand, not hypothetical future problems
5. **Performance**: No abstraction overhead

**Carmack's Wisdom**: "Sometimes the elegant implementation is just a function. Not a method. Not a class. Not a framework. Just a function."

---

## Example 4: The Allocation Storm → Zero-Allocation Code

### Original Code (The Problem)
```go
// Allocates millions of objects per second
func processRequests(requests []Request) []Response {
    responses := []Response{}  // Allocates
    
    for _, req := range requests {
        // Allocates a new string every iteration
        sanitized := strings.ToLower(strings.TrimSpace(req.Data))
        
        // Allocates a map every iteration
        parsed := parseData(sanitized)
        
        // Allocates response every iteration
        resp := Response{
            ID: req.ID,
            Result: computeResult(parsed),  // More allocations
            Timestamp: time.Now(),  // Allocates
        }
        
        responses = append(responses, resp)  // May allocate
    }
    
    return responses
}

func parseData(data string) map[string]string {
    result := make(map[string]string)  // Allocates
    parts := strings.Split(data, ",")  // Allocates slice
    for _, part := range parts {
        kv := strings.Split(part, ":")  // Allocates slice
        if len(kv) == 2 {
            result[kv[0]] = kv[1]
        }
    }
    return result
}
```

### Refactored Code (The Solution)

```go
// Pre-allocate and reuse everything possible
type RequestProcessor struct {
    // Reusable buffers
    buffer strings.Builder
    parseBuffer []string
    resultMap map[string]string
    
    // Pre-allocated response slice
    responses []Response
}

func NewRequestProcessor(maxRequests int) *RequestProcessor {
    return &RequestProcessor{
        buffer: strings.Builder{},
        parseBuffer: make([]string, 0, 16),
        resultMap: make(map[string]string, 16),
        responses: make([]Response, 0, maxRequests),
    }
}

func (p *RequestProcessor) ProcessRequests(requests []Request) []Response {
    // Reuse existing slice, just reset length
    p.responses = p.responses[:0]
    
    for i := range requests {
        req := &requests[i]  // No copy, use pointer
        
        // Reuse string builder instead of allocating
        p.buffer.Reset()
        sanitized := p.sanitizeInPlace(req.Data)
        
        // Reuse map, just clear it
        p.clearMap()
        p.parseDataInPlace(sanitized)
        
        // Response goes directly into pre-allocated slice
        p.responses = append(p.responses, Response{
            ID: req.ID,
            Result: p.computeResultInPlace(),
            Timestamp: timeNow(),  // Use cached time for this batch
        })
    }
    
    return p.responses
}

func (p *RequestProcessor) sanitizeInPlace(data string) string {
    p.buffer.Reset()
    
    // Avoid allocations from ToLower and TrimSpace
    inSpace := true
    for _, r := range data {
        if unicode.IsSpace(r) {
            if !inSpace {
                p.buffer.WriteRune(' ')
                inSpace = true
            }
            continue
        }
        p.buffer.WriteRune(unicode.ToLower(r))
        inSpace = false
    }
    
    return p.buffer.String()
}

func (p *RequestProcessor) clearMap() {
    // Clearing is faster than allocating a new map
    for k := range p.resultMap {
        delete(p.resultMap, k)
    }
}

func (p *RequestProcessor) parseDataInPlace(data string) {
    // Parse directly into reused map
    start := 0
    for i := 0; i < len(data); i++ {
        if data[i] == ',' || i == len(data)-1 {
            if i == len(data)-1 {
                i++
            }
            p.parseKeyValue(data[start:i])
            start = i + 1
        }
    }
}

func (p *RequestProcessor) parseKeyValue(kv string) {
    for i := 0; i < len(kv); i++ {
        if kv[i] == ':' {
            key := kv[:i]
            value := kv[i+1:]
            p.resultMap[key] = value
            return
        }
    }
}

// Cache timestamp for the batch
var cachedTime time.Time
var lastTimeUpdate time.Time

func timeNow() time.Time {
    now := time.Now()
    // Update cached time only every millisecond
    if now.Sub(lastTimeUpdate) > time.Millisecond {
        cachedTime = now
        lastTimeUpdate = now
    }
    return cachedTime
}
```

**Performance Impact:**
- **100x fewer allocations**: Reuse instead of allocate
- **10x faster**: Less GC pressure, better cache utilization
- **Predictable latency**: No GC pauses during processing

---

## Key Takeaways

1. **Linus would approve of**: Clear logic flow, obvious correctness, data structures that match usage
2. **Carmack would approve of**: Understanding the machine, minimizing state, measuring not guessing

The best refactoring makes code:
- Simpler to understand
- Easier to modify
- Faster to execute
- Harder to break

**Most important**: Each of these examples can be understood by reading the code, not documentation. That's the hallmark of great code.
