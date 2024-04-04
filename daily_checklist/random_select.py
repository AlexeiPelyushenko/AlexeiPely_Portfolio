import random
import time
import os
import sys


def setup():
    with open("want-to-do.txt", "w") as f:
        f.write("Write down things you want to do below. Run random-select.py. "
                "That's what you'll do tomorrow.\n----------------------\nExample Activity 1\nExample Activity 2\n"
                "Example Activity 3")
    print("want-to-do.txt set up complete. Sample want-to-do.txt file created/rewritten. \n"
          "Make sure the first two lines aren't deleted or blank. You can change what they say, but the first two lines"
          " in \nwant-to-do.txt will be omitted in the real program as options. Just write a list of entries \n"
          "separated by enters in the .txt file then run this again to choose a random thing to do.")
    time.sleep(25)
    sys.exit(0)


def improper_file_setup():
    print("Error: want-to-do.txt was set up incorrectly. If you want the want-to-do.txt template, delete \n"
          "the current want-to-do.txt and then run this program again.\n")
    response = input("Would you like want-to-do.txt to be overwritten right now? (yes/no):  ")
    if response.lower() == "yes":
        print()
        setup()
    else:
        print("\nThat's fine. Exiting program...")
        time.sleep(2)
        sys.exit(0)


def main():
    print("Beginning random selection. Whatever gets outputted, you'll have to do today or tomorrow. \n"
          "Ctrl-C to go back now. Otherwise...")
    time.sleep(5)
    os.system("cls")
    time.sleep(2)

    options = []
    with open("want-to-do.txt", "r") as f:
        options = f.read()
        options = options.split("\n")
        options = [i for i in options if i.strip() != ""]
        if len(options) < 3:
            improper_file_setup()
        options.pop(0)
        options.pop(0)

    print("\nCalculating thing to do...\n")

    for i in range(10, 0, -1):
        print(i)
        time.sleep(1)
        os.system("cls")
    print(f"ding\n------------------------\nWoohoo! You get to do {options[random.randint(0, len(options) - 1)]}"
          f"!!!\n------------------------")

    print("Quitting in 5 seconds.")
    time.sleep(5)


if __name__ == "__main__":
    # Ensures everything is set up nicely
    if not os.path.exists("want-to-do.txt"):
        print("First time running detected. Creating want-to-do.txt...\n")
        time.sleep(1.5)
        setup()
    main()
