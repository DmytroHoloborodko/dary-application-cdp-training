import uuid
from datetime import datetime


def generate_post_id():
    return str(uuid.uuid4())


def now_utc():
    return datetime.now().isoformat()
