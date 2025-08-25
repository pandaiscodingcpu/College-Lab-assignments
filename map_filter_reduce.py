
'''
map filter and reduce
'''

'''
PS: A real world application of map,filter and reduce and lambda functions is in data processing for finance or e-commerce:
Eg: calculating the total revenue  from a set of transactions where only certain orders qualify.
'''

from functools import reduce


numbers = [1,2,3,4,5,6]

squared = list(map(lambda x: x**2,numbers))
print("Squared: ",squared)

even_sq = list(filter(lambda x: x % 2 == 0,squared))
print("Even Squared: ",even_sq)

sum_even_sq = reduce(lambda x,y:x+y,even_sq)
print("Sum of even numbers: ",sum_even_sq)

orders = [
    {'amount':230,'completed':True},
    {'amount': 100, 'completed': True},
    {'amount': 230, 'completed': False},
    {'amount': 150, 'completed': True},
    {'amount': 0, 'completed': False},
    {'amount': 500, 'completed': True},
    {'amount': 230, 'completed': True},
    {'amount': 75, 'completed': False},
    {'amount': 300, 'completed': True},
]

completed_transactions = list(filter(lambda order: order['completed'],orders))
print("Completed Transactions: ",completed_transactions)

amounts = list(map(lambda order: order['amount'], completed_transactions))
print("Amounts: ",amounts)

total_amount = reduce(lambda a,b:a+b,amounts)
print("Total Amount: ",total_amount)


