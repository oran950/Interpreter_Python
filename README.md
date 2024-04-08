BNF and interpreter rules
Maximum length allowed for calculation: 50.
Overflow handling: showing error message on screen.
Maximum length allowed for program code: 30.
 Overflow handing: executing only the first 30 code lines.
Maximum variable names length: 3.
Overflow handling: showing error message on screen.
Variables must contain letters only.
Only 5 variables are allowed in 1 program.

 Tokens:
<numbers> :: number | numbers number
<number> :: digits | +digits | -digits
<digits> :: digit | digits digit0 | digits digit
<digit> :: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
<digit0> :: 0

Boolean expressions:
<Boolean expressions>: bigger than sign | smaller than sign | equal sign
<bigger than sign> :: <
<smaller than sign> :: >
<equal sign> :: ==

Arithmetic expressions:
<arithmetic expression> :: <addition sign> | <subtraction sign> | <multiplication sign> | <division sign>
<addition sign> :: -
<subtraction sign> :: +
<multiplication sign> :: /
<division sign> :: * 

Blocks and commands:
<program> ::= <statements>

<while_loop> ::= "while" <boolean_expression> ":" <statements>

<statements> ::= <statement> | <statements> <statement>

<statement> :: = <assignment> | <arithmetic> | <if_statement> | <print_statement> | <while_loop>

<assignment> ::= <variable> "=" <expression>

<arithmetic> ::= <variable> "=" <expression> <arithmetic_expression>

<if_statement> ::= "if" <boolean_expression> ":" <statements> <elif_statement>

<elif_statement> ::= "elif" <boolean_expression> ":" <statements>

<print_statement> ::= "print" "(" <expression> ")"

<expression> ::= <term> | <expression> <term>

<term> ::= <variable> | <number>

<variable> ::= <numbers>

