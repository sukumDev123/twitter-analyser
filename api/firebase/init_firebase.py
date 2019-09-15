import firebase_admin
from firebase_admin import credentials

# Fetch the service account key JSON file contents


# Initialize the app with a service account, granting admin privileges
def initFireBase():
    cred = credentials.Certificate(
        "private/predictpersonal-firebase-adminsdk-3wqs5-594652fe50.json")
    firebase_admin.initialize_app(
        cred, {"databaseURL": "https://predictpersonal.firebaseio.com/"})
