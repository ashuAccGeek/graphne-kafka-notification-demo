import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import ONESIGNAL_APP_ID and ONESIGNAL_REST_API_KEY from core.settings
from core.settings import ONESIGNAL_APP_ID, ONESIGNAL_REST_API_KEY
from onesignal_sdk.client import Client
from onesignal_sdk.error import OneSignalHTTPError
 

onesignal_client = Client(app_id=ONESIGNAL_APP_ID, rest_api_key=ONESIGNAL_REST_API_KEY)


def send_notification_onsignal(notification) :
    try:
        response = onesignal_client.send_notification(notification)
        print(response)
        print("Push notification sent successfully:", response)
    except OneSignalHTTPError as e:
            print("Failed to send push notification:", e)