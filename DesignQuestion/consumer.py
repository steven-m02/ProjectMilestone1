from google.cloud import pubsub_v1   # pip install google-cloud-pubsub  ##to install
import glob  # for searching for json file
import os
import json

#Search the current directory for the JSON file (including the service account key)
#to set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
files = glob.glob("*.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = files[0]

# Set the project_id with your project ID
project_id = "spatial-encoder-448821-q6"
subscription_id = "design-sub"

# create a subscriber to the subscriber for the project using the subscription_id
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

print(f"Listening for messages on {subscription_path}...\n")

# A callback function for handling received messages
def callback(message):

    message_data = json.loads(message.data.decode("utf-8"))
    
     # convert from bytes to string (deserialization)
    print(f"Consumed record: {message_data}")

  # Report To Google Pub/Sub the successful processed of the received messages
    message.ack()

with subscriber:
   # The call back function will be called for each message recieved from the topic 
    # throught the subscription.
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()