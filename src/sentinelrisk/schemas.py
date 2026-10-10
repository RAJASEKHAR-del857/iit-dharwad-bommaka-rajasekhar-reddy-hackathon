from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, Field, field_validator

EventType = Literal[
    "geopolitical", "macroeconomic", "credit_event", "merger_acquisition",
    "product_launch", "regulatory_legal", "earnings_business", "other"
]

class RiskSignal(BaseModel):
    signal_id: str
    source_type: str
    source_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    text: str = Field(min_length=1, max_length=12000)
    entities: list[str] = Field(default_factory=list)
    sentiment_label: Literal["positive", "negative", "neutral"]
    sentiment_score: float = Field(ge=-1.0, le=1.0)
    sentiment_confidence: float = Field(ge=0.0, le=1.0)
    event_type: EventType
    impact_score: int = Field(ge=1, le=10)
    impact_reasons: list[str] = Field(default_factory=list)
    affected_sectors: list[str] = Field(default_factory=list)
    model_used: str
    is_synthetic: bool = True

    @field_validator("text")
    @classmethod
    def non_blank_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text must not be blank")
        return value.strip()
