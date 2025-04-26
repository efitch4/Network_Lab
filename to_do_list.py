# Simple To-Do List App
print("Welcome to the To-Do List App!")

to_do_list = []

def show_menu():
    print("\nOptions:")
    print("1. Add a task")
    print("2. View all tasks")
    print("3. Remove a task")
    print("4. Exit")

while True:
    show_menu()
    choice = input("Choose an option (1-4):").strip()

    if choice == "1":
        task = input("Enter a task: ").strip()
        to_do_list.append(task)
        print(f"Task '{task}' added!")

    elif choice =="2":
        if to_do_list:
            print("\nYour to do List:")
            for i, task in enumerate(to_do_list, start =1 ):
                print(f"{i}. {task}")
        else:
            print("Your To-Do List is empty!")

    elif choice =="3":
        if to_do_list:
            print("\nWhich task would you like to remove?")
            for i, task in enumerate(to_do_list, start =1):
                print(f"{i}. {task}")
            try:
                task_num = int(input("Enter the number of the task to remove: "))
                if 1 <= task_num  <= len(to_do_list):
                    removed_task = to_do_list.pop(task_num -1)
                else:
                    print("Invalid task number!")
            except ValueError:
                print("Please enter a valid number!")
        else:
            print("Your To_Do List is empty, nothing to remove!")
                
    elif choice == "4":
        print("Goodbye!")
        break

    else: 
        print("Invalid choice! Please select a valid option.")
