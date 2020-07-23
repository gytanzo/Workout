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


def workout(weekday, lifts, resp):
    squat = lifts[0]
    bench = lifts[1]
    deadlift = lifts[2]
    press = lifts[3]
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


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


@app.route('/', methods=['GET', 'POST'])
def incoming_sms():
    resp = MessagingResponse()

    weekday = datetime.today().strftime('%A')

    body = request.values.get('Body', None)
    phone_number = request.values.get('From', None)
    phone_number = phone_number[1:]  # removes the addition symbol that messes w/ regex
    user = ""

    name_file = open("Names.txt", 'r')
    names = name_file.readlines()
    name_file.close()

    for line in names:
        if re.search(phone_number, line, re.IGNORECASE) is not None:
            line_copy = line
            line_copy = line_copy.replace(phone_number, "")  # Remove the phone number from the string.
            line_copy = line_copy.replace(", +", "")  # Remove remaining characters.
            line_copy = line_copy.replace("\n", "")  # Remove newline. Should JUST be the name now.
            user = line_copy

    if body is not None and body != '"':
        if user == "":
            if re.search('initial', body, re.IGNORECASE) is not None:
                if re.search('name', body, re.IGNORECASE) is not None:  # They received the welcome message.
                    name = re.sub("initial", '', body, flags=re.IGNORECASE)  # Remove the "initial" part of the string.
                    name = re.sub("name", '', name, flags=re.IGNORECASE)  # Remove the "name" part of the string."
                    name = "".join(name.split())  # Remove all whitespaces from string. String should JUST be name now.

                    name_file = open("Names.txt", 'a')
                    new_user = name + ", +" + phone_number + "\n"
                    name_file.write(new_user)
                    name_file.close()

                    user_value = open(name + ".txt", "w+")  # Create a file for the user's values.
                    value_lines = [name + "\n", "" + "\n"]
                    user_value.writelines(value_lines)
                    user_value.close()

                    user_value = open(name + "_Backup.txt", "w+")  # Repeat the process for their backup.
                    value_lines = [name + "\n", "" + "\n"]
                    user_value.writelines(value_lines)
                    user_value.close()

                    message = "Welcome, " + name + "! Let's get you set up. In four separate texts, reply to this" + \
                              "message with your four main lifts: squat, bench, deadlift, and overhead press. " + \
                              "The numbers should be prefaced with \"initial lift (lift name)\". Additionally, the numbers " + \
                              "should be 90% of your 1RMs. For example, if your 1RMs are 200 squat, 120 bench, 300 deadlift" + \
                              ", and 100 overhead, then the squat text as an example would be \"initial lift squat 180\"."
                    resp.message(message)
            else:
                message = "You do not seem to be registered yet. To register, reply to this text with " + \
                          "\"initial name\" followed by your name."
                resp.message(message)
        else:
            file = open(user + ".txt", 'r')
            lines = file.readlines()
            squat = int(lines[2].rstrip())
            bench = int(lines[3].rstrip())
            deadlift = int(lines[4].rstrip())
            press = int(lines[5].rstrip())
            lifts = [squat, bench, deadlift, press]
            file.close()
            
            if re.search('lift', body, re.IGNORECASE) is not None:  # They want to submit initial numbers.
                sent = body.replace("initial lift ", "")  # Remove the "initial" part of the string.

                main = open(user + ".txt", "r+")
                main_lines = main.readlines()
                backup = open(user + "_Backup.txt", "r+")
                backup_lines = backup.readlines()

                if file_len(user + ".txt") >= 11:
                    message = "You already provided your initial lifts."
                    resp.message(message)
                    return str(message)

                if re.search('squat', body, re.IGNORECASE) is not None:  # Inputting squat number.
                    sent = sent.replace("squat ", "")
                    sent = "".join(sent.split())
                    main_lines[2] = sent
                    main_lines[7] = sent
                    backup_lines[2] = sent
                    backup_lines[7] = sent
                elif re.search('bench', body, re.IGNORECASE) is not None:  # Inputting squat number.
                    sent = sent.replace("bench ", "")
                    sent = "".join(sent.split())
                    main_lines[3] = sent
                    main_lines[8] = sent
                    backup_lines[3] = sent
                    backup_lines[8] = sent
                elif re.search('deadlift', body, re.IGNORECASE) is not None:  # Inputting squat number.
                    sent = sent.replace("deadlift ", "")
                    sent = "".join(sent.split())
                    main_lines[4] = sent
                    main_lines[9] = sent
                    backup_lines[4] = sent
                    backup_lines[9] = sent
                elif re.search('overhead', body, re.IGNORECASE) is not None:  # Inputting squat number.
                    sent = sent.replace("overhead ", "")
                    sent = "".join(sent.split())
                    main_lines[5] = sent
                    main_lines[10] = sent
                    backup_lines[5] = sent
                    backup_lines[10] = sent
                main.writelines(main_lines)
                backup.writelines(backup_lines)
                main.close()
                backup.close()
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
                    workout(weekday, lifts, resp)
                else:
                    five_three_one(weekday, lifts, resp)
            elif has_numbers(body) and re.search('rep', body, re.IGNORECASE) is not None:
                backup = open(user + "_Backup.txt", 'w')
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
                    workout(weekday, lifts, resp)
                elif weekday == "Wednesday":
                    message += "Old max: " + str(press) + "\n" + \
                               "New max: " + str(press + increase)
                    lines[5] = str(press + increase) + "\n"
                    resp.message(message)
                    workout(weekday, lifts, resp)
                elif weekday == "Thursday":
                    message += "Old max: " + str(squat) + "\n" + \
                               "New max: " + str(squat + increase)
                    lines[2] = str(squat + increase) + "\n"
                    resp.message(message)
                    workout(weekday, lifts, resp)
                elif weekday == "Friday":
                    message += "Old max: " + str(bench) + "\n" + \
                               "New max: " + str(bench + increase)
                    lines[3] = str(bench + increase) + "\n"
                    resp.message(message)
                    workout(weekday, lifts, resp)
                else:
                    message = "You don't have a 5/3/1 split today, so I'm not particularly sure why you are giving me your reps.\n"
                    resp.message(message)
                modified = open(user + ".txt", 'w')
                modified.writelines(lines)
                modified.close()
            elif re.search('maxes', body, re.IGNORECASE) is not None:
                og_squat = int(lines[7].rstrip())
                og_bench = int(lines[8].rstrip())
                og_deadlift = int(lines[9].rstrip())
                og_press = int(lines[10].rstrip())
                message = "These are your current maxes.\n\n" + \
                          "Squat: " + str(og_squat) + " -> " + str(squat) + " (A " + \
                          str(get_change(og_squat, squat)) + "% increase!)\n" + \
                          "Bench: " + str(og_bench) + " -> " + str(bench) + " (A " + \
                          str(get_change(og_bench, bench)) + "% increase!)\n" + \
                          "Deadlift: " + str(og_deadlift) + " -> " + str(deadlift) + " (A " + \
                          str(get_change(og_deadlift, deadlift)) + "% increase!)\n" + \
                          "Press: " + str(og_press) + " -> " + str(press) + " (A " + \
                          str(get_change(og_press, press)) + "% increase!)"
                resp.message(message)
            elif re.search('undo', body, re.IGNORECASE) is not None:
                backup = open(user + "_Backup.txt", 'r')
                backup_lines = backup.readlines()
                backup.close()
                if backup_lines == lines:
                    message = "There are no changes to undo."
                else:
                    message = "Undid most recent change."
                    current = open(user + ".txt", 'w')
                    current.writelines(backup_lines)
                    current.close()
                resp.message(message)
            elif re.search('deload', body, re.IGNORECASE) is not None:
                if has_numbers(body) is False:
                    message = "This failed. You seem to have forgotten to provide a number."
                else:
                    backup = open(user + "_Backup.txt", 'w')
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
                modified = open(user + ".txt", 'w')
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
