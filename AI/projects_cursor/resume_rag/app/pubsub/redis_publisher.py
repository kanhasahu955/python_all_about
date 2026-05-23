import json

from redis import Redis

redis_client = Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

def publish_event(
    channel,
    payload
):

    redis_client.publish(
        channel,
        json.dumps(payload)
    )