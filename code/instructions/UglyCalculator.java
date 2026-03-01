package com.calculator;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * Calculator class that performs basic arithmetic operations.
 * Maintains a history of all operations performed.
 */
public class UglyCalculator {

    private int result = 0;
    private Optional<String> lastOperation;
    private final List<String> operations;

    /**
     * Constructs a new UglyCalculator instance with empty operation history.
     */
    public UglyCalculator() {
        this.operations = new ArrayList<>();
        this.lastOperation = Optional.empty();
    }

    /**
     * Adds two numbers and stores the result.
     *
     * @param firstNumber the first number to add
     * @param secondNumber the second number to add
     */
    public void add(int firstNumber, int secondNumber) {
        result = firstNumber + secondNumber;
        lastOperation = Optional.of("add");
        operations.add("add");
    }

    /**
     * Subtracts second number from first number and stores the result.
     *
     * @param firstNumber the number to subtract from
     * @param secondNumber the number to subtract
     */
    public void subtract(int firstNumber, int secondNumber) {
        result = firstNumber - secondNumber;
        lastOperation = Optional.of("subtract");
        operations.add("subtract");
    }

    /**
     * Multiplies two numbers and stores the result.
     *
     * @param firstNumber the first number to multiply
     * @param secondNumber the second number to multiply
     */
    public void multiply(int firstNumber, int secondNumber) {
        result = firstNumber * secondNumber;
        lastOperation = Optional.of("multiply");
        operations.add("multiply");
    }

    /**
     * Divides first number by second number and stores the result.
     *
     * @param dividend the number to be divided
     * @param divisor the number to divide by
     * @throws IllegalArgumentException if divisor is zero
     */
    public void divide(int dividend, int divisor) {
        if (divisor == 0) {
            throw new IllegalArgumentException(
                "Divisor cannot be zero");
        }
        result = dividend / divisor;
        lastOperation = Optional.of("divide");
        operations.add("divide");
    }

    /**
     * Returns the current result of the last operation.
     *
     * @return the current result as an integer
     */
    public int getResult() {
        return result;
    }

    /**
     * Returns the last operation performed.
     *
     * @return Optional containing the last operation, or empty if
     *         none performed
     */
    public Optional<String> getLastOperation() {
        return lastOperation;
    }

    /**
     * Clears the result and operation history.
     */
    public void clearAll() {
        result = 0;
        lastOperation = Optional.empty();
        operations.clear();
    }

    /**
     * Prints the history of all operations performed.
     */
    public void printHistory() {
        System.out.println("Operation History:");
        for (String operation : operations) {
            System.out.println("  - " + operation);
        }
    }

    /**
     * Performs a calculation based on the specified operation.
     *
     * @param operation the operation to perform (add, sub, mul, div)
     * @param firstNumber the first operand
     * @param secondNumber the second operand
     * @throws IllegalArgumentException if operation is not recognized
     * @throws IllegalArgumentException if divisor is zero in division
     */
    public void performCalculation(String operation, int firstNumber,
                                    int secondNumber) {
        switch (operation) {
            case "add":
                add(firstNumber, secondNumber);
                break;
            case "sub":
                subtract(firstNumber, secondNumber);
                break;
            case "mul":
                multiply(firstNumber, secondNumber);
                break;
            case "div":
                divide(firstNumber, secondNumber);
                break;
            default:
                throw new IllegalArgumentException(
                    "Unknown operation: " + operation);
        }
    }

    /**
     * Main method to demonstrate the calculator functionality.
     *
     * @param args command line arguments (not used)
     */
    public static void main(String[] args) {
        UglyCalculator calculator = new UglyCalculator();

        calculator.add(10, 20);
        calculator.subtract(50, 30);
        calculator.multiply(5, 6);
        calculator.divide(100, 5);

        System.out.println("Result: " + calculator.getResult());
        calculator.printHistory();
    }
}
