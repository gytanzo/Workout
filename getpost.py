from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
import re

app = Flask(__name__)


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
    message = "Here is your warmup.\n\n"
    if weekday == "Monday" or weekday == "Friday":
        message += "BENCH PRESS\n"
    elif weekday == "Tuesday" or weekday == "Saturday":
        message += "DEADLIFT\n"
    elif weekday == "Wednesday":
        message += "OVERHEAD PRESS\n"
    elif weekday == "Thursday":
        message += "SQUAT\n"
    message += convert(value, 40, 5) + "\n" + \
               convert(value, 50, 5) + "\n" + \
               convert(value, 60, 5) + "\n"  # Is this "over-indented? Maybe. Does it look better this way? YES.
    return message


def five_three_one(weekday, lifts, resp):
    squat = lifts[0]
    bench = lifts[1]
    deadlift = lifts[2]
    press = lifts[3]
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


def workout(old_message, weekday, lifts, resp):
    squat = lifts[0]
    bench = lifts[1]
    deadlift = lifts[2]
    press = lifts[3]
    message = old_message
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


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def setup_file(name):
    file = name + "\n" + \
           "\n" + \
           "Squat" + "\n" + \
           "Bench" + "\n" + \
           "Deadlift" + "\n" + \
           "Press" + "\n" + \
           "\n" + \
           "Squat" + "\n" + \
           "Bench" + "\n" + \
           "Deadlift" + "\n" + \
           "Press" + "\n"
    return file


@app.route('/', methods=['GET', 'POST'])
def incoming_sms():
    resp = MessagingResponse()

    weekday = datetime.today().strftime('%A')

    body = request.values.get('Body', None)
    phone_number = request.values.get('From', None)
    phone_number = phone_number[1:]  # removes the addition symbol that messes w/ regex
    user = ""

    with open("Names.txt") as f:
        names = f.readlines()

    for name in names:
        if name.__contains__(phone_number):
            split_user = name.split(",", 1)
            user = split_user[0]
            resp.message(user)

    if body is not None and body != '"':
        if user == "":  # User not found.
            if re.search('initial', body, re.IGNORECASE) is not None:
                if re.search('name', body, re.IGNORECASE) is not None:  # They received the welcome message.
                    name = re.sub("initial", '', body, flags=re.IGNORECASE)  # Remove the "initial" part of the string.
                    name = re.sub("name", '', name, flags=re.IGNORECASE)  # Remove the "name" part of the string."
                    name = "".join(name.split())  # Remove all whitespaces from string. String should JUST be name now.

                    with open("Names.txt", "a+") as f:
                        new_user = name + ", +" + phone_number + "\n"
                        f.write(new_user)

                    with open(name + ".txt", "w+") as f:
                        value_lines = setup_file(name)
                        f.write(value_lines)

                    with open(name + "_Backup.txt", "w+") as f:
                        f.write(value_lines)

                    message = "Welcome, " + name + "! Let's get you set up. In four separate texts, reply to this" + \
                              "message with your four main lifts: squat, bench, deadlift, and overhead press. " + \
                              "The numbers should be prefaced with \"initial lift (lift name)\". Additionally, the numbers " + \
                              "should be 90% of your 1RMs. For example, if your 1RM for squats is 200 lb," + \
                              "the squat text as an example would be \"initial lift squat 180\"."
                    resp.message(message)
                else:
                    message = "You aren't using the initial command correctly. Respond with \"initial name\" followed" + \
                              "by your name to get started. For example, I would respond with \"initial name Ben\"."
                    resp.message(message)
            #else:
                #message = "You do not seem to be registered yet. To register, reply to this text with " + \
                          #"\"initial name\" followed by your name."
                #resp.message(message)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
