'''
Create an employee management system with following features:
1. Take necessary details of the employee
2. Store the details in the form of dictionary
3. Store that dictionary in list
4. Add features like adding an employee, removing and employee etc.
5. Give a neatly formatted output
'''
from mpmath.ctx_mp_python import return_mpc

# list to store employees
employees = []

# dictionary to store employee details
emp_details = {
    'id':0,
    'name':"",
    'age':0,
    'salary':0,
    'role':"",
    'email':""
}

# taking user input for total number of employees
number_of_emp = int(input("Enter total number of employees: "))
for i in range(number_of_emp):
    print(f"\t\nEmployee {i+1}\n") # taking details for employee i+1
    emp_details['id'] = int(input("Enter ID: "))
    emp_details['name'] = str(input("Enter Name: "))
    emp_details['age'] = int(input("Enter Age: "))
    emp_details['salary'] = int(input("Enter Salary: "))
    emp_details['role'] = str(input("Enter Role: "))
    emp_details['email'] = str(input("Enter email: "))
    # storing the details in a list using copy() function
    employees.append(emp_details.copy())


# formatting and displaying
print("\n\tALL THE EMPLOYEE DETAILS HAVE BEEN ADDED TO THE SYSTEM\t\n")


while True:
    print("What would you like to do next??\n1. Add an employee\n2. Remove an Employee\n3. Sort the system\n4. Display the records\n5. Exit")
    option = int(input("Enter your choice: "))
    if option == 5:
        print("\nEXITING>>>>>")
        break
    if option == 1:
        print(f"\t\nEmployee {len(employees) + 1}\n")  # taking details for employee i+1
        emp_details['id'] = int(input("Enter ID: "))
        emp_details['name'] = str(input("Enter Name: "))
        emp_details['age'] = int(input("Enter Age: "))
        emp_details['salary'] = int(input("Enter Salary: "))
        emp_details['role'] = str(input("Enter Role: "))
        emp_details['email'] = str(input("Enter email: "))
        # storing the details in a list using copy() function
        employees.append(emp_details.copy())
        print("\nEmployee added successfully....\n")
    elif option == 2:
        id_rem = int(input("Enter the ID of the employee to remove: "))
        found = False
        for emp in employees:
            if emp['id'] == id_rem:
                employees.remove(emp)
                print(f"Employee with ID {id_rem} removed successfully.")
                found = True
                break
        if not found:
            print(f"Sorry....NO EMPLOYEE WITH ID {id_rem}")

    elif option == 3:
        print("Sort by:\n1. ID\n2. Name\n3. Salary")
        sort_choice = int(input("Enter your choice: "))
        if sort_choice == 1:
            employees.sort(key=lambda x: x['id'])
        elif sort_choice == 2:
            employees.sort(key=lambda x: x['name'].lower())
        elif sort_choice == 3:
            employees.sort(key=lambda x: x['salary'])
        print("Employees sorted successfully.")

    elif option == 4:
        print("\n---- Employee Records ----")
        print("{:<5} {:<15} {:<5} {:<10} {:<15} {:<25}".format("ID","NAME","AGE","SALARY","ROLE","EMAIL"))
        print("-"*100)
        for emp in employees:
            print("{:<5} {:<15} {:<5} {:<10} {:<15} {:<25}".format(emp['id'], emp['name'], emp['age'], emp['salary'], emp['role'], emp['email']))
        print("-"*100)