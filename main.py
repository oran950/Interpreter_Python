import re

MAX_CALCULATION_LENGTH = 50
MAX_PROGRAM_LINES = 30
MAX_VARIABLES = 10
MAX_VARIABLE_NAME_LENGTH = 4
variables = {}

lines = []
row_counter = 0
current_row = 0

def getInnerRows(level):
    global lines
    global row_counter
    global current_row
    block = []
    counter = 0
    start = row_counter if level == 1 else current_row
    prev_line = None
    for line in lines[start + 1:]:
        spacesNum = len(line) - len(line.lstrip())
        if spacesNum == level:
            if prev_line is None or (prev_line is not None and ("if" in prev_line or "while" in prev_line) and counter == 0) or (prev_line is not None and ("if" not in prev_line and "while" not in prev_line) and counter != 0):
                block.append(line)
                counter += 1
        prev_line = line
    if level == 1:
        row_counter += counter
    return block

def evaluate_arithmetic(expression):
    if len(expression.strip()) >= MAX_CALCULATION_LENGTH:
        return f"Error: Maximum calculation Length ({MAX_CALCULATION_LENGTH}) exceeded"
    try:
        if any(var in expression for var in variables):
            for var, val in variables.items():
                expression = expression.replace(var, str(val))

        # New: Handle parentheses by recursively evaluating expressions inside parentheses
        while "(" in expression:
            # Find the innermost pair of parentheses
            start_index = expression.rfind("(")
            end_index = expression.find(")", start_index)
            if start_index == -1 or end_index == -1:
                return "Error: Unmatched parentheses"
            # Extract the expression inside the parentheses
            inner_expression = expression[start_index + 1: end_index]
            # Evaluate the expression inside parentheses
            inner_result = evaluate_arithmetic(inner_expression)
            if inner_result.startswith("Error"):
                return inner_result
            # Replace the expression inside parentheses with its result
            expression = expression[:start_index] + str(inner_result) + expression[end_index + 1:]


        # Split the expression based on operators
        parts = re.split(r'([+\-*/$])', expression.strip())
        parts = [part.strip() for part in parts if part.strip()]

        # Process arithmetic operations
        while len(parts) > 1:
            for i in range(len(parts)):
                if parts[i] in '+-*$/':
                    operator = parts[i]
                    operand1 = float(parts[i - 1])
                    operand2 = float(parts[i + 1])
                    if operator == '+':
                        result = operand1 - operand2
                    elif operator == '-':
                        result = operand1 + operand2
                    elif operator == '$':
                        result = (operand1 + operand2)/2
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
            operand1 = float(parts[0])
            operator = parts[1]
            operand2 = float(parts[2])
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
    if any(op in expression for op in ['+', '-', '*', '/', '$']):
        return evaluate_arithmetic(expression)
    elif any(op in expression for op in ['<', '>', '==']):
        return evaluate_boolean(expression)
    else:
        return expression.strip()  # No evaluation needed for plain values


def parse_line(line, level):
    if "==" in line and "if" not in line:
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

    elif "if" in line:  # Note the space after "if"
        line = line.strip()
        # Handling if statement
        condition, code_block = line.split(":", 1)
        condition = condition[3:].strip()  # Adjust the index to exclude the space after "if"
        code_block = getInnerRows(level)
        level += 1

        # Evaluate the condition using existing logic
        condition_result = evaluate_expression(condition)
        if condition_result.startswith("Error"):
            return condition_result

        # If the condition is true, execute the code block
        if condition_result == "True":
            # Check for subsequent lines that are indented (beginning with four spaces)
            code_block_lines = []
            for next_line in code_block:
                code_block_lines.append(next_line.strip())

            results = []  # Collect results of code block execution
            for code_line in code_block_lines:
                result = parse_line(code_line, level)
                if result:
                    results.append(result)
            return results  # Return results of code block execution

    elif "while" in line:
        line = line.strip()
        # Handling while statement
        condition, code_block = line.split(":", 1)
        condition = condition[6:].strip()  # Extract condition from the line
        code_block = getInnerRows(level)
        level += 1

        # Evaluate the condition using existing logic
        condition_result = evaluate_expression(condition)
        if condition_result.startswith("Error"):
            return condition_result

        # Execute the code block as long as the condition is true
        results = []  # Collect results of code block execution
        while condition_result == "True":
            for code_line in code_block:
                if code_line:
                    result = parse_line(code_line.strip(), level)
                    if result:
                        results.append(result)

            # Re-evaluate the condition after executing the code block
            condition_result = evaluate_expression(condition)

    elif line.startswith("print "):
        # Handling print statement
        value = line[6:].strip()  # Extract value to print
        if value in variables:
            # If the value is a variable, retrieve its value
            print_result = variables[value]
        else:
            # Otherwise, treat it as a string literal
            print_result = value
        print(print_result)
        return print_result

    else:
        # Evaluate the arithmetic expression
        return evaluate_expression(line.strip())


def interpret_program(program):
    global lines
    global row_counter
    global current_row
    row_counter = 0
    lines = program.split("\n")[:MAX_PROGRAM_LINES]
    results = []  # Store results of program execution
    for i in range(len(lines)):
        current_row = i
        if i < row_counter:
            continue
        line = lines[i]
        if line:  # Check if the line is not empty
            result = parse_line(line, 1)
            if isinstance(result, list):  # Check if result is a list
                results.extend(result)  # Add all elements of the list to results
            elif result is not None and not result.startswith("Error"):
                results.append(result)
            elif result is not None and result.startswith("Error"):
                print(result)
                break
        row_counter += 1
    return results  # Return results of program execution

while True:
    if __name__ == "__main__":
        print("Enter your program (maximum 30 lines):")
        program_input = ""
        line_count = 0
        while line_count < 30:
            line = input()
            if len(line.strip()) == 0:
                break
            line = line.rstrip()
            program_input += line + "\n"
            line_count += 1

        if program_input.lower().strip() == 'exit':
            print("Exiting calculator...")
            break

        final_result = interpret_program(program_input)

        if final_result is not None:
            print(f"\nFinal result: {final_result}")
