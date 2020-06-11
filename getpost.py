from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime

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


def warmup(value):
    message = "Here is your warmup.\n\n" + \
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
        message = \
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
        message = \
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

    user = list(names.keys())[list(names.values()).index(phone_number)]

    resp = MessagingResponse()

    if body is not None and body != '"':
        if body == 'Warmup' or body == 'warmup' or body == 'Warmup ' or body == 'warmup ':
            if weekday == "Sunday":
                resp.message("Silly goose, it's a Sunday. You don't have a warmup. Or a workout.")
            elif weekday == "Monday" or weekday == "Friday":
                resp.message(warmup(bench))
            elif weekday == "Tuesday" or weekday == "Saturday":
                resp.message(warmup(deadlift))
            elif weekday == "Wednesday":
                resp.message(warmup(press))
            elif weekday == "Thursday":
                resp.message(warmup(squat))
        elif body == 'Workout' or body == 'workout' or body == 'Workout ' or body == 'workout ':
            if weekday == "Sunday":
                message = "Dude, it's a Sunday. You don't have a workout. Go watch anime or something."
                resp.message(message)
            elif weekday == "Monday" or workout == "Saturday":
                workout(weekday, resp)
            else:
                five_three_one(weekday, resp)
        elif has_numbers(body) and ("reps" in body or "Reps" in body or "rep" in body or "Rep" in body):
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
        elif body == 'maxes' or body == 'Maxes' or body == 'maxes ' or body == 'Maxes ':
            og_squat = int(lines[7].rstrip())
            og_bench = int(lines[8].rstrip())
            og_deadlift = int(lines[9].rstrip())
            og_press = int(lines[10].rstrip())
            message = "These are your current maxes.\n\n" + \
                "Squat: " + str(og_squat) + " -> " + str(squat) + " (A " + str(get_change(og_squat, squat)) + "% increase!)\n" + \
                "Bench: " + str(og_bench) + " -> " + str(bench) + " (A " + str(get_change(og_bench, bench)) + "% increase!)\n" + \
                "Deadlift: " + str(og_deadlift) + " -> " + str(deadlift) + " (A " + str(get_change(og_deadlift, deadlift)) + "% increase!)\n" + \
                "Press: " + str(og_press) + " -> " + str(press) + " (A " + str(get_change(og_press, press)) + "% increase!)"
            resp.message(message)
        elif body == 'Undo' or body == 'undo' or body == 'Undo ' or body == 'undo ':
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
        elif "deload" in body or "Deload" or "deload " or "Deload " in body:
            if not has_numbers(body):
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
        elif "hello " or "Hello " or "hello" or "Hello" in body:
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
