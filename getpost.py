from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime

app = Flask(__name__)

file = open('Current Values.txt', 'r')
lines = file.readlines()
squat = int(lines[0].rstrip())
bench = int(lines[1].rstrip())
deadlift = int(lines[2].rstrip())
press = int(lines[3].rstrip())
file.close()


def my_round(x, base=5):
    return base * round(x / base)


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
    message = "Here is your warmup." + "\n" + "\n"
    message += str(my_round(value * 0.4)) + " x5\n"
    message += str(my_round(value * 0.5)) + " x5\n"
    message += str(my_round(value * 0.6)) + " x5\n"
    return message


def five_three_one(weekday, resp):
    message = "Here is your 5/3/1 split for today.\n\n"
    if weekday == "Tuesday":
        message += \
            str(my_round(deadlift * 0.75)) + " x5\n" + \
            str(my_round(deadlift * 0.85)) + " x3\n" + \
            str(my_round(deadlift * 0.95)) + " x1+\n"
    elif weekday == "Wednesday":
        message += \
            str(my_round(press * 0.75)) + " x5\n" + \
            str(my_round(press * 0.85)) + " x3\n" + \
            str(my_round(press * 0.95)) + " x1+\n"
    elif weekday == "Thursday":
        message += \
            str(my_round(squat * 0.75)) + " x5\n" + \
            str(my_round(squat * 0.85)) + " x3\n" + \
            str(my_round(squat * 0.95)) + " x1+\n"
    elif weekday == "Friday":
        message += \
            str(my_round(bench * 0.75)) + " x5\n" + \
            str(my_round(bench * 0.85)) + " x3\n" + \
            str(my_round(bench * 0.95)) + " x1+\n"
    else:
        message = "You don't have a 5/3/1 split today."
    resp.message(message)


def workout(weekday, resp):
    message = "Here is the remainder of your workout.\n\n"
    if weekday == "Monday":
        message = \
            "BENCH PRESS\n" + \
            str(my_round(bench * 0.65)) + " x8\n" + \
            str(my_round(bench * 0.75)) + " x6\n" + \
            str(my_round(bench * 0.85)) + " x4\n" + \
            str(my_round(bench * 0.85)) + " x4\n" + \
            str(my_round(bench * 0.85)) + " x4\n" + \
            str(my_round(bench * 0.8)) + " x5\n" + \
            str(my_round(bench * 0.75)) + " x6\n" + \
            str(my_round(bench * 0.7)) + " x7\n" + \
            str(my_round(bench * 0.65)) + " x8+\n\n" + \
            "OVERHEAD PRESS\n" + \
            str(my_round(press * 0.5)) + " x6\n" + \
            str(my_round(press * 0.6)) + " x5\n" + \
            str(my_round(press * 0.7)) + " x3\n" + \
            str(my_round(press * 0.7)) + " x5\n" + \
            str(my_round(press * 0.7)) + " x7\n" + \
            str(my_round(press * 0.7)) + " x4\n" + \
            str(my_round(press * 0.7)) + " x6\n" + \
            str(my_round(press * 0.7)) + " x8"
    elif weekday == "Tuesday":
        message += \
            "DEADLIFT\n" + \
            str(my_round(deadlift * 0.9)) + " x3\n" + \
            str(my_round(deadlift * 0.85)) + " x3\n" + \
            str(my_round(deadlift * 0.8)) + " x3\n" + \
            str(my_round(deadlift * 0.75)) + " x3\n" + \
            str(my_round(deadlift * 0.7)) + " x3\n" + \
            str(my_round(deadlift * 0.65)) + " x3+\n\n" + \
            "FRONT SQUAT\n" + \
            str(my_round(squat * 0.35)) + " x5\n" + \
            str(my_round(squat * 0.45)) + " x5\n" + \
            str(my_round(squat * 0.55)) + " x3\n" + \
            str(my_round(squat * 0.55)) + " x5\n" + \
            str(my_round(squat * 0.55)) + " x7\n" + \
            str(my_round(squat * 0.55)) + " x4\n" + \
            str(my_round(squat * 0.55)) + " x6\n" + \
            str(my_round(squat * 0.55)) + " x8"
    elif weekday == "Wednesday":
        message += \
            "OVERHEAD PRESS\n" + \
            str(my_round(press * 0.9)) + " x3\n" + \
            str(my_round(press * 0.85)) + " x3\n" + \
            str(my_round(press * 0.8)) + " x3\n" + \
            str(my_round(press * 0.75)) + " x5\n" + \
            str(my_round(press * 0.7)) + " x5\n" + \
            str(my_round(press * 0.65)) + " x5+\n\n" + \
            "INCLINE BENCH PRESS\n" + \
            str(my_round(bench * 0.4)) + " x6\n" + \
            str(my_round(bench * 0.5)) + " x5\n" + \
            str(my_round(bench * 0.6)) + " x3\n" + \
            str(my_round(bench * 0.6)) + " x5\n" + \
            str(my_round(bench * 0.6)) + " x7\n" + \
            str(my_round(bench * 0.6)) + " x4\n" + \
            str(my_round(bench * 0.6)) + " x6\n" + \
            str(my_round(bench * 0.6)) + " x8"
    elif weekday == "Thursday":
        message += \
            "SQUAT\n" + \
            str(my_round(squat * 0.9)) + " x3\n" + \
            str(my_round(squat * 0.85)) + " x3\n" + \
            str(my_round(squat * 0.8)) + " x3\n" + \
            str(my_round(squat * 0.75)) + " x5\n" + \
            str(my_round(squat * 0.7)) + " x5\n" + \
            str(my_round(squat * 0.65)) + " x5+\n\n" + \
            "SUMO DEADLIFT\n" + \
            str(my_round(deadlift * 0.5)) + " x5\n" + \
            str(my_round(deadlift * 0.6)) + " x5\n" + \
            str(my_round(deadlift * 0.7)) + " x3\n" + \
            str(my_round(deadlift * 0.7)) + " x5\n" + \
            str(my_round(deadlift * 0.7)) + " x7\n" + \
            str(my_round(deadlift * 0.7)) + " x4\n" + \
            str(my_round(deadlift * 0.7)) + " x6\n" + \
            str(my_round(deadlift * 0.7)) + " x8"
    elif weekday == "Friday":
        message += \
            "BENCH PRESS\n" + \
            str(my_round(bench * 0.9)) + " x3\n" + \
            str(my_round(bench * 0.85)) + " x5\n" + \
            str(my_round(bench * 0.8)) + " x3\n" + \
            str(my_round(bench * 0.75)) + " x5\n" + \
            str(my_round(bench * 0.7)) + " x3\n" + \
            str(my_round(bench * 0.65)) + " x5+\n\n" + \
            "CLOSE GRIP BENCH PRESS\n" + \
            str(my_round(bench * 0.4)) + " x6\n" + \
            str(my_round(bench * 0.5)) + " x5\n" + \
            str(my_round(bench * 0.6)) + " x3\n" + \
            str(my_round(bench * 0.6)) + " x5\n" + \
            str(my_round(bench * 0.6)) + " x7\n" + \
            str(my_round(bench * 0.6)) + " x4\n" + \
            str(my_round(bench * 0.6)) + " x6\n" + \
            str(my_round(bench * 0.6)) + " x8"
    elif weekday == "Saturday":
        message = \
            "DEADLIFT\n" + \
            str(my_round(deadlift * 0.725)) + " x3\n" + \
            str(my_round(deadlift * 0.725)) + " x3\n" + \
            str(my_round(deadlift * 0.725)) + " x3\n" + \
            str(my_round(deadlift * 0.725)) + " x3\n" + \
            str(my_round(deadlift * 0.725)) + " x3\n" + \
            str(my_round(deadlift * 0.725)) + " x3\n" + \
            str(my_round(deadlift * 0.725)) + " x3\n" + \
            str(my_round(deadlift * 0.725)) + " x3\n\n" + \
            "FRONT SQUAT\n" + \
            str(my_round(squat * 0.75 * .75)) + " x3\n" + \
            str(my_round(squat * 0.75 * .75)) + " x3\n" + \
            str(my_round(squat * 0.75 * .75)) + " x3\n" + \
            str(my_round(squat * 0.75 * .75)) + " x3\n" + \
            str(my_round(squat * 0.75 * .75)) + " x3\n" + \
            str(my_round(squat * 0.75 * .75)) + " x3"
    resp.message(message)


@app.route('/', methods=['GET', 'POST'])
def incoming_sms():
    weekday = datetime.today().strftime('%A')

    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body is not None and body != '"':
        if body == 'Warmup' or body == 'warmup' or body == 'Warmup ' or body == 'warmup ':
            if weekday == "Sunday":
                resp.message("Silly goose, it's a Sunday. You don't have a warmup. Or a workout.")
            elif weekday == "Monday":
                resp.message(warmup(bench))
            elif weekday == "Tuesday":
                resp.message(warmup(deadlift))
            elif weekday == "Wednesday":
                resp.message(warmup(press))
            elif weekday == "Thursday":
                resp.message(warmup(squat))
            elif weekday == "Friday":
                resp.message(warmup(bench))
            elif weekday == "Saturday":
                resp.message(warmup(deadlift))
        elif body == 'Workout' or body == 'workout' or body == 'Workout ' or body == 'workout ':
            if weekday == "Sunday":
                message = "Dude, it's a Sunday. You don't have a workout. Go back to bed."
                resp.message(message)
            if weekday == "Monday":
                workout(weekday, resp)
            elif weekday == "Saturday":
                workout(weekday, resp)
            else:
                five_three_one(weekday, resp)
        elif has_numbers(body):
            string = ""
            for character in body:
                if character.isdigit():
                    string += character
            number = int(string)
            increase = ""
            if number <= 1:
                increase = 0
            elif 2 <= number <= 3:
                increase = 5
            elif 4 <= number <= 5:
                increase = 10
            elif number > 5:
                increase = 15
            message = "You did " + string + " reps, which results in a " + str(increase) + "lb increase.\n\n"
            if weekday == "Tuesday":
                message += "Old max: " + str(deadlift) + "\n" + \
                           "New max: " + str(deadlift + increase)
                lines[2] = str(deadlift + increase) + "\n"
                resp.message(message)
                workout(weekday, resp)
            elif weekday == "Wednesday":
                message += "Old max: " + str(press) + "\n" + \
                           "New max: " + str(press + increase)
                lines[3] = str(press + increase) + "\n"
                resp.message(message)
                workout(weekday, resp)
            elif weekday == "Thursday":
                message += "Old max: " + str(squat) + "\n" + \
                           "New max: " + str(squat + increase)
                lines[0] = str(squat + increase) + "\n"
                resp.message(message)
                workout(weekday, resp)
            elif weekday == "Friday":
                message += "Old max: " + str(bench) + "\n" + \
                           "New max: " + str(bench + increase)
                lines[1] = str(bench + increase) + "\n"
                resp.message(message)
                workout(weekday, resp)
            modified = open('Current Values.txt', 'w')
            modified.writelines(lines)
            modified.close()
        elif body == 'maxes' or body == 'Maxes' or body == 'maxes ' or body == 'Maxes ':
            og_squat = int(lines[5].rstrip())
            og_bench = int(lines[6].rstrip())
            og_deadlift = int(lines[7].rstrip())
            og_press = int(lines[8].rstrip())
            message = "These are your current maxes.\n\n" + \
                str(og_squat) + " -> " + str(squat) + " (A " + str(get_change(og_squat, squat)) + "% increase!)\n" + \
                str(og_bench) + " -> " + str(bench) + " (A " + str(get_change(og_bench, bench)) + "% increase!)\n" + \
                str(og_deadlift) + " -> " + str(deadlift) + " (A " + str(get_change(og_deadlift, deadlift)) + "% increase!)\n" + \
                str(og_press) + " -> " + str(press) + " (A " + str(get_change(og_press, press)) + "% increase!)"
            resp.message(message)
        else:
            message = "You don't seem to be using this correctly. These are the currently available commands.\n\n" + \
                      "warmup\n" + \
                      "workout\n" + \
                      "(int) reps" + \
                      "maxes"
            resp.message(message)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
