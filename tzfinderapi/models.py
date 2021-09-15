from typing import Optional

from pydantic import BaseModel


class Coordinates(BaseModel):
    lat: float
    lng: float


class Timezone(BaseModel):
    timezone_id: Optional[str]
