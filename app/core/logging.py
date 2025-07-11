import json
import time
from typing import List
from app.redis import redis_client
from app.models.log_model import LogEntry

def log_event(api_key: str, log_data: dict):
    r = redis_client.get_client()
    log_key = f"logs:{api_key}"

    log_data["timestamp"] = int(time.time())

    # Push to Redis list
    r.lpush(log_key, json.dumps(log_data))

    # Keep most recent 1000 logs
    r.ltrim(log_key, 0, 999)


def get_latest_logs(api_key: str, limit: int = 50) -> List[LogEntry]:
    r = redis_client.get_client()
    log_key = f"logs:{api_key}"
    
    raw_logs = r.lrange(log_key, 0, limit - 1)
    logs = []

    for raw in raw_logs:
        try:
            log_data = json.loads(raw)
            logs.append(LogEntry(**log_data))
        except Exception:
            continue

    return logs
