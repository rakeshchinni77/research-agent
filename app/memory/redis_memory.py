import redis
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))


redis_client = None


def get_redis_client():
    """
    Lazily create Redis connection.
    Falls back to localhost if Docker hostname fails.
    """
    global redis_client

    if redis_client:
        return redis_client

    try:
        # Try configured Redis host (Docker setup)
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True
        )

        redis_client.ping()
        return redis_client

    except Exception:
        try:
            # Fallback for local development
            redis_client = redis.Redis(
                host="localhost",
                port=REDIS_PORT,
                db=REDIS_DB,
                decode_responses=True
            )

            redis_client.ping()
            return redis_client

        except Exception:
            raise Exception(
                "Redis connection failed. Ensure Redis server is running."
            )


def save_message(session_id: str, role: str, content: str):
    """
    Save a message in Redis conversation history.
    """

    client = get_redis_client()

    key = f"session:{session_id}:messages"

    message = {
        "role": role,
        "content": content
    }

    client.rpush(key, json.dumps(message))


def get_conversation_history(session_id: str):
    """
    Retrieve conversation history for a session.
    """

    client = get_redis_client()

    key = f"session:{session_id}:messages"

    messages = client.lrange(key, 0, -1)

    return [json.loads(msg) for msg in messages]


def clear_session(session_id: str):
    """
    Clear conversation history for a session.
    """

    client = get_redis_client()

    key = f"session:{session_id}:messages"

    client.delete(key)