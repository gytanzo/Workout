from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime

app = Flask(__name__)

weekday = datetime.today().strftime('%A')


def warmup():
    if weekday == "Sunday":
        return "Silly goose, it's a Sunday. You don't have a warmup."
    elif weekday == "Monday":
        message = "Today's T1 is Bench Press. This is your warmup." + "\n" + "\n"
        file = open('Message.txt', 'r')
        lines = file.readlines()
        for line in lines:
            message += line
        return message


@app.route('/', methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body == 'Warmup' or body == 'warmup' or body == 'Warmup ' or body == 'warmup ':
        resp.message(warmup())
    elif body == 'bye':
        resp.message("Goodbye")
    else:
        string = ""
        for character in body:
            if character.isdigit():
                string += character
        resp.message(string)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
