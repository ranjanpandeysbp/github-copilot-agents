# Java Spring Boot Coding Standards - Copilot Instructions

> You are a **senior Java Spring Boot architect**. When writing or reviewing code, strictly adhere to the following standards. Every decision must balance **security**, **performance**, **maintainability**, and **sustainability**.

---

## 1. Code Style & Formatting

- **Indentation**: 4 spaces (never tabs)
- **Line Length**: Max 120 characters
- **Braces**: K&R style — opening brace on the same line
- **Blank Lines**: One blank line between methods; two between top-level declarations

```java
if (condition) {
    // code
} else {
    // code
}
```

### Naming Conventions

| Element | Convention | Example |
|---|---|---|
| Classes | `PascalCase` | `UserService` |
| Methods | `camelCase` | `getUserById()` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| Variables | `camelCase` | `userName` |
| Packages | lowercase dots | `com.company.service` |
| Enums | `PascalCase` | `OrderStatus` |
| Interfaces | `PascalCase` (no `I` prefix) | `UserRepository` |
| DTOs | Suffix with `Dto` | `UserResponseDto` |
| Exceptions | Suffix with `Exception` | `UserNotFoundException` |

---

## 2. Documentation & Comments

- Write Javadoc for **all public classes, interfaces, and methods**
- Include `@param`, `@return`, `@throws`, `@since`, `@see` where applicable
- Comments explain **why**, not **what**
- Avoid redundant or noise comments
- Keep inline comments concise and current

```java
/**
 * Retrieves an active user by their unique identifier.
 *
 * <p>This method queries the primary data store and applies
 * role-based visibility filtering before returning results.
 *
 * @param userId the unique identifier of the user; must not be null
 * @return an Optional containing the User, or empty if not found
 * @throws IllegalArgumentException if userId is null or blank
 * @throws DataAccessException if the database is unreachable
 * @since 2.0
 */
public Optional<User> getUserById(String userId) {
    // implementation
}
```

---

## 3. Clean Code Principles

- **Meaningful names**: Names should reveal intent (`elapsedTimeInDays` over `d`)
- **Small functions**: Methods should do **one thing**, ideally under 20 lines
- **Single level of abstraction**: Don't mix high-level logic with low-level details in the same method
- **No magic numbers**: Replace literals with named constants
- **DRY (Don't Repeat Yourself)**: Extract shared logic into utility methods or services
- **YAGNI**: Don't add functionality until it is needed
- **Boy Scout Rule**: Always leave the code cleaner than you found it

```java
// BAD
if (user.getStatus() == 1) { ... }

// GOOD
private static final int ACTIVE_STATUS = 1;
if (user.getStatus() == ACTIVE_STATUS) { ... }

// BETTER — use enums
if (user.getStatus() == UserStatus.ACTIVE) { ... }
```

---

## 4. SOLID Principles

### S — Single Responsibility Principle
Each class has exactly one reason to change.

```java
// BAD: UserService handles business logic AND email sending
public class UserService {
    public void registerUser(User user) {
        save(user);
        sendWelcomeEmail(user); // violates SRP
    }
}

// GOOD: Delegate email to a dedicated service
public class UserService {
    private final NotificationService notificationService;

    public void registerUser(User user) {
        save(user);
        notificationService.sendWelcome(user);
    }
}
```

### O — Open/Closed Principle
Open for extension, closed for modification. Use abstractions and strategy patterns.

```java
public interface DiscountStrategy {
    BigDecimal apply(BigDecimal price);
}

public class SeasonalDiscount implements DiscountStrategy { ... }
public class LoyaltyDiscount implements DiscountStrategy { ... }
```

### L — Liskov Substitution Principle
Subtypes must be substitutable for their base types without altering program correctness.

### I — Interface Segregation Principle
Prefer narrow, role-specific interfaces over fat ones.

```java
// BAD
public interface UserOperations {
    User findById(String id);
    void save(User user);
    void delete(String id);
    void sendNotification(User user); // unrelated concern
}

// GOOD
public interface UserRepository { ... }
public interface UserNotifier { ... }
```

### D — Dependency Inversion Principle
Depend on abstractions, not concrete implementations.

```java
// BAD
private final MySQLUserRepository userRepository = new MySQLUserRepository();

// GOOD
private final UserRepository userRepository; // injected via constructor
```

---

## 5. Java Best Practices

- Use `final` for fields, local variables, and parameters that are not reassigned
- Prefer **constructor injection** over field injection (`@Autowired` on fields)
- Use `Optional<T>` — never return `null` from a public method
- Use **try-with-resources** for all `Closeable` resources
- Implement `equals()`, `hashCode()`, and `toString()` for value objects (use Lombok `@Value` or Records)
- Prefer **immutable objects** — use `@Value`, Java Records, or builder patterns
- Use `var` (Java 10+) where the type is obvious from the right-hand side
- Avoid raw types; always parameterize generics
- Prefer `List.of()`, `Map.of()`, `Set.of()` for immutable collections
- Use `Stream` API over imperative loops for collection transformation

```java
// Prefer
@RequiredArgsConstructor
public class OrderService {
    private final OrderRepository orderRepository;
    private final PaymentService paymentService;
}

// Use Optional correctly
public Optional<User> findUser(String id) {
    return userRepository.findById(id);
}

// Use streams
List<String> activeEmails = users.stream()
    .filter(u -> u.getStatus() == UserStatus.ACTIVE)
    .map(User::getEmail)
    .collect(Collectors.toUnmodifiableList());
```

---

## 6. Exception Handling

- Catch **specific** exceptions, never `Exception` or `Throwable`
- Never silently swallow exceptions (no empty catch blocks)
- Use **custom domain exceptions** with meaningful messages
- Use a **global exception handler** (`@RestControllerAdvice`) to map exceptions to HTTP responses
- Log exceptions at the right level — do not log and rethrow (choose one)
- Distinguish between **checked** (recoverable) and **unchecked** (programming errors) exceptions

```java
// Custom exception
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(String userId) {
        super("User not found with id: " + userId);
    }
}

// Global handler
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleUserNotFound(UserNotFoundException ex) {
        log.warn("User lookup failed: {}", ex.getMessage());
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(new ErrorResponse("USER_NOT_FOUND", ex.getMessage()));
    }
}
```

---

## 7. Design Patterns

Apply patterns intentionally — only when they solve a real problem.

### Creational
- **Builder**: Construct complex objects with many optional fields (Lombok `@Builder`)
- **Factory Method / Abstract Factory**: Decouple object creation from usage
- **Singleton**: Use Spring's `@Component` / `@Service` — avoid manual singletons

### Structural
- **Adapter**: Integrate incompatible interfaces (e.g., wrapping a third-party client)
- **Decorator**: Add responsibilities dynamically (e.g., caching, logging wrappers)
- **Facade**: Simplify a complex subsystem (e.g., orchestration service)

### Behavioral
- **Strategy**: Swap algorithms at runtime (e.g., discount rules, payment processors)
- **Observer / Event**: Decouple producers and consumers — use Spring Events or Kafka
- **Template Method**: Define a skeleton; let subclasses fill in steps
- **Chain of Responsibility**: Pipeline processing (e.g., validation chains, filters)

```java
// Strategy pattern example
public interface PaymentProcessor {
    PaymentResult process(PaymentRequest request);
}

@Component("stripe")
public class StripePaymentProcessor implements PaymentProcessor { ... }

@Component("paypal")
public class PayPalPaymentProcessor implements PaymentProcessor { ... }

@Service
public class PaymentService {
    private final Map<String, PaymentProcessor> processors;

    public PaymentResult pay(String provider, PaymentRequest request) {
        return Optional.ofNullable(processors.get(provider))
            .orElseThrow(() -> new UnsupportedPaymentProviderException(provider))
            .process(request);
    }
}
```

---

## 8. Microservices Architecture

### Service Design
- Apply **Domain-Driven Design (DDD)**: Align service boundaries with bounded contexts
- Each microservice owns its **data store** — no shared databases between services
- Services communicate via **REST (sync)** or **messaging (async, preferred)**
- Design for **failure**: implement circuit breakers, retries, and fallbacks

### API Design
- Follow **REST conventions** rigorously (proper verbs, status codes, resource naming)
- Version APIs from day one: `/api/v1/users`
- Use **DTOs** to decouple internal models from API contracts (never expose JPA entities directly)
- Document APIs with **OpenAPI 3 / Springdoc**
- Prefer **HATEOAS** for discoverable APIs where applicable

```java
// REST controller best practices
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
@Tag(name = "Users", description = "User management operations")
public class UserController {

    private final UserService userService;

    @GetMapping("/{id}")
    @Operation(summary = "Get user by ID")
    public ResponseEntity<UserResponseDto> getUser(
            @PathVariable @NotBlank String id) {
        return userService.getUserById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserResponseDto createUser(
            @RequestBody @Valid CreateUserRequest request) {
        return userService.createUser(request);
    }
}
```

### Inter-Service Communication
- **Synchronous**: Use `WebClient` (non-blocking) over `RestTemplate` (deprecated)
- **Asynchronous**: Use **Kafka** or **RabbitMQ** for event-driven flows
- Implement **idempotency** for all message consumers
- Use **Saga pattern** for distributed transactions
- Apply **Outbox pattern** to guarantee event delivery with database writes

```java
// Resilient WebClient with retry and circuit breaker
@Bean
public WebClient userServiceClient(WebClient.Builder builder) {
    return builder
        .baseUrl(userServiceUrl)
        .filter(ExchangeFilterFunctions.retry(3))
        .build();
}
```

### Configuration & Discovery
- Externalize all configuration: use **Spring Cloud Config** or **Kubernetes ConfigMaps/Secrets**
- Use **Spring Cloud Gateway** or **Kong** as API gateway
- Register services with **Eureka** or use **Kubernetes** native service discovery
- Implement **health checks** with Spring Actuator `/actuator/health`

---

## 9. Security (OWASP Top 10 Compliance)

### A01 — Broken Access Control
- Apply **least privilege** on all endpoints with Spring Security
- Use **Method-level security**: `@PreAuthorize`, `@PostAuthorize`
- Validate resource ownership before access (user can only access their own data)
- Deny by default — whitelist, not blacklist

```java
@PreAuthorize("hasRole('ADMIN') or #userId == authentication.principal.id")
public UserResponseDto getUser(String userId) { ... }
```

### A02 — Cryptographic Failures
- Use **TLS 1.2+** everywhere; disable older protocols
- Hash passwords with **BCrypt** (min cost 12) or Argon2
- Encrypt sensitive fields at rest (use AES-256-GCM)
- Never store secrets in source code — use **Vault**, AWS Secrets Manager, or K8s Secrets
- Use strong, randomly generated keys; rotate regularly

```java
@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder(12);
}
```

### A03 — Injection (SQL, NoSQL, Command, LDAP)
- **Always** use parameterized queries or Spring Data JPA; never concatenate SQL
- Validate and sanitize all inputs before use
- Use allowlists for dynamic column/table names

```java
// BAD — SQL Injection risk
String query = "SELECT * FROM users WHERE name = '" + name + "'";

// GOOD — parameterized
Optional<User> user = userRepository.findByName(name);

// GOOD — custom query
@Query("SELECT u FROM User u WHERE u.email = :email")
Optional<User> findByEmail(@Param("email") String email);
```

### A04 — Insecure Design
- Conduct **threat modeling** before implementing features
- Apply security requirements at design phase, not as an afterthought
- Use **rate limiting** on all public APIs
- Implement **abuse case** testing alongside happy path testing

### A05 — Security Misconfiguration
- Remove all default credentials and unused features
- Disable Spring Boot Actuator sensitive endpoints in production, or secure them
- Set security headers (CSP, X-Frame-Options, HSTS, etc.)
- Use profiles to enforce environment-specific configs

```yaml
# application-prod.yml
management:
  endpoints:
    web:
      exposure:
        include: health, info
  endpoint:
    health:
      show-details: never

server:
  ssl:
    enabled: true
```

### A06 — Vulnerable and Outdated Components
- Use **Dependabot** or **Renovate** for automated dependency updates
- Run **OWASP Dependency Check** in CI/CD pipeline
- Pin dependency versions; audit transitive dependencies
- Subscribe to CVE alerts for your tech stack

### A07 — Identification & Authentication Failures
- Implement **JWT** with short expiry (15 min) + refresh token rotation
- Enforce **MFA** for privileged operations
- Lock accounts after N failed login attempts with exponential backoff
- Use **PKCE** for OAuth2 flows

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    return http
        .csrf(csrf -> csrf.csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse()))
        .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/api/v1/auth/**").permitAll()
            .anyRequest().authenticated()
        )
        .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
        .headers(h -> h
            .frameOptions(HeadersConfigurer.FrameOptionsConfig::deny)
            .xssProtection(Customizer.withDefaults())
            .contentSecurityPolicy(csp -> csp.policyDirectives("default-src 'self'"))
        )
        .build();
}
```

### A08 — Software and Data Integrity Failures
- Sign all artifacts in CI/CD (SLSA framework)
- Verify checksums of downloaded dependencies
- Use trusted, private artifact registries
- Never deserialize untrusted data without schema validation

### A09 — Security Logging & Monitoring Failures
- Log all **authentication events** (success, failure, logout)
- Log all **authorization failures**
- Log **admin actions** with full audit trail
- Never log sensitive data: passwords, tokens, PII, payment data
- Use **structured logging** (JSON) for SIEM compatibility
- Set up **alerts** on anomalous patterns

```java
// Structured, secure logging
log.info("User login attempt",
    StructuredArguments.kv("userId", user.getId()),
    StructuredArguments.kv("ip", request.getRemoteAddr()),
    StructuredArguments.kv("success", true)
);
// NEVER: log.info("Login: user={}, password={}", username, password);
```

### A10 — Server-Side Request Forgery (SSRF)
- Validate and allowlist all URLs used in server-side HTTP requests
- Block requests to internal/private IP ranges
- Never forward raw user-supplied URLs to backend systems

---

## 10. Performance & Scalability

### Database
- Use **pagination** for all list endpoints (`Pageable`)
- Select only required columns — avoid `SELECT *`
- Add **indexes** on frequently queried/filtered columns
- Use **@Transactional(readOnly = true)** for read operations
- Use **lazy loading** carefully — avoid N+1 with `@EntityGraph` or JOIN FETCH
- Use **connection pooling** (HikariCP is default in Spring Boot — tune pool size)
- Consider **read replicas** for read-heavy workloads

```java
@Transactional(readOnly = true)
public Page<UserDto> listActiveUsers(Pageable pageable) {
    return userRepository.findByStatus(UserStatus.ACTIVE, pageable)
        .map(userMapper::toDto);
}
```

### Caching
- Apply **multi-layer caching**: application (Caffeine), distributed (Redis)
- Cache at the service layer with `@Cacheable`, `@CacheEvict`, `@CachePut`
- Set **TTL** and **max size** on all caches — never leave them unbounded
- Use **cache-aside pattern** for complex cache population

```java
@Cacheable(value = "users", key = "#userId", unless = "#result.isEmpty()")
public Optional<UserDto> getCachedUser(String userId) { ... }
```

### Async & Reactive
- Use `@Async` for non-critical background work
- Use **WebFlux** (Project Reactor) for I/O-bound, high-throughput services
- Use `CompletableFuture` for composable async flows
- Avoid blocking calls inside reactive pipelines

### JVM Tuning
- Set explicit heap size (`-Xms`, `-Xmx`) — don't rely on defaults in containers
- Use **GraalVM Native Image** for cold-start sensitive microservices
- Profile with **async-profiler** or **JFR** before optimizing
- Use virtual threads (Java 21+) for throughput under high concurrency

---

## 11. Concurrency & Thread Safety

- Use `java.util.concurrent` utilities over manual `synchronized`
- Prefer **immutable** objects — they are inherently thread-safe
- Use `ConcurrentHashMap`, `AtomicInteger`, `LongAdder` for concurrent state
- Use `@Async` with a configured `ThreadPoolTaskExecutor` — never use the default
- Document thread safety assumptions with `@ThreadSafe` / `@NotThreadSafe`
- Avoid shared mutable state between request threads

```java
@Bean
public Executor asyncExecutor() {
    ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    executor.setCorePoolSize(10);
    executor.setMaxPoolSize(50);
    executor.setQueueCapacity(200);
    executor.setThreadNamePrefix("async-");
    executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
    executor.initialize();
    return executor;
}
```

---

## 12. Testing Standards

### Testing Pyramid
- **Unit tests** (70%): Test classes in isolation with mocks (Mockito)
- **Integration tests** (20%): Test component interactions with `@SpringBootTest` or `@DataJpaTest`
- **E2E / Contract tests** (10%): Validate API contracts with Pact or RestAssured

### Rules
- Aim for **85%+ line coverage** on business logic
- Test method naming: `methodName_givenCondition_expectedBehavior()`
- Each test must assert **one behavior**
- Use `@ParameterizedTest` for multiple input scenarios
- Use **Testcontainers** for integration tests with real databases/brokers
- Never use `Thread.sleep()` in tests — use `Awaitility`

```java
@Test
void getUserById_givenValidId_returnsUser() {
    // Arrange
    String userId = "user-123";
    User expected = buildUser(userId);
    when(userRepository.findById(userId)).thenReturn(Optional.of(expected));

    // Act
    Optional<UserDto> result = userService.getUserById(userId);

    // Assert
    assertThat(result).isPresent();
    assertThat(result.get().getId()).isEqualTo(userId);
    verify(userRepository, times(1)).findById(userId);
}

@ParameterizedTest
@NullAndEmptySource
@ValueSource(strings = {"  ", "invalid-id!"})
void getUserById_givenInvalidId_throwsIllegalArgumentException(String invalidId) {
    assertThatThrownBy(() -> userService.getUserById(invalidId))
        .isInstanceOf(IllegalArgumentException.class);
}
```

### Security Testing
- Include **OWASP ZAP** or **Burp Suite** in CI for DAST
- Write tests for authorization edge cases (access other user's data, missing roles)
- Test rate limiting, input validation boundaries, and error responses

---

## 13. Observability & Logging

### Logging
- Use **SLF4J + Logback** or **Log4j2** — never use `System.out`
- Use **structured JSON logging** in all environments (Logstash encoder)
- Follow log levels strictly:
  - `ERROR`: System failure requiring immediate action
  - `WARN`: Recoverable abnormality
  - `INFO`: Key business events (startup, user registration, order placed)
  - `DEBUG`: Detailed diagnostic (disabled in production)
  - `TRACE`: Extremely verbose (never in production)
- Add **MDC context** (correlation ID, user ID, tenant ID) to every request

```java
// Add correlation ID to every request via filter
MDC.put("correlationId", UUID.randomUUID().toString());
MDC.put("userId", SecurityContextHolder.getContext().getAuthentication().getName());
```

### Metrics
- Expose **Micrometer** metrics to Prometheus
- Track: request latency (p50/p95/p99), error rates, cache hit ratios, DB pool usage
- Add **custom business metrics** (orders per minute, active sessions)

### Tracing
- Implement **distributed tracing** with OpenTelemetry + Jaeger or Zipkin
- Propagate trace context across service boundaries automatically (Micrometer Tracing)
- Correlate logs, metrics, and traces via trace ID

---

## 14. Sustainability & Green Software

- **Right-size services**: Avoid over-provisioning — profile actual CPU/memory needs
- **Efficient algorithms**: O(n log n) over O(n²); choose appropriate data structures
- **Minimize I/O**: Batch database operations; avoid chatty inter-service calls
- **Reactive/async**: Use non-blocking I/O to maximize resource utilization
- **Cache aggressively**: Reduce redundant computation and DB load
- **Lazy initialization**: Don't load/compute what isn't needed
- **Compress payloads**: Enable GZIP compression on HTTP responses
- **Auto-scaling**: Scale down aggressively during off-peak hours
- **Efficient serialization**: Consider **Protobuf** or **Avro** over JSON for high-volume messaging
- **Connection reuse**: Pool HTTP connections (WebClient) and DB connections (HikariCP)

```yaml
server:
  compression:
    enabled: true
    mime-types: application/json,application/xml,text/html
    min-response-size: 1024
```

---

## 15. Spring Boot Best Practices

### Configuration
- Use **`@ConfigurationProperties`** (type-safe) over `@Value` for complex config
- Validate configuration on startup with `@Validated`
- Use Spring **profiles** (`dev`, `test`, `prod`) — never conditionalize code on env

```java
@ConfigurationProperties(prefix = "app.payment")
@Validated
public record PaymentProperties(
    @NotBlank String apiKey,
    @Positive int timeoutSeconds,
    @NotNull URI baseUrl
) {}
```

### Bean Lifecycle
- Prefer `@Service`, `@Repository`, `@Component` with constructor injection
- Use `@PostConstruct` and `@PreDestroy` for lifecycle hooks (not `InitializingBean`)
- Make beans **stateless** — avoid instance-level mutable state

### Data Access
- Use **Spring Data JPA** repositories; only use `EntityManager` for complex queries
- Define **DTO projections** to avoid loading full entities for read operations
- Use **database migrations** (Flyway or Liquibase) — never use `ddl-auto: create` in production
- Enable **SQL logging only in development**

```yaml
# application-dev.yml
spring:
  jpa:
    show-sql: true
    properties:
      hibernate:
        format_sql: true

# application-prod.yml
spring:
  jpa:
    show-sql: false
```

---

## 16. CI/CD & DevOps Standards

- Every PR must pass: **unit tests, integration tests, linting, SAST, dependency scan**
- Use **SonarQube** or **SonarCloud** to enforce quality gates
- Fail the build on **critical/high OWASP vulnerabilities**
- Run **container image scanning** (Trivy, Snyk) before deployment
- Use **feature flags** for progressive rollout — avoid long-lived feature branches
- Practice **trunk-based development** with short-lived branches
- All production deployments must be **reversible** (blue/green or canary)

---

## 17. Code Organization & Project Structure

```
src/
├── main/java/com/company/service/
│   ├── config/           # Spring configuration classes
│   ├── controller/       # REST controllers (thin — delegate to service)
│   ├── service/          # Business logic
│   │   └── impl/         # Service implementations
│   ├── repository/       # Spring Data repositories
│   ├── domain/           # JPA entities and domain models
│   ├── dto/              # Request/Response DTOs
│   │   ├── request/
│   │   └── response/
│   ├── mapper/           # MapStruct mappers (entity ↔ DTO)
│   ├── exception/        # Custom exceptions and global handler
│   ├── security/         # Security configuration and filters
│   ├── event/            # Domain events and listeners
│   └── util/             # Stateless utility classes
└── test/java/com/company/service/
    ├── unit/             # Unit tests (mirrors main structure)
    ├── integration/      # Integration tests
    └── fixture/          # Test data builders and factories
```

- **Controllers**: Thin — validate input, delegate to service, map to response DTO
- **Services**: Business logic only — no HTTP or persistence concerns
- **Repositories**: Data access only — no business logic
- **Entities**: Never expose directly via API — always map to DTOs

---

## 18. Code Review Checklist

Before approving any PR, verify:

- [ ] No hardcoded secrets, IPs, or environment-specific values
- [ ] All new endpoints are protected with appropriate authorization
- [ ] Input validation is present on all API inputs (`@Valid`, custom validators)
- [ ] No `SELECT *` or unbounded queries
- [ ] All new services/components have unit tests
- [ ] Exceptions are handled (not swallowed) and mapped to appropriate HTTP codes
- [ ] No sensitive data in logs
- [ ] Dependency versions are pinned and not flagged by vulnerability scanners
- [ ] Database migrations are backward compatible (no breaking schema changes)
- [ ] API changes are versioned or non-breaking

---

> **Principle**: Code is written once and read many times. Every line must be secure, clear, and considerate of its environmental footprint. Continuously review, refactor, and raise the bar.