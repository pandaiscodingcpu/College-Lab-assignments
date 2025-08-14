number = int(input("Enter a number: "))
temp = str(number)
if temp[::-1] == str(number):
    print("Palindrome")
else:
    print("not palindrome")