from datetime import datetime as dt
from pydantic import BaseModel


class OutlookMessage(BaseModel):
    message_idx: int
    subject: str
    html_body: str
    sender: str
    received_time: dt
