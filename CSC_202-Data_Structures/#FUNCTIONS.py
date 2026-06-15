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