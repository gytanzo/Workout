from twilio.rest import Client
from datetime import datetime

# Your Account SID from twilio.com/console
account_sid = "***REMOVED***"
# Your Auth Token from twilio.com/console
auth_token  = "***REMOVED***"

client = Client(account_sid, auth_token)

# weekday = datetime.today().strftime('%A')  # Set the current weekday.
weekday = "Monday"
if weekday == "Sunday":
    test = client.messages.create(
        to="+15853974321",
        from_="+18722595697",
        body="Good evening Ben. This test went well.")
    print(test.sid)
elif weekday == "Monday":
    hello = client.messages.create(
        to="+15853974321",
        from_="+18722595697",
        body="Today's T1 is Bench Press. This is your warmup.")
    print(hello.sid)
    file = open('Message.txt', 'r')
    lines = file.readlines()
    body = ""
    for line in lines:
        body += line
    warmup = client.messages.create(
        to="+15853974321",
        from_="+18722595697",
        body=body)
    print(warmup.sid)


