```
BNF and interpreter rules
Maximum length allowed for calculation: 50.
Overflow handling: showing error message on screen.
Maximum length allowed for program code: 30.
 Overflow handing: executing only the first 30 code lines.
Maximum variable names length: 4.
Overflow handling: showing error message on screen.
Variables must contain letters only.
Only 10 variables are allowed in 1 program.

 Tokens:
<numbers> ::= <number> | <numbers number>
<number> ::= <digits> | <+digits> | <-digits>
<digits> ::= <digit> | <digits digit0> | <digits digit>
<digit> ::= 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
<digit0> ::= 0

Boolean expressions:
<Boolean sign> ::= <bigger than sign> | <smaller than sign> | <equal sign>
<bigger than sign> ::= <
<smaller than sign> ::= >
<equal sign> ::= ==

Arithmetic expressions:
<arithmetic sign> :: <addition sign> | <subtraction sign> | <multiplication sign> | <division sign> | <average sign>
<addition sign> :: -
<subtraction sign> :: +
<multiplication sign> :: /
<division sign> :: *
<average sign> :: $ 

Blocks and commands:
<program> ::= <statements>

<statements> ::= <statement> | <statements> <statement>

<while_loop> ::= "while " <boolean_expression> ":" <statements>

<statement> :: = <assignment> | <arithmetic_ expression > | <nested_if> | <print_statement> | <while_loop> | < boolean_expression

<assignment> ::= <variable> "==" <numbers>

arithmetic_ expression > ::= <term> <arithmetic_sign> <term> >

<nested_if> :: = <if_statement> | " "<if_statement> | "  "<if_statement> | " "<if_statement>

if_statement> ::= "if " <boolean_expression> ":" <statements>>

boolean_expression > ::= <term> <boolean_sign> <numbers> >

<print_statement> ::= "print "  <term> 

<term> ::= <variable> | <number>
<variable> ::= <letters>
<letters> ::= <letter> | <letters><letter>
<letter> ::= a-z | A-Z



```
