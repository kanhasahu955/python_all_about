import json

from redis import Redis

redis_client = Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

pubsub = redis_client.pubsub()

pubsub.subscribe(
    "resume_events"
)

for message in pubsub.listen():

    if message["type"] == "message":

        payload = json.loads(
            message["data"]
        )

        print(payload)