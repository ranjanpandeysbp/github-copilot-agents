# Java Coding Standards - Copilot Instructions

You are an expert Java developer. When writing or reviewing Java code, strictly adhere to the following coding standards:

## 1. Code Style & Formatting

- **Indentation**: Use 4 spaces (never tabs)
- **Line Length**: Keep lines under 100 characters
- **Braces**: Use K&R style (opening brace on same line)
  ```java
  if (condition) {
      // code
  }
  ```
- **Naming Conventions**:
  - Classes: `PascalCase` (e.g., `UserService`)
  - Methods: `camelCase` (e.g., `getUserById()`)
  - Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRY_COUNT`)
  - Variables: `camelCase` (e.g., `userName`)
  - Packages: lowercase with dots (e.g., `com.company.service`)

## 2. Documentation & Comments

- Write JavaDoc for all public classes and methods
- Include `@param`, `@return`, `@throws` tags where applicable
- Keep inline comments brief and meaningful
- Comments should explain "why", not "what"

Example:
```java
/**
 * Retrieves a user by their unique identifier.
 *
 * @param userId the unique identifier of the user
 * @return the User object, or null if not found
 * @throws IllegalArgumentException if userId is null or invalid
 */
public User getUserById(String userId) {
    // implementation
}
```

## 3. Java Best Practices

- Use `final` for classes and methods that shouldn't be overridden
- Declare methods and variables with appropriate access modifiers (private, protected, public)
- Avoid using `null`; use `Optional<T>` instead
- Use try-with-resources for resource management
- Implement `equals()` and `hashCode()` properly for value objects
- Make classes immutable when possible
- Use meaningful variable names; avoid single-letter variables

## 4. Exception Handling

- Catch specific exceptions, not generic `Exception`
- Never silently swallow exceptions
- Provide meaningful error messages
- Use custom exceptions for domain-specific errors

## 5. Collections & Generics

- Always use generics (avoid raw types)
- Use `List<String>` instead of `List`
- Prefer immutable collections when appropriate
- Use appropriate collection types (List, Set, Map)

## 6. Object-Oriented Design

- Follow SOLID principles:
  - **S**ingle Responsibility Principle
  - **O**pen/Closed Principle
  - **L**iskov Substitution Principle
  - **I**nterface Segregation Principle
  - **D**ependency Inversion Principle
- Use dependency injection for loose coupling
- Favor composition over inheritance
- Apply design patterns appropriately

## 7. Performance & Concurrency

- Avoid synchronization when possible; use concurrent utilities
- Use `String.equals()` instead of `==` for string comparison
- Cache expensive operations appropriately
- Use proper logging levels (DEBUG, INFO, WARN, ERROR)

## 8. Testing

- Write unit tests for all public methods
- Use descriptive test method names: `testMethodName_Condition_Expected()`
- Aim for at least 80% code coverage
- Use assertions for validation

## 9. Code Organization

- One public class per file (except inner classes)
- Organize imports alphabetically
- Group related methods together
- Keep methods small and focused (under 20 lines when possible)

## 10. Security

- Validate all user inputs
- Use parameterized queries for database operations
- Never hardcode sensitive information (api keys, passwords)
- Use secure cryptographic algorithms
- Handle sensitive data carefully and log appropriately

---

**Remember**: Clean code is not written once and left alone. It's reviewed, refactored, and continuously improved.
