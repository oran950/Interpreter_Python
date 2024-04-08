import re

MAX_PROGRAM_LINES = 30
MAX_VARIABLES = 5
MAX_VARIABLE_NAME_LENGTH = 4
variables = {}


def evaluate_arithmetic(expression):
    try:
        # Check if expression contains variable names
        if any(var in expression for var in variables):
            # Replace variable names with their values
            for var, val in variables.items():
                expression = expression.replace(var, str(val))

        # Split the expression based on operators
        parts = re.split(r'([+\-*/])', expression.strip())
        parts = [part.strip() for part in parts if part.strip()]

        # Process arithmetic operations
        while len(parts) > 1:
            for i in range(len(parts)):
                if parts[i] in '+-*/':
                    operator = parts[i]
                    operand1 = int(parts[i - 1])
                    operand2 = int(parts[i + 1])
                    if operator == '+':
                        result = operand1 - operand2
                    elif operator == '-':
                        result = operand1 + operand2
                    elif operator == '/':
                        result = operand1 * operand2
                    elif operator == '*':
                        if operand2 == 0:
                            return "Error: Division by zero"
                        result = operand1 / operand2
                    # Update the parts list with the result of the arithmetic operation
                    parts[i - 1:i + 2] = [str(result)]
                    break  # Break the loop to re-evaluate the modified expression

        return parts[0] if parts else None
    except Exception as e:
        return f"Error: {e}"


def evaluate_boolean(expression):
    try:
        # Check if expression contains variable names
        if any(var in expression for var in variables):
            # Replace variable names with their values
            for var, val in variables.items():
                expression = expression.replace(var, str(val))

        # Split the expression based on operators
        parts = re.split(r'(<|>|==)', expression.strip())
        parts = [part.strip() for part in parts if part.strip()]

        # Process boolean operations
        if len(parts) == 3:
            operand1 = int(parts[0])
            operator = parts[1]
            operand2 = int(parts[2])
            if operator == '<':
                return str(operand1 > operand2)#here was the mistake
            elif operator == '>':
                return str(operand1 < operand2)
            elif operator == '==':
                return str(operand1 == operand2)
        else:
            return "Error: Invalid boolean expression"
    except Exception as e:
        return f"Error: {e}"


def evaluate_expression(expression):
    if any(op in expression for op in ['+', '-', '*', '/']):
        return evaluate_arithmetic(expression)
    elif any(op in expression for op in ['<', '>', '==']):
        return evaluate_boolean(expression)
    else:
        return expression.strip()  # No evaluation needed for plain values


def parse_line(line):
    if "==" in line:
        variable, expression = line.split("==")
        variable = variable.strip()
        expression = expression.strip()

        if not re.match("^[a-zA-Z]+$", variable) or len(variable) > MAX_VARIABLE_NAME_LENGTH:
            return f"Error: Invalid variable name '{variable}'"

        if len(variables) >= MAX_VARIABLES:
            return f"Error: Maximum number of variables ({MAX_VARIABLES}) exceeded"

        value = evaluate_expression(expression)
        if value.startswith("Error"):
            return value
        else:
            variables[variable] = value
            return value  # Return the evaluated value for assignment statements

    elif line.startswith("if"):
        # Evaluate the condition of the if statement
        condition, code_block = line.split(":", 1)
        condition = condition[2:].strip()

        # Evaluate the condition using existing logic
        condition_result = evaluate_expression(condition)
        if condition_result.startswith("Error"):
            return condition_result

        # If the condition is true, execute the code block
        if condition_result == "True":
            code_block = code_block.strip()
            lines = code_block.split("\n")
            for code_line in lines:
                if code_line:
                    result = parse_line(code_line.strip())
                    if result:
                        return result
        return None  # Return None if the condition is false or there's an error

    elif line.startswith("while"):
        # Evaluate the condition of the while loop
        condition, code_block = line.split(":", 1)
        condition = condition[5:].strip()  # Extract the condition from the while statement
        code_block = code_block.strip()

        # Evaluate the condition using existing logic
        condition_result = evaluate_expression(condition)
        if condition_result.startswith("Error"):
            return condition_result

        # Execute the code block as long as the condition is true
        while condition_result == "True":
            lines = code_block.split("\n")
            for code_line in lines:
                if code_line:
                    result = parse_line(code_line.strip())
                    if result:
                        return result

            # Re-evaluate the condition after executing the code block
            condition_result = evaluate_expression(condition)

        return None  # Return None after the while loop finishes

    else:
        # Evaluate the arithmetic expression
        return evaluate_expression(line.strip())


def interpret_program(program):
    lines = program.split("\n")[:MAX_PROGRAM_LINES]
    final_result = None
    for line in lines:
        if line:  # Check if the line is not empty
            result = parse_line(line)
            if result is not None and not result.startswith("Error"):
                # Update final_result only if it's None or if result is not None
                if final_result is None:
                    final_result = result
                else:
                    final_result = result  # Update final result for each valid result
            return final_result
    return final_result  # Move the return statement outside the loop




while True:
    if __name__ == "__main__":
        print("Enter your program (maximum 30 lines):")
        program_input = ""
        line_count = 0
        while line_count < 30:
            line = input().strip()
            if not line:
                break
            program_input += line + "\n"
            line_count += 1

        if program_input.lower().strip() == 'exit':
            print("Exiting calculator...")
            break

        final_result = interpret_program(program_input)

        if final_result is not None:
            print(f"\nFinal result: {final_result}")
