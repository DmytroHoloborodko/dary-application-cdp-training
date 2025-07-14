from datetime import datetime
import uuid

def generate_post_id():
    return str(uuid.uuid4())

def now_utc():
    return datetime.now().isoformat()
