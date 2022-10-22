from datetime import datetime

from pydantic import BaseModel


class IEvent(BaseModel):
    creation_time: datetime = datetime.now()
    replication_time: datetime = datetime.now()
