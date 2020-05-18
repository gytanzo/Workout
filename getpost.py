from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime

app = Flask(__name__)


def my_round(x, base = 5):
    return base * round(x/base)


def warmup(value):
    message = "Here is your warmup." + "\n" + "\n"
    message += str(my_round(value * 0.4)) + "x5\n"
    message += str(my_round(value * 0.5)) + "x5\n"
    message += str(my_round(value * 0.6)) + "x5\n"
    return message


@app.route('/', methods=['GET', 'POST'])
def incoming_sms():
    weekday = datetime.today().strftime('%A')
    file = open('Current Values.txt', 'r')
    lines = file.readlines()
    squat = int(lines[0].rstrip())
    bench = int(lines[1].rstrip())
    deadlift = int(lines[2].rstrip())
    press = int(lines[3].rstrip())

    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
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
    elif body is not None and body != '"':
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
        message = "You did " + string + " reps, which results in a " + str(increase) + "lb increase. The file has been updated, you may continue with your workout."
        resp.message(message)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
