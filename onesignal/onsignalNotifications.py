import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import ONESIGNAL_APP_ID and ONESIGNAL_REST_API_KEY from core.settings
from core.settings import ONESIGNAL_APP_ID, ONESIGNAL_REST_API_KEY,TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,TWILIO_PHONE_NUMBER
from onesignal_sdk.client import Client
from onesignal_sdk.error import OneSignalHTTPError

from twilio.rest import Client as TWilioClient
 

onesignal_client = Client(app_id=ONESIGNAL_APP_ID, rest_api_key=ONESIGNAL_REST_API_KEY)


def send_notification_onsignal(notification) :
    try:
        response = onesignal_client.send_notification(notification)
        print(response)
        print("Push notification sent successfully:", response)
    except OneSignalHTTPError as e:
            print("Failed to send push notification:", e)


# twilio_client = TWilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# message = twilio_client.messages.create(
#   from_='+16593335588',
#   to='+918709011213',
#   body="Twilio Order Created"
# )

def send_sms_notification(sms):
    # Parse event_data and extract necessary information
    # user_id, delivery_address, delivery_time, item_ids = parse_message_data(event_data)

    # Initialize Twilio client
    twilio_client = TWilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # Construct SMS message body
    sms_body = f"Your order has been placed successfully! {sms}"

    # Send SMS notification using Twilio
    message = twilio_client.messages.create(
        from_='+16593335588',
        to='+918709011213',
        body=sms_body
    )
    print("SMS notification sent successfully:", message.sid)