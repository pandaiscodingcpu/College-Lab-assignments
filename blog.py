# Simulated user database
users = {
    "alice": {"registered": True, "paid": True},
    "bob": {"registered": True, "paid": False},
    "charlie": {"registered": False, "paid": False}
}

# Decorator to check registration and payment
def blog_access(func):
    def wrapper(username):
        user = users.get(username)
        if not user:
            print(f"\nUser '{username}' is not registered. Please register to access the full blog.")
            choice = input("Do you want to register? (yes/no): ").strip().lower()
            if choice == "yes":
                users[username] = {"registered": True, "paid": False}
                print("Registration successful! You now need a membership to read the full blog.")
            else:
                print("Access denied. Only registered users can read the blog.")
                return
        elif not user["paid"]:
            print(f"\nHi {username}, you are registered but do not have a paid membership.")
            choice = input("Do you want to upgrade to paid membership? (yes/no): ").strip().lower()
            if choice == "yes":
                users[username]["paid"] = True
                print("Membership activated! You can now read the full blog.")
                return func(username)
            else:
                print("Access denied. Paid membership is required to read the full blog.")
                return
        else:
            return func(username)
    return wrapper

# The full blog content function
@blog_access
def read_full_blog(username):
    print(f"\nWelcome {username}!")
    print("Here is the full blog content:")
    print("""
    -------------------------------
    Title: 5 Ways to Learn Python
    -------------------------------
    1. Practice coding daily.
    2. Work on small projects.
    3. Read and explore others' code.
    4. Use online platforms for coding challenges.
    5. Never stop learning!
    -------------------------------
    """)

# Main program
if __name__ == "__main__":
    username = input("Enter your username: ").strip().lower()
    read_full_blog(username)
    print("\nThank you for visiting the blog!")
