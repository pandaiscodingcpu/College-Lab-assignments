import random

# Invalid Account number exception: if account number is not 12 digit
class InvalidAccountNumber(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
    def __str__(self):
        return f"{self.message} (Error code: {self.error_code})"


# Amount Withdraw exception: if current amount is more than the balance
class AmountWithdrawExceeded(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
    def __str__(self):
        return f"{self.message} (Error code: {self.error_code})"


# Wrong otp exception: Incorrect otp
class WrongOTP(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
    def __str__(self):
        return f"{self.message} (Error code: {self.error_code})"

# main bank class
class Bank:
    def __init__(self):
        # Random balance 
        self.current_bank_balance = random.randint(2000, 10000)
        self.pin = "1234"  # Default PIN

    def validateAccount(self):
        account_number = input("Enter your Account Number: ").strip()
        valid_length = 12
        # user will get maximum of 5 attempts to enter their correct AC number
        max_attempts = 5
        attempt = 1 # count of current attempts
        while attempt <= max_attempts:
            try:
                if len(account_number) != valid_length or not account_number.isdigit():
                    raise InvalidAccountNumber("Invalid account number", 1000)
                else:
                    print("Account number verified.")
                    return True
            except InvalidAccountNumber as e:
                print(e)
                if attempt == max_attempts:
                    print("Maximum attempts reached. Account is locked.")
                    return False
                account_number = input("Re-enter your account number: ").strip()
                attempt += 1
        return False

    # function for OTP verification
    def otpVerification(self):
        otp = random.randint(1000, 9999) # random otp
        print(f"(For demo) OTP sent to registered mobile: {otp}")
        otp_attempts = 1 # current otp attempt
        while otp_attempts <= 3:
            try:
                user_otp = int(input("Enter the OTP: "))
                if user_otp != otp:
                    raise WrongOTP("Invalid OTP entered", 3000)
                else:
                    print("OTP verified successfully.")
                    return True
            except WrongOTP as e:
                print(e)
                otp_attempts += 1
                if otp_attempts == 3:
                    print("Too many wrong OTP attempts. Transaction cancelled.")
                    return False
            except ValueError:
                print("OTP must be numeric.")
                otp_attempts += 1
        return False

    # withdraw amount function
    def withdrawAmount(self):
        # try-exception block for checking if the balance is non-negative
        try: 
            amount_withdraw = int(input("Enter amount to withdraw: "))
            if amount_withdraw > self.current_bank_balance:
                raise AmountWithdrawExceeded("Withdrawal amount exceeds balance", 2000)
            else:
                self.current_bank_balance -= amount_withdraw
                print(f"Withdrawal successful. Remaining Balance: {self.current_bank_balance}")
        except AmountWithdrawExceeded as e:
            print(e)
        except ValueError:
            print("Please enter a valid number.")
    
    # deposit amount function
    def depositAmount(self):
        try:
            deposit = int(input("Enter amount to deposit: "))
            if deposit <= 0:
                print("Deposit amount must be positive.")
                return
            self.current_bank_balance += deposit
            print(f"Deposit successful. Current Balance: {self.current_bank_balance}")
        except ValueError:
            print("Please enter a valid number.")

    # checking the balance
    def checkBalance(self):
        print(f"Current Balance: {self.current_bank_balance}")

    # changing the pin 
    def changePIN(self):
        old_pin = input("Enter your current PIN: ").strip()
        if old_pin != self.pin:
            print("Incorrect current PIN.")
            return
        new_pin = input("Enter new 4-digit PIN: ").strip()
        if len(new_pin) == 4 and new_pin.isdigit():
            self.pin = new_pin
            print("PIN changed successfully.")
        else:
            print("PIN must be exactly 4 digits.")

    # validating account using account number and otp
    def mainMenu(self):
        if not self.validateAccount():
            return
        if not self.otpVerification():
            return
        
        # Menu driven options
        while True:
            print("\n--- ATM MENU ---")
            print("1. Withdraw")
            print("2. Deposit")
            print("3. Check Balance")
            print("4. Change PIN")
            print("5. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                self.withdrawAmount()
            elif choice == "2":
                self.depositAmount()
            elif choice == "3":
                self.checkBalance()
            elif choice == "4":
                self.changePIN()
            elif choice == "5":
                print("Thank you for using our ATM.")
                break
            else:
                print("Invalid choice. Try again.")
if __name__ == "__main__":
    bank = Bank()
    bank.mainMenu()
