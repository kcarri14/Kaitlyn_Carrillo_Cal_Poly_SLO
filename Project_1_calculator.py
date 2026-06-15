#FUNCTIONS
def add(a, b):   #function to add both inputs
  return a + b

def subtract(a,b):   #function to subtract the first number by the second
  return a - b

def multiply(a,b):  #function to multiply both inputs
  return a * b

def divide(a,b):  #function to divide the first number by the second
  return a / b

def floor_division(a,b):  #function to floor division the first number by the second which cuts off the remainder
  return a // b

def modulus(a,b):  #function to modulus the first number by the second
  return a % b

def power(a,b):  #function to bring a to the power of b
  return a**b

def square_root(a,b):   #function to square root using the desired root
  return a**(1/b)


#INTERFACE

#A welcoming note to the calculator
print(" ---------------------- ")
print("Hello! Welcome to Kaitlyn's Calculator!")
print(" ---------------------- ")
#Tells the rules of the calculator
print("Rules")
print("1. If dividing, using modulus, or floor division, second number must not be zero")
print("2. If using the square root, you must type out 'square root' into the operations section")
print("3. When using square root, the first number is the one inside the square root and the second is the desired root you want to use")
print("4. No negatives when using square root")
print(" ---------------------- ")
#Asks the user to input the First number they want to compute
x = float(input("First Number: "))
print(" ---------------------- ")
#Asks the user to input the operation they want to use
choose_number = str(input("Please input an operation(+,-,*,/,//,%,**): "))
print(" ---------------------- ")
#Asks the user to input the Second Number they want to compute
y = float(input("Second Number: "))
print(" ---------------------- ")


#PERFORMANCE

#Performs the operation based on the user's input and prints the answer
if choose_number == "+": #if operation is "+"
  print("Answer: ", add(x,y))
elif choose_number == "-":  #if operation is "-"
  print("Answer: ", subtract(x,y))
elif choose_number == "*":   #if operation is "*"
  print("Answer: ", multiply(x,y))
elif choose_number == "/":   #if operation is "/"
  print("Answer: ", divide(x,y))
elif choose_number == "//":   #if operation is "//"
  print("Answer: ", floor_division(x,y))
elif choose_number == "%":   #if operation is "%"
  print("Answer: ", modulus(x,y))
elif choose_number == "**":   #if operation is "**"
  print("Answer: ", power(x,y))
elif choose_number == "square root":
    print("Answer: ", square_root(x,y))
else :                        #if the inputs are not operations it will print out "Invalid inputs"
  print("Invalid Inputs")


#TESTS

#tests the various cases and edge cases and displays the results
def testing_function():
  result = add(1,3)                       #tests the add function for simple cases
  assert result == 4, f"Expected 4, but got {result}"

  result = subtract(4,3)                       #tests the subtract function for simple cases
  assert result == 1, f"Expected 1, but got {result}"

  result = multiply(10,3)                       #tests the multiply function for simple cases
  assert result == 30, f"Expected 30, but got {result}"

  result = divide(28,4)                       #tests the divide function for simple cases
  assert result == 7, f"Expected 4, but got {result}"

  result = modulus(6,3)                       #tests the modulus function for simple cases
  assert result == 0, f"Expected 0, but got {result}"

  result = floor_division(9,3)                       #tests the floor division function for simple cases
  assert result == 3, f"Expected 3, but got {result}"

  result = power(6,2)                       #tests the power function for simple cases
  assert result == 36, f"Expected 4, but got {result}"

  result = multiply(150,3)                       #tests the mulitply function for simple cases
  assert result == 450, f"Expected 450, but got {result}"

  result = divide(65.38,75.9)                       #tests the divide function for edge cases
  assert result == 0.8613965744400526, f"Expected 0.8613965744400526, but got {result}"

  result = multiply(9587580,73940)                       #tests the multiply function for edge cases
  assert result == 708905665200, f"Expected 708905665200, but got {result}"

  result = modulus(73493,890)                       #tests the modulus function for edge cases
  assert result == 513, f"Expected 513, but got {result}"

  result = add(23984723,20394823)                       #tests the add function for edge cases
  assert result == 44379546, f"Expected 708905665200, but got {result}"

  result = subtract(8430984309,9090898)                       #tests the subtract function for edge cases
  assert result == 8421893411, f"Expected 8421893411, but got {result}"

  result = power(784,54)                       #tests the power function for edge cases
  assert result == 1963664934673089874884556153736029298585448572928851665221485147713909491544548935628445299989616397707897858918119919465183498421634121426425971096038670336, f"Expected 1963664934673089874884556153736029298585448572928851665221485147713909491544548935628445299989616397707897858918119919465183498421634121426425971096038670336, but got {result}"

  result = floor_division(2387423,4634)                       #tests the floor division function for edge cases
  assert result == 515, f"Expected 515, but got {result}"

  result = square_root(345,2)                       #tests the square root function for edge cases
  assert result == 18.57417562100671, f"Expected 18.57417562100671, but got {result}"

  result = square_root(16,2)                       #tests the square root function for simple cases
  assert result == 4, f"Expected 4, but got {result}"

  result = square_root(3245,4)                       #tests the square root function for edge cases
  assert result == 7.547509620696383, f"Expected 7.547509620696383, but got{result}"


  print("All tests passed")

#Runs the tests
testing_function()