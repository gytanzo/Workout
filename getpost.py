from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
import re

app = Flask(__name__)

name = "Ben"
names = {"Ben": "+15853974321"}

file = open(name + ".txt", 'r')
lines = file.readlines()
squat = int(lines[2].rstrip())
bench = int(lines[3].rstrip())
deadlift = int(lines[4].rstrip())
press = int(lines[5].rstrip())
file.close()


def convert(x, percentage, reps, base=5):
    decimal_percent = percentage * .01
    val = x * decimal_percent
    rounded = str(base * round(val / base))
    return rounded + " x" + str(reps)


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


def get_change(current, previous):
    if current == previous:
        return 0
    try:
        return round((abs(current - previous) / previous) * 100.0, 2)
    except ZeroDivisionError:
        return float('inf')


def warmup(value, weekday):
    message = ""
    if weekday == "Monday" or weekday == "Friday":
        message = "Today is a bench press day."
    elif weekday == "Tuesday" or weekday == "Saturday":
        message = "Today is a deadlift day."
    elif weekday == "Wednesday":
        message = "Today is an overhead press day."
    elif weekday == "Thursday":
        message = "Today is a squat day."
    message += "Here is your warmup.\n\n" + \
               convert(value, 40, 5) + "\n" + \
               convert(value, 50, 5) + "\n" + \
               convert(value, 60, 5) + "\n"
    return message


def five_three_one(weekday, resp):
    message = "Here is your 5/3/1 split for today.\n\n"
    if weekday == "Tuesday":
        message += \
            convert(deadlift, 75, 5) + "\n" + \
            convert(deadlift, 85, 3) + "\n" + \
            convert(deadlift, 95, 1) + "+\n"
    elif weekday == "Wednesday":
        message += \
            convert(press, 75, 5) + "\n" + \
            convert(press, 85, 3) + "\n" + \
            convert(press, 95, 1) + "+\n"
    elif weekday == "Thursday":
        message += \
            convert(squat, 75, 5) + "\n" + \
            convert(squat, 85, 3) + "\n" + \
            convert(squat, 95, 1) + "+\n"
    elif weekday == "Friday":
        message += \
            convert(bench, 75, 5) + "\n" + \
            convert(bench, 85, 3) + "\n" + \
            convert(bench, 95, 1) + "+\n"
    else:
        message = "You don't have a 5/3/1 split today."
    resp.message(message)


def workout(weekday, resp):
    message = "Here is the remainder of your workout.\n\n"
    if weekday == "Monday":
        message += \
            "BENCH PRESS\n" + \
            convert(bench, 65, 8) + "\n" + \
            convert(bench, 75, 6) + "\n" + \
            convert(bench, 85, 4) + "\n" + \
            convert(bench, 85, 4) + "\n" + \
            convert(bench, 85, 4) + "\n" + \
            convert(bench, 80, 5) + "\n" + \
            convert(bench, 75, 6) + "\n" + \
            convert(bench, 70, 7) + "\n" + \
            convert(bench, 65, 8) + "+\n\n" + \
            "OVERHEAD PRESS\n" + \
            convert(press, 50, 6) + "\n" + \
            convert(press, 60, 5) + "\n" + \
            convert(press, 70, 3) + "\n" + \
            convert(press, 70, 5) + "\n" + \
            convert(press, 70, 7) + "\n" + \
            convert(press, 70, 4) + "\n" + \
            convert(press, 70, 6) + "\n" + \
            convert(press, 70, 8)
    elif weekday == "Tuesday":
        message += \
            "DEADLIFT\n" + \
            convert(deadlift, 90, 3) + "\n" + \
            convert(deadlift, 85, 3) + "\n" + \
            convert(deadlift, 80, 3) + "\n" + \
            convert(deadlift, 75, 3) + "\n" + \
            convert(deadlift, 70, 3) + "\n" + \
            convert(deadlift, 65, 3) + "+\n\n" + \
            "FRONT SQUAT\n" + \
            convert(squat, 35, 5) + "\n" + \
            convert(squat, 45, 5) + "\n" + \
            convert(squat, 55, 3) + "\n" + \
            convert(squat, 55, 5) + "\n" + \
            convert(squat, 55, 7) + "\n" + \
            convert(squat, 55, 4) + "\n" + \
            convert(squat, 55, 6) + "\n" + \
            convert(squat, 55, 8)
    elif weekday == "Wednesday":
        message += \
            "OVERHEAD PRESS\n" + \
            convert(press, 90, 3) + "\n" + \
            convert(press, 85, 3) + "\n" + \
            convert(press, 80, 3) + "\n" + \
            convert(press, 75, 5) + "\n" + \
            convert(press, 70, 5) + "\n" + \
            convert(press, 65, 5) + "+\n\n" + \
            "INCLINE BENCH PRESS\n" + \
            convert(bench, 40, 6) + "\n" + \
            convert(bench, 50, 5) + "\n" + \
            convert(bench, 60, 3) + "\n" + \
            convert(bench, 60, 5) + "\n" + \
            convert(bench, 60, 7) + "\n" + \
            convert(bench, 60, 4) + "\n" + \
            convert(bench, 60, 6) + "\n" + \
            convert(bench, 60, 8)
    elif weekday == "Thursday":
        message += \
            "SQUAT\n" + \
            convert(squat, 90, 3) + "\n" + \
            convert(squat, 85, 3) + "\n" + \
            convert(squat, 80, 3) + "\n" + \
            convert(squat, 75, 5) + "\n" + \
            convert(squat, 70, 5) + "\n" + \
            convert(squat, 65, 5) + "+\n\n" + \
            "SUMO DEADLIFT\n" + \
            convert(deadlift, 50, 5) + "\n" + \
            convert(deadlift, 60, 5) + "\n" + \
            convert(deadlift, 70, 3) + "\n" + \
            convert(deadlift, 70, 5) + "\n" + \
            convert(deadlift, 70, 7) + "\n" + \
            convert(deadlift, 70, 4) + "\n" + \
            convert(deadlift, 70, 6) + "\n" + \
            convert(deadlift, 70, 8)
    elif weekday == "Friday":
        message += \
            "BENCH PRESS\n" + \
            convert(bench, 90, 3) + "\n" + \
            convert(bench, 85, 5) + "\n" + \
            convert(bench, 80, 3) + "\n" + \
            convert(bench, 75, 5) + "\n" + \
            convert(bench, 70, 3) + "\n" + \
            convert(bench, 65, 5) + "+\n\n" + \
            "CLOSE GRIP BENCH PRESS\n" + \
            convert(bench, 40, 6) + "\n" + \
            convert(bench, 50, 5) + "\n" + \
            convert(bench, 60, 3) + "\n" + \
            convert(bench, 60, 5) + "\n" + \
            convert(bench, 60, 7) + "\n" + \
            convert(bench, 60, 4) + "\n" + \
            convert(bench, 60, 6) + "\n" + \
            convert(bench, 60, 8)
    elif weekday == "Saturday":
        message += \
            "DEADLIFT\n" + \
            convert(deadlift, 72.5, 3) + "\n" + \
            convert(deadlift, 72.5, 3) + "\n" + \
            convert(deadlift, 72.5, 3) + "\n" + \
            convert(deadlift, 72.5, 3) + "\n" + \
            convert(deadlift, 72.5, 3) + "\n" + \
            convert(deadlift, 72.5, 3) + "\n" + \
            convert(deadlift, 72.5, 3) + "\n" + \
            convert(deadlift, 72.5, 3) + "\n\n" + \
            "FRONT SQUAT\n" + \
            convert(squat, 56.25, 3) + "\n" + \
            convert(squat, 56.25, 3) + "\n" + \
            convert(squat, 56.25, 3) + "\n" + \
            convert(squat, 56.25, 3) + "\n" + \
            convert(squat, 56.25, 3) + "\n" + \
            convert(squat, 56.25, 3)
    resp.message(message)


@app.route('/', methods=['GET', 'POST'])
def incoming_sms():
    weekday = datetime.today().strftime('%A')

    body = request.values.get('Body', None)
    phone_number = request.values.get('From', None)
    user = ""

    for username, number in names.items():
        if number == phone_number:
            user = username

    resp = MessagingResponse()

    if body is not None and body != '"':
        if user == "":
            if re.search('initial', body, re.IGNORECASE) is not None:
                if re.search('name', body, re.IGNORECASE) is not None:  # They received the welcome message.
                    new_body = re.sub('initial', '', body, re.IGNORECASE)  # Remove the "initial" part of the string.
                    new_body = re.sub('name', '', new_body, re.IGNORECASE)  # Remove the "name" part of the string."
                    new_body = "".join(new_body.split())  # Remove all whitespaces from string. String should JUST be name now.
                    names[new_body] = phone_number  # Register the user.

                    user_value = open(new_body + ".txt", "w+")  # Create a file for the user's values.
                    value_lines = [new_body, ""]
                    user_value.writelines(value_lines)
                    user_value.close()

                    user_value = open(new_body + "_Backup.txt", "w+")  # Repeat the process for their backup.
                    value_lines = [new_body, ""]
                    user_value.writelines(value_lines)
                    user_value.close()

                    message = "Hello, " + new_body + "!"  # Change this later to request starting lifts.
                    resp.message(message)
                else:  # Welcome them!
                    message = "Welcome to my program! I hope this workout tool will be useful in your steroid pump" + \
                              " seeking goals. To begin, let's get your name. Reply to this message with \"initial name\"" + \
                              ", followed by your name."
                    resp.message(message)
            else:
                message = "You do not seem to be registered yet. To learn how to register, text this number \"initial\"."
                resp.message(message)
        else:
            if re.search('initial', body, re.IGNORECASE) is not None:
                message = "This will be filled out later. For now, this confirms that something in my code doesn't" + \
                    " get reset each time someone texts it, otherwise it would never recognize anyone but me."
                # If the above line doesn't work, you will need to figure out a solution using a text file, which
                # wouldn't get overridden each execution. That's an uglier implementation, however, so this method
                # was tried first.
                resp.message(message)
            elif re.search('warmup', body, re.IGNORECASE) is not None:
                if weekday == "Sunday":
                    resp.message("Silly goose, it's a Sunday. You don't have a warmup. Or a workout.")
                elif weekday == "Monday" or weekday == "Friday":
                    resp.message(warmup(bench, weekday))
                elif weekday == "Tuesday" or weekday == "Saturday":
                    resp.message(warmup(deadlift, weekday))
                elif weekday == "Wednesday":
                    resp.message(warmup(press, weekday))
                elif weekday == "Thursday":
                    resp.message(warmup(squat, weekday))
            elif re.search('workout', body, re.IGNORECASE) is not None:
                if weekday == "Sunday":
                    message = "Dude, it's a Sunday. You don't have a workout. Go watch anime or something."
                    resp.message(message)
                elif weekday == "Monday" or weekday == "Saturday":
                    workout(weekday, resp)
                else:
                    five_three_one(weekday, resp)
            elif has_numbers(body) and re.search('rep', body, re.IGNORECASE) is not None:
                backup = open(name + "_Backup.txt", 'w')
                backup.writelines(lines)
                backup.close()
                number = int(''.join(filter(str.isdigit, body)))
                if number <= 1:
                    increase = 0
                elif 2 <= number <= 3:
                    increase = 5
                elif 4 <= number <= 5:
                    increase = 10
                else:
                    increase = 15
                message = "You did " + str(number) + " reps, which results in a " + str(increase) + "lb increase.\n\n"
                if weekday == "Tuesday":
                    message += "Old max: " + str(deadlift) + "\n" + \
                               "New max: " + str(deadlift + increase)
                    lines[4] = str(deadlift + increase) + "\n"
                    resp.message(message)
                    workout(weekday, resp)
                elif weekday == "Wednesday":
                    message += "Old max: " + str(press) + "\n" + \
                               "New max: " + str(press + increase)
                    lines[5] = str(press + increase) + "\n"
                    resp.message(message)
                    workout(weekday, resp)
                elif weekday == "Thursday":
                    message += "Old max: " + str(squat) + "\n" + \
                               "New max: " + str(squat + increase)
                    lines[2] = str(squat + increase) + "\n"
                    resp.message(message)
                    workout(weekday, resp)
                elif weekday == "Friday":
                    message += "Old max: " + str(bench) + "\n" + \
                               "New max: " + str(bench + increase)
                    lines[3] = str(bench + increase) + "\n"
                    resp.message(message)
                    workout(weekday, resp)
                else:
                    message = "You don't have a 5/3/1 split today, so I'm not particularly sure why you are giving me your reps.\n"
                    resp.message(message)
                modified = open(name + ".txt", 'w')
                modified.writelines(lines)
                modified.close()
            elif re.search('maxes', body, re.IGNORECASE) is not None:
                og_squat = int(lines[7].rstrip())
                og_bench = int(lines[8].rstrip())
                og_deadlift = int(lines[9].rstrip())
                og_press = int(lines[10].rstrip())
                message = "These are your current maxes.\n\n" + \
                          "Squat: " + str(og_squat) + " -> " + str(squat) + " (A " + str(
                    get_change(og_squat, squat)) + "% increase!)\n" + \
                          "Bench: " + str(og_bench) + " -> " + str(bench) + " (A " + str(
                    get_change(og_bench, bench)) + "% increase!)\n" + \
                          "Deadlift: " + str(og_deadlift) + " -> " + str(deadlift) + " (A " + str(
                    get_change(og_deadlift, deadlift)) + "% increase!)\n" + \
                          "Press: " + str(og_press) + " -> " + str(press) + " (A " + str(
                    get_change(og_press, press)) + "% increase!)"
                resp.message(message)
            elif re.search('undo', body, re.IGNORECASE) is not None:
                backup = open(name + "_Backup.txt", 'r')
                backup_lines = backup.readlines()
                backup.close()
                if backup_lines == lines:
                    message = "There are no changes to undo."
                else:
                    message = "Undid most recent change."
                    current = open(name + ".txt", 'w')
                    current.writelines(backup_lines)
                    current.close()
                resp.message(message)
            elif re.search('deload', body, re.IGNORECASE) is not None:
                if has_numbers(body) is False:
                    message = "This failed. You seem to have forgotten to provide a number."
                else:
                    backup = open(name + "_Backup.txt", 'w')
                    backup.writelines(lines)
                    backup.close()
                    number = int(''.join(filter(str.isdigit, body)))
                    message = "Successfully lowered Training Max.\n\n"
                    if "squat" in body or "Squat" in body:
                        message += "Old max: " + str(squat) + "\n" + \
                                   "New max: " + str(squat - number)
                        lines[2] = str(squat - number) + "\n"
                    elif "bench" in body or "Bench" in body:
                        message += "Old max: " + str(bench) + "\n" + \
                                   "New max: " + str(bench - number)
                        lines[3] = str(bench - number) + "\n"
                    elif "deadlift" in body or "Deadlift" in body:
                        message += "Old max: " + str(deadlift) + "\n" + \
                                   "New max: " + str(deadlift - number)
                        lines[4] = str(deadlift - number) + "\n"
                    elif "press" in body or "Press" in body or "ohp" in body or "OHP" in body:
                        message += "Old max: " + str(press) + "\n" + \
                                   "New max: " + str(press - number)
                        lines[5] = str(press - number) + "\n"
                    else:
                        message = "This failed. Did you spell the name of the workout incorrectly?"
                modified = open(name + ".txt", 'w')
                modified.writelines(lines)
                modified.close()
                resp.message(message)
            elif re.search('hello', body, re.IGNORECASE) is not None:
                message = "Hello, " + user + "!"
                resp.message(message)
            else:
                message = "You don't seem to be using this correctly. These are the currently available commands.\n\n" + \
                          "deload (# decrease) (workout)\n" + \
                          "maxes\n" + \
                          "(# of reps) reps\n" + \
                          "undo\n" + \
                          "warmup\n" + \
                          "workout"
                resp.message(message)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
