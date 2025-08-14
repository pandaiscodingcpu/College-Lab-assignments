# Normal if statement
age = 20
if age>=18:
    print("You are eligible to vote....")

# short hand if
age = 19
if age>=18:print("Eligible to vote....")


# if else condition

number = int(input("Enter a number: "))
print("Number is even") if number % 2 == 0 else print("Number is Odd")


# if -elif-else
marks = int(input("Enter the marks obtained...."))

if marks >= 90:
    print("Grade A+")
elif marks >= 75:
    print("Grade A")
elif marks >= 60:
    print("Grade B")
else:
    print("Grade C")


# nested if
if number > 0:
    print("Number is positive")
    if number % 3 == 0:
        print("Number is divisible by 3")
    else:
        print("Number is not divisible by 3")
else:
    print("Number is negative")