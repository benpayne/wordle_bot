import os
from twilio.rest import Client
try:
    from account import twilio_SID, twilio_token, twilio_source_phone, twilio_test_phone
    send_text = True
except:
    print("Check README.md for how to setup twilio") 
    send_text = False


def send_message(text):
    if send_text:
        # Find your Account SID and Auth Token at twilio.com/console
        # and set the environment variables. See http://twil.io/secure
        account_sid = twilio_SID
        auth_token = twilio_token
        client = Client(account_sid, auth_token)

        message = client.messages \
                        .create(
                            body=text,
                            from_=twilio_source_phone,
                            to=twilio_test_phone
                        )
        return message.sid
    else:
        print(f"No Text Capabilities: {text}")


def main():
    res = send_message("This is a test")
    print(res)

if __name__ == "__main__":
    #main()
    print(f"{yellow_box}{green_box}{grey_box}{grey_box}{grey_box}")
