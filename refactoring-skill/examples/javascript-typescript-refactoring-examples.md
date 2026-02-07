# JavaScript & TypeScript Refactoring Examples

## Example 1: Callback Hell → Async/Await Paradise

### Original Code (The Problem)
```javascript
// Classic callback pyramid of doom
function processUserData(userId, callback) {
    fetchUser(userId, function(err, user) {
        if (err) {
            callback(err);
            return;
        }
        
        fetchUserPosts(user.id, function(err, posts) {
            if (err) {
                callback(err);
                return;
            }
            
            fetchComments(posts[0].id, function(err, comments) {
                if (err) {
                    callback(err);
                    return;
                }
                
                updateAnalytics(user.id, posts.length, function(err) {
                    if (err) {
                        callback(err);
                        return;
                    }
                    
                    sendNotification(user.email, posts.length, function(err) {
                        if (err) {
                            callback(err);
                            return;
                        }
                        
                        callback(null, {
                            user: user,
                            posts: posts,
                            comments: comments
                        });
                    });
                });
            });
        });
    });
}
```

### Refactored Code (The Solution)

```typescript
// Modern TypeScript with async/await
interface User {
    id: string;
    email: string;
    name: string;
}

interface Post {
    id: string;
    userId: string;
    title: string;
    content: string;
}

interface Comment {
    id: string;
    postId: string;
    text: string;
}

interface UserDataResult {
    user: User;
    posts: Post[];
    comments: Comment[];
}

async function processUserData(userId: string): Promise<UserDataResult> {
    // Clear, linear flow - reads top to bottom
    const user = await fetchUser(userId);
    const posts = await fetchUserPosts(user.id);
    const comments = await fetchComments(posts[0].id);
    
    // Parallel operations that don't depend on each other
    await Promise.all([
        updateAnalytics(user.id, posts.length),
        sendNotification(user.email, posts.length)
    ]);
    
    return { user, posts, comments };
}

// With proper error handling
async function processUserDataSafe(userId: string): Promise<UserDataResult> {
    try {
        const user = await fetchUser(userId);
        const posts = await fetchUserPosts(user.id);
        
        if (posts.length === 0) {
            throw new Error('User has no posts');
        }
        
        const comments = await fetchComments(posts[0].id);
        
        // Fire and forget analytics (don't wait)
        updateAnalytics(user.id, posts.length).catch(err => 
            console.error('Analytics update failed:', err)
        );
        
        // Must wait for notification
        await sendNotification(user.email, posts.length);
        
        return { user, posts, comments };
        
    } catch (error) {
        // Add context to error
        throw new Error(
            `Failed to process user data for ${userId}: ${error.message}`
        );
    }
}

// Even better: with timeout and retry logic
async function processUserDataRobust(
    userId: string,
    options: { timeout?: number; retries?: number } = {}
): Promise<UserDataResult> {
    const { timeout = 5000, retries = 3 } = options;
    
    return withTimeout(
        withRetry(
            async () => {
                const user = await fetchUser(userId);
                const posts = await fetchUserPosts(user.id);
                
                if (posts.length === 0) {
                    return { user, posts, comments: [] };
                }
                
                const comments = await fetchComments(posts[0].id);
                
                await Promise.allSettled([
                    updateAnalytics(user.id, posts.length),
                    sendNotification(user.email, posts.length)
                ]);
                
                return { user, posts, comments };
            },
            retries
        ),
        timeout
    );
}

// Utility functions
async function withTimeout<T>(
    promise: Promise<T>,
    ms: number
): Promise<T> {
    const timeout = new Promise<never>((_, reject) =>
        setTimeout(() => reject(new Error(`Timeout after ${ms}ms`)), ms)
    );
    return Promise.race([promise, timeout]);
}

async function withRetry<T>(
    fn: () => Promise<T>,
    retries: number
): Promise<T> {
    try {
        return await fn();
    } catch (error) {
        if (retries <= 0) throw error;
        await delay(1000 * (4 - retries)); // Exponential backoff
        return withRetry(fn, retries - 1);
    }
}

function delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
}
```

**Why This Is Better:**
- **Readability**: Linear flow instead of nested callbacks
- **Error Handling**: Try/catch instead of error-first callbacks everywhere
- **Composability**: Easy to add timeout, retry, parallel execution
- **Type Safety**: TypeScript catches errors at compile time
- **Maintainability**: Easy to add/remove steps in the flow

---

## Example 2: Mutating State → Immutable Updates

### Original Code (The Problem)
```javascript
// Mutations everywhere - hard to track state changes
class ShoppingCart {
    constructor() {
        this.items = [];
        this.discounts = [];
        this.total = 0;
    }
    
    addItem(item) {
        // Mutates array
        this.items.push(item);
        // Mutates total
        this.total += item.price * item.quantity;
        
        // Side effect: modifies item
        item.addedAt = Date.now();
        
        // Mutates discount array
        if (this.total > 100) {
            this.discounts.push({ type: 'bulk', amount: 10 });
            this.total -= 10;
        }
    }
    
    removeItem(itemId) {
        // Mutates array
        const index = this.items.findIndex(i => i.id === itemId);
        if (index !== -1) {
            const item = this.items[index];
            this.items.splice(index, 1);
            // Mutates total
            this.total -= item.price * item.quantity;
            
            // Mutates discount array
            if (this.total <= 100) {
                this.discounts = this.discounts.filter(d => d.type !== 'bulk');
            }
        }
    }
    
    updateQuantity(itemId, newQuantity) {
        // Mutates item
        const item = this.items.find(i => i.id === itemId);
        if (item) {
            const oldQuantity = item.quantity;
            item.quantity = newQuantity;
            // Mutates total
            this.total += item.price * (newQuantity - oldQuantity);
        }
    }
}
```

### Refactored Code (The Solution)

```typescript
// Immutable, functional approach
interface CartItem {
    readonly id: string;
    readonly name: string;
    readonly price: number;
    readonly quantity: number;
    readonly addedAt: number;
}

interface Discount {
    readonly type: string;
    readonly amount: number;
}

interface Cart {
    readonly items: ReadonlyArray<CartItem>;
    readonly discounts: ReadonlyArray<Discount>;
    readonly subtotal: number;
    readonly total: number;
}

// Pure functions that return new state
function createEmptyCart(): Cart {
    return {
        items: [],
        discounts: [],
        subtotal: 0,
        total: 0
    };
}

function addItem(cart: Cart, item: Omit<CartItem, 'addedAt'>): Cart {
    const newItem: CartItem = {
        ...item,
        addedAt: Date.now()
    };
    
    const items = [...cart.items, newItem];
    const subtotal = calculateSubtotal(items);
    const discounts = calculateDiscounts(subtotal, cart.discounts);
    const total = subtotal - sumDiscounts(discounts);
    
    return { items, discounts, subtotal, total };
}

function removeItem(cart: Cart, itemId: string): Cart {
    const items = cart.items.filter(item => item.id !== itemId);
    const subtotal = calculateSubtotal(items);
    const discounts = calculateDiscounts(subtotal, cart.discounts);
    const total = subtotal - sumDiscounts(discounts);
    
    return { items, discounts, subtotal, total };
}

function updateQuantity(cart: Cart, itemId: string, quantity: number): Cart {
    const items = cart.items.map(item =>
        item.id === itemId
            ? { ...item, quantity }
            : item
    );
    
    const subtotal = calculateSubtotal(items);
    const discounts = calculateDiscounts(subtotal, cart.discounts);
    const total = subtotal - sumDiscounts(discounts);
    
    return { items, discounts, subtotal, total };
}

// Pure calculation functions
function calculateSubtotal(items: ReadonlyArray<CartItem>): number {
    return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

function calculateDiscounts(
    subtotal: number,
    existingDiscounts: ReadonlyArray<Discount>
): ReadonlyArray<Discount> {
    const discounts = [...existingDiscounts];
    
    // Add bulk discount if applicable
    if (subtotal > 100 && !discounts.some(d => d.type === 'bulk')) {
        return [...discounts, { type: 'bulk', amount: 10 }];
    }
    
    // Remove bulk discount if no longer applicable
    if (subtotal <= 100) {
        return discounts.filter(d => d.type !== 'bulk');
    }
    
    return discounts;
}

function sumDiscounts(discounts: ReadonlyArray<Discount>): number {
    return discounts.reduce((sum, discount) => sum + discount.amount, 0);
}

// Usage with immutable updates
let cart = createEmptyCart();

cart = addItem(cart, { 
    id: '1', 
    name: 'Widget', 
    price: 50, 
    quantity: 2 
});

cart = addItem(cart, { 
    id: '2', 
    name: 'Gadget', 
    price: 30, 
    quantity: 1 
});

cart = updateQuantity(cart, '1', 3);

// Easy to implement undo/redo
class CartHistory {
    private history: Cart[] = [];
    private currentIndex = -1;
    
    push(cart: Cart): void {
        // Remove any future states
        this.history = this.history.slice(0, this.currentIndex + 1);
        this.history.push(cart);
        this.currentIndex++;
    }
    
    undo(): Cart | null {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            return this.history[this.currentIndex];
        }
        return null;
    }
    
    redo(): Cart | null {
        if (this.currentIndex < this.history.length - 1) {
            this.currentIndex++;
            return this.history[this.currentIndex];
        }
        return null;
    }
}

// With React hooks
function useCart() {
    const [cart, setCart] = useState(createEmptyCart());
    
    const add = useCallback((item: Omit<CartItem, 'addedAt'>) => {
        setCart(currentCart => addItem(currentCart, item));
    }, []);
    
    const remove = useCallback((itemId: string) => {
        setCart(currentCart => removeItem(currentCart, itemId));
    }, []);
    
    const update = useCallback((itemId: string, quantity: number) => {
        setCart(currentCart => updateQuantity(currentCart, itemId, quantity));
    }, []);
    
    return { cart, add, remove, update };
}
```

**Why This Is Better:**
- **Predictability**: No hidden mutations, easy to reason about
- **Testability**: Pure functions are trivial to test
- **Time Travel**: Undo/redo becomes simple
- **React Integration**: Works perfectly with React's reconciliation
- **Debugging**: Easy to log state changes
- **Concurrency**: No race conditions from shared mutable state

---

## Example 3: Prototype Soup → Modern Classes & Composition

### Original Code (The Problem)
```javascript
// Old-school prototype-based inheritance mess
function Animal(name) {
    this.name = name;
    this.energy = 100;
}

Animal.prototype.eat = function(amount) {
    this.energy += amount;
    console.log(this.name + ' ate. Energy: ' + this.energy);
};

Animal.prototype.sleep = function(hours) {
    this.energy += hours * 10;
    console.log(this.name + ' slept ' + hours + ' hours');
};

function Dog(name, breed) {
    Animal.call(this, name);
    this.breed = breed;
}

// Prototype chain setup
Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog;

Dog.prototype.bark = function() {
    this.energy -= 5;
    console.log(this.name + ' barked! Energy: ' + this.energy);
};

Dog.prototype.fetch = function() {
    this.energy -= 15;
    console.log(this.name + ' fetched the ball!');
};

function Cat(name, color) {
    Animal.call(this, name);
    this.color = color;
}

Cat.prototype = Object.create(Animal.prototype);
Cat.prototype.constructor = Cat;

Cat.prototype.meow = function() {
    this.energy -= 3;
    console.log(this.name + ' meowed!');
};

Cat.prototype.scratch = function() {
    this.energy -= 8;
    console.log(this.name + ' scratched something!');
};
```

### Refactored Code (The Solution)

```typescript
// Modern class-based approach with composition
interface Energy {
    readonly current: number;
    readonly max: number;
}

interface LivingBeing {
    readonly name: string;
    readonly energy: Energy;
}

// Composition over inheritance - reusable behaviors
class EnergyManager {
    constructor(
        private current: number = 100,
        private readonly max: number = 100
    ) {}
    
    consume(amount: number): EnergyManager {
        const newCurrent = Math.max(0, this.current - amount);
        return new EnergyManager(newCurrent, this.max);
    }
    
    restore(amount: number): EnergyManager {
        const newCurrent = Math.min(this.max, this.current + amount);
        return new EnergyManager(newCurrent, this.max);
    }
    
    getCurrent(): number {
        return this.current;
    }
    
    getPercentage(): number {
        return (this.current / this.max) * 100;
    }
    
    isEmpty(): boolean {
        return this.current === 0;
    }
}

// Base class with common functionality
abstract class Animal {
    protected energyManager: EnergyManager;
    
    constructor(
        public readonly name: string,
        initialEnergy: number = 100
    ) {
        this.energyManager = new EnergyManager(initialEnergy);
    }
    
    eat(amount: number): void {
        this.energyManager = this.energyManager.restore(amount);
        console.log(`${this.name} ate. Energy: ${this.getEnergy()}%`);
    }
    
    sleep(hours: number): void {
        this.energyManager = this.energyManager.restore(hours * 10);
        console.log(`${this.name} slept ${hours} hours. Energy: ${this.getEnergy()}%`);
    }
    
    protected consumeEnergy(amount: number): void {
        if (this.energyManager.isEmpty()) {
            throw new Error(`${this.name} is too tired!`);
        }
        this.energyManager = this.energyManager.consume(amount);
    }
    
    getEnergy(): number {
        return Math.round(this.energyManager.getPercentage());
    }
    
    abstract makeSound(): void;
}

// Specific implementations
class Dog extends Animal {
    constructor(
        name: string,
        public readonly breed: string
    ) {
        super(name);
    }
    
    makeSound(): void {
        this.bark();
    }
    
    bark(): void {
        this.consumeEnergy(5);
        console.log(`${this.name} (${this.breed}) barked! Energy: ${this.getEnergy()}%`);
    }
    
    fetch(): void {
        this.consumeEnergy(15);
        console.log(`${this.name} fetched the ball! Energy: ${this.getEnergy()}%`);
    }
}

class Cat extends Animal {
    constructor(
        name: string,
        public readonly color: string
    ) {
        super(name);
    }
    
    makeSound(): void {
        this.meow();
    }
    
    meow(): void {
        this.consumeEnergy(3);
        console.log(`${this.name} (${this.color} cat) meowed! Energy: ${this.getEnergy()}%`);
    }
    
    scratch(): void {
        this.consumeEnergy(8);
        console.log(`${this.name} scratched something! Energy: ${this.getEnergy()}%`);
    }
}

// Even better: composition with interfaces (no inheritance)
interface Soundable {
    makeSound(): void;
}

interface Feedable {
    eat(amount: number): void;
}

interface Restable {
    sleep(hours: number): void;
}

// Behaviors as separate, composable objects
class VoiceBox implements Soundable {
    constructor(
        private readonly name: string,
        private readonly sound: string,
        private readonly energyCost: number
    ) {}
    
    makeSound(): void {
        console.log(`${this.name} says: ${this.sound}!`);
    }
    
    getEnergyCost(): number {
        return this.energyCost;
    }
}

// Composition-based animal
class ModernAnimal implements Soundable, Feedable, Restable {
    private energyManager: EnergyManager;
    
    constructor(
        public readonly name: string,
        private readonly voice: VoiceBox,
        private readonly traits: Map<string, any> = new Map()
    ) {
        this.energyManager = new EnergyManager();
    }
    
    makeSound(): void {
        this.consumeEnergy(this.voice.getEnergyCost());
        this.voice.makeSound();
    }
    
    eat(amount: number): void {
        this.energyManager = this.energyManager.restore(amount);
    }
    
    sleep(hours: number): void {
        this.energyManager = this.energyManager.restore(hours * 10);
    }
    
    private consumeEnergy(amount: number): void {
        this.energyManager = this.energyManager.consume(amount);
    }
    
    getTrait<T>(key: string): T | undefined {
        return this.traits.get(key) as T | undefined;
    }
}

// Factory functions for easy creation
function createDog(name: string, breed: string): ModernAnimal {
    const voice = new VoiceBox(name, 'Woof', 5);
    const traits = new Map([
        ['breed', breed],
        ['canFetch', true]
    ]);
    return new ModernAnimal(name, voice, traits);
}

function createCat(name: string, color: string): ModernAnimal {
    const voice = new VoiceBox(name, 'Meow', 3);
    const traits = new Map([
        ['color', color],
        ['canScratch', true]
    ]);
    return new ModernAnimal(name, voice, traits);
}

// Usage
const dog = createDog('Buddy', 'Golden Retriever');
const cat = createCat('Whiskers', 'Orange');

dog.makeSound();  // Buddy says: Woof!
cat.makeSound();  // Whiskers says: Meow!
```

**Why This Is Better:**
- **Modern Syntax**: Classes are clearer than prototype chains
- **Type Safety**: TypeScript catches errors at compile time
- **Composition**: Mix and match behaviors without complex inheritance
- **Encapsulation**: Private fields and methods
- **Immutability**: EnergyManager returns new instances
- **Flexibility**: Easy to add new behaviors without changing existing code

---

## Example 4: jQuery Spaghetti → Modern DOM Management

### Original Code (The Problem)
```javascript
// Classic jQuery spaghetti code
$(document).ready(function() {
    var currentPage = 1;
    var isLoading = false;
    var hasMore = true;
    
    function loadUsers() {
        if (isLoading || !hasMore) return;
        
        isLoading = true;
        $('#loading').show();
        
        $.ajax({
            url: '/api/users?page=' + currentPage,
            method: 'GET',
            success: function(data) {
                isLoading = false;
                $('#loading').hide();
                
                if (data.users.length === 0) {
                    hasMore = false;
                    $('#load-more').hide();
                    return;
                }
                
                data.users.forEach(function(user) {
                    var html = '<div class="user" data-id="' + user.id + '">' +
                               '<img src="' + user.avatar + '">' +
                               '<h3>' + user.name + '</h3>' +
                               '<p>' + user.email + '</p>' +
                               '<button class="delete-btn">Delete</button>' +
                               '</div>';
                    $('#users-container').append(html);
                });
                
                currentPage++;
            },
            error: function(err) {
                isLoading = false;
                $('#loading').hide();
                alert('Error loading users: ' + err.message);
            }
        });
    }
    
    $('#load-more').click(function() {
        loadUsers();
    });
    
    $(document).on('click', '.delete-btn', function() {
        var userId = $(this).closest('.user').data('id');
        
        if (!confirm('Delete this user?')) return;
        
        $.ajax({
            url: '/api/users/' + userId,
            method: 'DELETE',
            success: function() {
                $('[data-id="' + userId + '"]').fadeOut(function() {
                    $(this).remove();
                });
            },
            error: function(err) {
                alert('Error deleting user: ' + err.message);
            }
        });
    });
    
    loadUsers();
});
```

### Refactored Code (The Solution)

```typescript
// Modern vanilla JavaScript/TypeScript with proper architecture

// Types
interface User {
    id: string;
    name: string;
    email: string;
    avatar: string;
}

interface UsersResponse {
    users: User[];
    hasMore: boolean;
    page: number;
}

// API Client
class UserAPI {
    private baseUrl = '/api/users';
    
    async fetchUsers(page: number): Promise<UsersResponse> {
        const response = await fetch(`${this.baseUrl}?page=${page}`);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return response.json();
    }
    
    async deleteUser(userId: string): Promise<void> {
        const response = await fetch(`${this.baseUrl}/${userId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error(`Failed to delete user: ${response.statusText}`);
        }
    }
}

// View Components
class UserCard {
    private element: HTMLElement;
    
    constructor(private user: User, private onDelete: (id: string) => void) {
        this.element = this.render();
    }
    
    private render(): HTMLElement {
        const card = document.createElement('div');
        card.className = 'user';
        card.dataset.id = this.user.id;
        
        card.innerHTML = `
            <img src="${this.escapeHtml(this.user.avatar)}" 
                 alt="${this.escapeHtml(this.user.name)}"
                 loading="lazy">
            <h3>${this.escapeHtml(this.user.name)}</h3>
            <p>${this.escapeHtml(this.user.email)}</p>
            <button class="delete-btn" type="button">Delete</button>
        `;
        
        const deleteBtn = card.querySelector('.delete-btn');
        deleteBtn?.addEventListener('click', () => this.handleDelete());
        
        return card;
    }
    
    private async handleDelete(): Promise<void> {
        const confirmed = confirm(`Delete ${this.user.name}?`);
        if (!confirmed) return;
        
        this.onDelete(this.user.id);
    }
    
    remove(): void {
        this.element.classList.add('removing');
        
        // Wait for CSS animation
        setTimeout(() => {
            this.element.remove();
        }, 300);
    }
    
    getElement(): HTMLElement {
        return this.element;
    }
    
    private escapeHtml(text: string): string {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// State Management
class UserListState {
    private users: User[] = [];
    private currentPage = 1;
    private hasMore = true;
    private isLoading = false;
    private listeners: Array<() => void> = [];
    
    addUsers(users: User[]): void {
        this.users.push(...users);
        this.notify();
    }
    
    removeUser(userId: string): void {
        this.users = this.users.filter(u => u.id !== userId);
        this.notify();
    }
    
    setLoading(loading: boolean): void {
        this.isLoading = loading;
        this.notify();
    }
    
    setHasMore(hasMore: boolean): void {
        this.hasMore = hasMore;
        this.notify();
    }
    
    incrementPage(): void {
        this.currentPage++;
    }
    
    getState() {
        return {
            users: [...this.users],
            currentPage: this.currentPage,
            hasMore: this.hasMore,
            isLoading: this.isLoading
        };
    }
    
    subscribe(listener: () => void): () => void {
        this.listeners.push(listener);
        return () => {
            this.listeners = this.listeners.filter(l => l !== listener);
        };
    }
    
    private notify(): void {
        this.listeners.forEach(listener => listener());
    }
}

// Main Controller
class UserListController {
    private state = new UserListState();
    private api = new UserAPI();
    private userCards = new Map<string, UserCard>();
    
    constructor(
        private container: HTMLElement,
        private loadingElement: HTMLElement,
        private loadMoreButton: HTMLElement
    ) {
        this.setupEventListeners();
        this.state.subscribe(() => this.render());
    }
    
    private setupEventListeners(): void {
        this.loadMoreButton.addEventListener('click', () => {
            this.loadUsers();
        });
    }
    
    async loadUsers(): Promise<void> {
        const { isLoading, hasMore, currentPage } = this.state.getState();
        
        if (isLoading || !hasMore) return;
        
        try {
            this.state.setLoading(true);
            
            const response = await this.api.fetchUsers(currentPage);
            
            this.state.addUsers(response.users);
            this.state.setHasMore(response.hasMore);
            this.state.incrementPage();
            
        } catch (error) {
            this.handleError('Failed to load users', error);
        } finally {
            this.state.setLoading(false);
        }
    }
    
    async deleteUser(userId: string): Promise<void> {
        const card = this.userCards.get(userId);
        if (!card) return;
        
        try {
            // Optimistic update
            card.remove();
            this.userCards.delete(userId);
            
            await this.api.deleteUser(userId);
            this.state.removeUser(userId);
            
        } catch (error) {
            // Revert on error
            this.handleError('Failed to delete user', error);
            // In real app, would re-add the card
        }
    }
    
    private render(): void {
        const { users, isLoading, hasMore } = this.state.getState();
        
        // Render loading state
        this.loadingElement.style.display = isLoading ? 'block' : 'none';
        
        // Render users
        users.forEach(user => {
            if (!this.userCards.has(user.id)) {
                const card = new UserCard(user, (id) => this.deleteUser(id));
                this.userCards.set(user.id, card);
                this.container.appendChild(card.getElement());
            }
        });
        
        // Render load more button
        this.loadMoreButton.style.display = hasMore ? 'block' : 'none';
    }
    
    private handleError(message: string, error: unknown): void {
        console.error(message, error);
        
        // Better error UI
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        errorDiv.style.cssText = `
            background: #fee;
            color: #c00;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 4px;
        `;
        
        this.container.insertBefore(errorDiv, this.container.firstChild);
        
        setTimeout(() => errorDiv.remove(), 5000);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('users-container')!;
    const loading = document.getElementById('loading')!;
    const loadMore = document.getElementById('load-more')!;
    
    const controller = new UserListController(container, loading, loadMore);
    controller.loadUsers();
});

// Bonus: React version
function UserListReact() {
    const [users, setUsers] = useState<User[]>([]);
    const [page, setPage] = useState(1);
    const [isLoading, setIsLoading] = useState(false);
    const [hasMore, setHasMore] = useState(true);
    const [error, setError] = useState<string | null>(null);
    
    const api = useMemo(() => new UserAPI(), []);
    
    const loadUsers = useCallback(async () => {
        if (isLoading || !hasMore) return;
        
        try {
            setIsLoading(true);
            setError(null);
            
            const response = await api.fetchUsers(page);
            
            setUsers(prev => [...prev, ...response.users]);
            setHasMore(response.hasMore);
            setPage(prev => prev + 1);
            
        } catch (err) {
            setError('Failed to load users');
        } finally {
            setIsLoading(false);
        }
    }, [api, page, isLoading, hasMore]);
    
    const deleteUser = useCallback(async (userId: string) => {
        if (!confirm('Delete this user?')) return;
        
        try {
            // Optimistic update
            setUsers(prev => prev.filter(u => u.id !== userId));
            await api.deleteUser(userId);
            
        } catch (err) {
            setError('Failed to delete user');
            // Reload to restore state
            setUsers([]);
            setPage(1);
            loadUsers();
        }
    }, [api, loadUsers]);
    
    useEffect(() => {
        loadUsers();
    }, []);  // Only load on mount
    
    return (
        <div>
            {error && <div className="error">{error}</div>}
            
            <div className="users-grid">
                {users.map(user => (
                    <UserCardComponent
                        key={user.id}
                        user={user}
                        onDelete={deleteUser}
                    />
                ))}
            </div>
            
            {isLoading && <div className="loading">Loading...</div>}
            
            {hasMore && !isLoading && (
                <button onClick={loadUsers}>Load More</button>
            )}
        </div>
    );
}
```

**Why This Is Better:**
- **No jQuery Dependency**: Modern browsers have everything we need
- **Separation of Concerns**: API, State, View are separate
- **Type Safety**: TypeScript catches errors
- **Testability**: Each class can be tested independently
- **Memory Management**: Proper cleanup of event listeners
- **Security**: HTML escaping prevents XSS
- **Performance**: Only renders what changed
- **Maintainability**: Clear structure and responsibilities

---

## Example 5: Memory Leaks → Proper Cleanup

### Original Code (The Problem)
```javascript
// Memory leak city
class DataFetcher {
    constructor(url) {
        this.url = url;
        this.cache = {};
        
        // LEAK 1: Never cleaned up
        setInterval(() => {
            this.refreshCache();
        }, 5000);
        
        // LEAK 2: Event listener never removed
        window.addEventListener('online', () => {
            this.refreshCache();
        });
        
        // LEAK 3: Closure captures this permanently
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.refreshCache();
            }
        });
    }
    
    async fetch(key) {
        if (this.cache[key]) {
            return this.cache[key];
        }
        
        const response = await fetch(`${this.url}/${key}`);
        const data = await response.json();
        
        // LEAK 4: Cache grows unbounded
        this.cache[key] = data;
        
        return data;
    }
    
    async refreshCache() {
        for (const key in this.cache) {
            const data = await this.fetch(key);
            this.cache[key] = data;
        }
    }
}

// Usage leaks memory
function createFetcher() {
    return new DataFetcher('/api/data');
}

// Every time this runs, old fetcher leaks
let fetcher = createFetcher();
```

### Refactored Code (The Solution)

```typescript
// Proper cleanup and resource management
interface CacheEntry<T> {
    data: T;
    timestamp: number;
}

class DataFetcher<T = any> {
    private cache = new Map<string, CacheEntry<T>>();
    private timerId: number | null = null;
    private abortController = new AbortController();
    private eventListeners = new Map<string, EventListener>();
    
    constructor(
        private url: string,
        private options: {
            refreshInterval?: number;
            maxCacheSize?: number;
            maxCacheAge?: number;
        } = {}
    ) {
        const {
            refreshInterval = 5000,
            maxCacheSize = 100,
            maxCacheAge = 60000
        } = options;
        
        this.maxCacheSize = maxCacheSize;
        this.maxCacheAge = maxCacheAge;
        
        // Use abortController for fetch cancellation
        this.startRefreshTimer(refreshInterval);
        this.setupEventListeners();
    }
    
    private startRefreshTimer(interval: number): void {
        // Store timer ID for cleanup
        this.timerId = window.setInterval(() => {
            this.refreshCache();
        }, interval);
    }
    
    private setupEventListeners(): void {
        // Store bound listeners for cleanup
        const onlineHandler = () => this.refreshCache();
        const visibilityHandler = () => {
            if (!document.hidden) {
                this.refreshCache();
            }
        };
        
        this.eventListeners.set('online', onlineHandler);
        this.eventListeners.set('visibilitychange', visibilityHandler);
        
        window.addEventListener('online', onlineHandler);
        document.addEventListener('visibilitychange', visibilityHandler);
    }
    
    async fetch(key: string): Promise<T> {
        // Check cache first
        const cached = this.cache.get(key);
        if (cached && this.isCacheValid(cached)) {
            return cached.data;
        }
        
        try {
            const response = await fetch(`${this.url}/${key}`, {
                signal: this.abortController.signal
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            this.setCacheEntry(key, data);
            
            return data;
            
        } catch (error) {
            if (error instanceof Error && error.name === 'AbortError') {
                throw new Error('Fetch was cancelled');
            }
            throw error;
        }
    }
    
    private setCacheEntry(key: string, data: T): void {
        // Implement LRU cache with size limit
        if (this.cache.size >= this.maxCacheSize) {
            // Remove oldest entry
            const firstKey = this.cache.keys().next().value;
            this.cache.delete(firstKey);
        }
        
        this.cache.set(key, {
            data,
            timestamp: Date.now()
        });
    }
    
    private isCacheValid(entry: CacheEntry<T>): boolean {
        return Date.now() - entry.timestamp < this.maxCacheAge;
    }
    
    private async refreshCache(): Promise<void> {
        // Clean expired entries first
        const now = Date.now();
        for (const [key, entry] of this.cache.entries()) {
            if (now - entry.timestamp > this.maxCacheAge) {
                this.cache.delete(key);
            }
        }
        
        // Refresh remaining entries
        const refreshPromises = Array.from(this.cache.keys()).map(
            key => this.fetch(key).catch(err => {
                console.error(`Failed to refresh ${key}:`, err);
            })
        );
        
        await Promise.allSettled(refreshPromises);
    }
    
    // CRITICAL: Cleanup method
    destroy(): void {
        // Clear timer
        if (this.timerId !== null) {
            clearInterval(this.timerId);
            this.timerId = null;
        }
        
        // Abort any pending fetches
        this.abortController.abort();
        
        // Remove event listeners
        for (const [event, handler] of this.eventListeners.entries()) {
            if (event === 'online') {
                window.removeEventListener(event, handler);
            } else {
                document.removeEventListener(event, handler);
            }
        }
        this.eventListeners.clear();
        
        // Clear cache
        this.cache.clear();
    }
}

// Wrapper for automatic cleanup
class ManagedDataFetcher<T = any> {
    private fetcher: DataFetcher<T> | null;
    
    constructor(url: string, options?: any) {
        this.fetcher = new DataFetcher<T>(url, options);
    }
    
    async fetch(key: string): Promise<T> {
        if (!this.fetcher) {
            throw new Error('Fetcher has been destroyed');
        }
        return this.fetcher.fetch(key);
    }
    
    destroy(): void {
        if (this.fetcher) {
            this.fetcher.destroy();
            this.fetcher = null;
        }
    }
    
    // Automatically cleanup when garbage collected
    [Symbol.dispose](): void {
        this.destroy();
    }
}

// React hook with automatic cleanup
function useDataFetcher<T>(url: string) {
    const fetcherRef = useRef<DataFetcher<T> | null>(null);
    
    useEffect(() => {
        // Create fetcher
        fetcherRef.current = new DataFetcher<T>(url);
        
        // Cleanup on unmount
        return () => {
            fetcherRef.current?.destroy();
            fetcherRef.current = null;
        };
    }, [url]);
    
    const fetch = useCallback(async (key: string) => {
        if (!fetcherRef.current) {
            throw new Error('Fetcher not initialized');
        }
        return fetcherRef.current.fetch(key);
    }, []);
    
    return { fetch };
}

// Vue 3 composition API
function useDataFetcherVue<T>(url: Ref<string>) {
    const fetcher = ref<DataFetcher<T> | null>(null);
    
    watchEffect((onCleanup) => {
        fetcher.value = new DataFetcher<T>(url.value);
        
        onCleanup(() => {
            fetcher.value?.destroy();
            fetcher.value = null;
        });
    });
    
    const fetch = async (key: string) => {
        if (!fetcher.value) {
            throw new Error('Fetcher not initialized');
        }
        return fetcher.value.fetch(key);
    };
    
    return { fetch };
}

// Modern using declaration (TypeScript 5.2+)
async function processData() {
    using fetcher = new ManagedDataFetcher('/api/data');
    
    const data = await fetcher.fetch('users');
    // ... process data
    
    // Automatically cleaned up when leaving scope
}
```

**Why This Is Better:**
- **No Memory Leaks**: Proper cleanup of all resources
- **AbortController**: Cancel pending requests
- **Bounded Cache**: LRU with size limit
- **Event Cleanup**: Listeners properly removed
- **Timer Cleanup**: Intervals cleared
- **Framework Integration**: Works with React, Vue, etc.
- **Modern Features**: Using declarations for automatic cleanup

---

## Key Takeaways for JavaScript/TypeScript

1. **Use Modern Syntax**: async/await, classes, const/let
2. **Embrace Immutability**: Pure functions, no mutations
3. **Type Everything**: TypeScript catches bugs before runtime
4. **Clean Up Resources**: Always implement cleanup/destroy methods
5. **Composition Over Inheritance**: Mix behaviors instead of deep hierarchies
6. **Separate Concerns**: API, State, View should be independent
7. **Handle Errors Properly**: Try/catch, proper error messages
8. **Optimize Carefully**: Measure before optimizing

These patterns work whether you're building vanilla JS, React, Vue, Angular, or any other framework!
