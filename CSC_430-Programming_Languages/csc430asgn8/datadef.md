# AST DATA FORMATS
All ASTs are stored as characters in a buffer with a fixed size of 50 characters.
This documentation details the data layout for every ExprC within this buffer.

### General Rule of Thumb:
    **Numbers** - Stored as 10 characters: PIC S9(5)V99999
        Numbers are signed and contain 5 decimal places.
    **Strings** - Stored as 10 characters: PIC X(10)

## NumC
Input Type: `'N'`

Attributes:
- `value` (Size 10)

## IdC
Input Type: `'I'`

Attributes:
- `sym` (Size 10)

## StrC
Input Type: `'S'`

Attributes:
- `string` (Size 10)

## IfC
Input Type: `'If'`

Attributes:
- `test` (Size 10)
- `then` (Size 10)
- `else` (Size 10)

## LamC (Work-in-Progress)
Attributes:
- `parameters` (Size 10n, n <= 4 and n is the no. of params) 
- `body` (Size 10)

## AppC
Input Type: `'A'`

Attributes:
- `name` (Size 10)
- `args` (Size 10n, n <= 4 and n is the no. of args)

# Environments & Values
The environment stores a maximum number of `BINDING`s which map `SYMBOLS` to `BOUND-VALS`. `BOUND-VALS` Represent the value bounded to the symbol and consists of two attributes:
1. `VAL-TYPES` - A single character denoting the type of the value
2. `VALS` - The value itself (Max 10 characters)

For example, the primitive operation of addition is stored in the top-level environment as element 1 and is represented by:
```
SYMBOLS(1) = "+"
VAL-TYPES(1) = "P"
VALS(1) = "+"
```

Below are all the suffixes for each value type:
```
- 'P' (Used for Primitives)
- 'B' (Used for Booleans)
- 'N' (Used for Numbers, refer to the above Data Formats for constraints)
- 'C' (Used for Closures)
```