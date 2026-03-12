import redis
import json

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

SESSION_TTL = 3600


def save_session(patient_id, data):
    """
    Save session data for a patient
    """
    key = f"session:{patient_id}"

    redis_client.setex(
        key,
        SESSION_TTL,
        json.dumps(data)
    )


def get_session(patient_id):
    """
    Retrieve session data
    """

    key = f"session:{patient_id}"

    data = redis_client.get(key)

    if data:
        return json.loads(data)

    return None