import re

class InvalidIdError(Exception):
    """Custom exception for invalid account ID."""
    def __init__(self, message="Invalid ID format. Please enter a valid ID (numeric only)."):
        self.message = message
        super().__init__(self.message)

class InvalidNameError(Exception):
    """Custom exception for invalid account name."""
    def __init__(self, message="Invalid name. Name should contain only letters and spaces."):
        self.message = message
        super().__init__(self.message)

class BankAccount:
    def __init__(self, id, name, amount):
        self.id = id
        self.name = name
        self.amount = amount

    def deposit(self, amt_deposit):
        if amt_deposit <= 0:
            print("Deposit amount must be positive.")
            return
        self.amount += amt_deposit
        print(f"{amt_deposit} deposited successfully to {self.name}'s account.")

    def withdraw(self, amt_withdraw):
        if amt_withdraw <= 0:
            print("Withdraw amount must be positive.")
            return
        if amt_withdraw > self.amount:
            print("Sorry, insufficient balance.")
        else:
            self.amount -= amt_withdraw
            print(f"{amt_withdraw} withdrawn successfully from {self.name}'s account.")

    def transfer(self, amt_transfer, other_account):
        if amt_transfer <= 0:
            print("Transfer amount must be positive.")
            return
        if amt_transfer > self.amount:
            print("Sorry, insufficient balance.")
        else:
            self.amount -= amt_transfer
            other_account.amount += amt_transfer
            print(f"Amount {amt_transfer} transferred to {other_account.name}.")

    def show_balance(self):
        print(f"Current balance of {self.name} ({self.id}): {self.amount}")

    def __str__(self):
        return f"Account[{self.id}] - {self.name}, Balance: {self.amount}"

def get_account_input(account_num):
    """Helper function to get valid account details."""
    while True:
        try:
            id = input(f"Enter ID for Account {account_num} (numeric only): ")
            if not re.match(r'^\d+$', id):
                raise InvalidIdError()
            
            name = input(f"Enter name for Account {account_num}: ")
            if not re.match(r'^[A-Za-z ]+$', name):
                raise InvalidNameError()

            amount = float(input(f"Enter initial balance for Account {account_num}: "))
            if amount < 0:
                print("Initial balance cannot be negative. Please try again.")
                continue

            return id, name, amount

        except InvalidIdError as e:
            print(e)
        except InvalidNameError as e:
            print(e)
        except ValueError:
            print("Invalid input for balance. Please enter a valid number.")

def get_amount_input(prompt):
    """Helper to get valid amount input."""
    while True:
        try:
            amt = float(input(prompt))
            if amt <= 0:
                print("Amount must be positive. Try again.")
                continue
            return amt
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

# Get details for both accounts
id1, name1, amount1 = get_account_input(1)
account_a = BankAccount(id1, name1, amount1)

id2, name2, amount2 = get_account_input(2)
account_b = BankAccount(id2, name2, amount2)

print("\nAccounts created successfully:\n")
print(account_a)
print(account_b)

# Get deposit amount from user and deposit
deposit_amount = get_amount_input(f"\nEnter amount to deposit into {account_a.name}'s account: ")
account_a.deposit(deposit_amount)

# Get withdraw amount from user and withdraw
withdraw_amount = get_amount_input(f"Enter amount to withdraw from {account_a.name}'s account: ")
account_a.withdraw(withdraw_amount)

# Get transfer amount from user and transfer
transfer_amount = get_amount_input(f"Enter amount to transfer from {account_a.name} to {account_b.name}: ")
account_a.transfer(transfer_amount, account_b)

print("\nAfter transactions:\n")
print(account_a)
print(account_b)
