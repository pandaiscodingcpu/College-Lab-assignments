def check_prime(num):
    for i in range(1,int(num ** 0.5)):
        if num % i == 0:
           return "Number is not prime"
    return "Number is not Prime"

print("Enter a number: ")
try:
    number = int(input())
    print(check_prime(number))
except ValueError as e:
    print(e)
    exit()
finally:
    print("Program terminated!!")