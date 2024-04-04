import time, os
import datetime as dt
import random_select

streak = False
reward_action = 0.43
reward_perfect_day = 1.5
reward_streak = 0.1
star = "🌟"


def invalid_selection():
    print("\nInvalid selection")
    time.sleep(1)
    os.system("cls")


def check_perfect(save_data):
    for item in save_data[2:-3]:
        if item[-1] == "x":
            return False, save_data
    save_data[0] += reward_perfect_day
    return True, save_data


def checkoff(i, save_data):
    # Needs to select the i+1th element of save_data since the first two
    # elements aren't actually included in the to-do list.
    if save_data[i + 1][-1] == "+":
        print("Selected item has already checked off for today.")
        time.sleep(1)
        os.system("cls")
    else:
        save_data[i + 1] = save_data[i + 1][:-1] + "+"
        save_data[0] += reward_action
        print(f"Action {i} complete. Adding ${reward_action} to balance.")
        time.sleep(1)
        perfect, save_data = check_perfect(save_data)
        if perfect:
            print(f"Perfect checklist detected. Awarding additional ${reward_perfect_day} on top of action reward.")
            time.sleep(3)
        return save_data


def reset_list(save_data):
    save_data[0] += save_data[1] * reward_streak
    for i in range(2, len(save_data)):
        save_data[i] = save_data[i][:-1] + "x"
    return save_data


def info():
    os.system("cls")
    print("This program is a to-do list application that can help you stay motivated to do basic everyday things.\n"
          "The user is motivated with a point system. As you complete tasks, points are awarded to a running balance\n"
          "and if the user wishes, can treat themselves accordingly to how many points they receive. By default,\n"
          "I am using this program with money, where my balance is how much money I will allow myself to spend\n"
          "on anything I want.\n\nSpecifications: Each task you complete will give you a set amount of points.\n"
          "If you complete all tasks for the day, you will be rewarded with additional points. Specifications are\n"
          "down below.")
    print(f"\nTask completion reward: {reward_action}\nPerfect day reward: {reward_perfect_day}\nStreak reward ("
          f"per day): {reward_streak}")
    l = input("\nPress enter to go back")


def setup_data():
    # Extract data from data.txt into list
    with open("data.txt", "r") as f:
        save_data = f.readlines()

    # Clean so no empty lines and extra spaces on lines exist
    for i in range(len(save_data)):
        save_data[i] = save_data[i].strip()
    save_data = [x for x in save_data if x != ""]

    # Clean balance and streak data segments and extract date value into the date class.
    save_data[0] = float(save_data[0][9::])
    save_data[1] = int(save_data[1][8::])
    date = save_data[2].split(" ")[1]
    date = dt.datetime.strptime(date, "%Y-%m-%d").date()
    today = dt.date.today()

    # Get rid of unnecessary lines
    for i in range(3):
        save_data.pop(2)

    # Check if it's a new day, if so reset list and adjust streak as needed
    if today > date:
        save_data = reset_list(save_data)
        if today - date == dt.timedelta(1):
            save_data[1] += 1
        else:
            save_data[1] = 0

    return save_data


def done(save_data):
    os.system("cls")
    day = dt.date.today().__str__()
    with open("data.txt", "w") as f:
        f.write(f"Balance: {save_data[0]}\n")
        f.write(f"Streak: {save_data[1]}\n")
        f.write(f"Date: {day}\n\n")
        f.write("List of things to do\n-------------------")
        for i in range(2, len(save_data) - 4):
            f.write("\n" + save_data[i])

    print("Goodbye!")
    time.sleep(3)


def main():
    save_data = setup_data()
    save_data.extend(["Random Idea Selector", "Spend points", "Help/Info", "Quit"])

    # Purely cosmetic loop.
    load = "Loading save data"
    for i in range(4):
        print(load)
        load += "."
        time.sleep(1)
        os.system("cls")

    finished = False
    # Beginning of the real program
    while not finished:
        # Get rid of annoying 13.5500000000000000000003 floats
        save_data[0] = round(save_data[0], 2)

        os.system("cls")
        print("Welcome to the daily checklist program!")
        print("\nThis program will automatically manage your daily checklist and "
              "provide\nthe correct reward for you as you go!\nEnter the number of the item you'd like to check off/"
              "select.\n")
        print(f"Current balance: ${save_data[0]}\nStreak: {save_data[1] * star}\n")
        i = 0
        for item in save_data[2::]:
            i += 1
            print(f"{i}: {item}")
        print()

        inp = 0
        try:
            inp = int(input("Selection: "))
        except ValueError:
            invalid_selection()
            continue

        if inp > i or inp < 1:
            invalid_selection()
        elif inp == i:
            done(save_data)
            finished = True
        elif inp == i - 1:
            info()
        elif inp == i - 2:
            try:
                spend = float(input("How many points would you like to spend?: "))
                if spend <= save_data[0]:
                    save_data[0] -= spend
                    print(f"Spending {spend} points. New balance: {save_data[0]}")
                else:
                    print("Invalid selection: you can't spend that many points.")
            except ValueError:
                print("Invalid selection: you need to input an integer or float.")
            time.sleep(2)
        elif inp == i - 3:
            os.system("cls")
            choice = input("You are selecting an option where the program will select a random thing that you must do "
                           "tomorrow (or today).\n\nYou can change the list of possible choices in want-to-do.txt.\n\n"
                           "Do you wish to continue? (y/n): ")
            if choice.lower() == "y":
                random_select.main()
        else:
            checkoff(inp, save_data)


if __name__ == "__main__":
    if not os.path.exists("data.txt"):
        # Create new data.txt file
        pass
    main()
