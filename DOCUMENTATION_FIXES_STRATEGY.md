# Documentation Warnings Fix Strategy

## Overview
There are 728 documentation warnings across the functional test LimeIDL files that need to be fixed. These warnings fall into two categories:

1. **Function/Method Documentation**: Missing `@param` and `@return` tags
2. **Lambda Documentation**: Missing parameter and return documentation for lambda types

## Files with Most Warnings (Priority Order)
1. Lambdas.lime - 55 warnings
2. StaticIntMethods.lime - 48 warnings
3. MethodOverloads.lime - 37 warnings
4. Equatable.lime - 35 warnings
5. Nullability.lime - 34 warnings

## Documentation Format
Based on the smoke tests, the correct format is:

```lime
// Function documentation
// @param[parameter_name] description of parameter
// @return description of return value
fun functionName(parameter: Type): ReturnType

// Lambda documentation
// @param[p0] description of first parameter
// @param[p1] description of second parameter
// @return description of return value
lambda LambdaName = (Type, Type) -> ReturnType
```

## Approach
1. Fix functions by adding `@param` and `@return` tags
2. Fix lambdas by adding parameter and return documentation
3. Use descriptive but generic documentation that fits the context
4. Verify fixes by running the build again

## Example Fixes

### Before:
```lime
fun getName(): String
fun processData(data: String): Boolean
lambda StringProcessor = (String) -> String
```

### After:
```lime
// @return the name as a string
test getName(): String

// @param[data] the data to process
// @return true if processing was successful, false otherwise
fun processData(data: String): Boolean

// @param[p0] the string to process
// @return the processed string
lambda StringProcessor = (String) -> String
```

## Files to Fix (Top Priority)
1. Lambdas.lime - Lambda and function documentation
2. StaticIntMethods.lime - Function documentation
3. MethodOverloads.lime - Function overload documentation
4. StaticStringMethods.lime - String function documentation
5. Interfaces.lime - Interface method documentation

## Verification
After fixing files, run:
```bash
./functional-tests/scripts/build-python-functional --verbose 2>&1 | grep "WARNING.*must be documented"
```
To verify the warnings are reduced/eliminated.
