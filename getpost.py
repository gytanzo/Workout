from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from datetime import datetime

app = Flask(__name__)

# Your Account SID from twilio.com/console
account_sid = "***REMOVED***"
# Your Auth Token from twilio.com/console
auth_token  = "***REMOVED***"

client = Client(account_sid, auth_token)


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
        message = "You did " + string + " reps, which results in a " + str(increase) + "lb increase.\n\n" + "Old max: " + str(bench) + "\n" + "New max: " + str(bench + increase)
        resp.message(message)
    else:
        message = "This is the second massage."
        resp.message(message)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
