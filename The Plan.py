def my_round(x, base = 5):
    return base * round(x/base)


def workout():
    weekday = "Monday"
    value_file = open('Current Values.txt', 'r')  # Open the text file storing current maxes for reading.
    message_file = open('Message.txt', 'w')  # Open the file used to store the text.
    lines = value_file.readlines()  # Create a list storing each line.
    if weekday == "Sunday":
        print("You don't have a workout today.")
    elif weekday == "Monday":
        bench = int(lines[1].rstrip())   # rstrip() is used to remove the newline characters.
        press = int(lines[3].rstrip())
        message_file.write(str(my_round(bench * 0.4)) + "x5\n")
        message_file.write(str(my_round(bench * 0.5)) + "x5\n")
        message_file.write(str(my_round(bench * 0.6)) + "x5")

    value_file.close()  # Close max file.
    message_file.close()  # Close message file.


def main():
    workout()


main()
