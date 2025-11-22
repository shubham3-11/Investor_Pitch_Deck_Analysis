from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Startup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    website: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    decks: List["Deck"] = Relationship(back_populates="startup")

class Deck(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    startup_id: int = Field(foreign_key="startup.id")
    file_path: str
    raw_text: Optional[str] = None
    summary_json: Optional[str] = None
    processed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)

    startup: Optional[Startup] = Relationship(back_populates="decks")
    claims: List["Claim"] = Relationship(back_populates="deck")
    questions: List["Question"] = Relationship(back_populates="deck")

class Claim(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    deck_id: int = Field(foreign_key="deck.id")
    text: str
    category: str
    plausibility_score: Optional[float] = None
    notes: Optional[str] = None

    deck: Optional[Deck] = Relationship(back_populates="claims")

class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    deck_id: int = Field(foreign_key="deck.id")
    text: str
    category: str

    deck: Optional[Deck] = Relationship(back_populates="questions")
