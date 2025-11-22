import os
from dotenv import load_dotenv

load_dotenv()
import shutil
from typing import List
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from contextlib import asynccontextmanager

from database import create_db_and_tables, get_session
from models import Startup, Deck, Claim, Question
from scheduler import start_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    start_scheduler()
    os.makedirs("uploads", exist_ok=True)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startups
@app.post("/api/startups", response_model=Startup)
def create_startup(startup: Startup, session: Session = Depends(get_session)):
    session.add(startup)
    session.commit()
    session.refresh(startup)
    return startup

@app.get("/api/startups")
def read_startups(session: Session = Depends(get_session)):
    # Custom response to include counts
    startups = session.exec(select(Startup)).all()
    results = []
    for s in startups:
        deck_count = len(s.decks)
        latest_deck_id = None
        if s.decks:
            # Assuming decks are ordered by id or created_at, but let's sort to be sure or just take last
            latest_deck = sorted(s.decks, key=lambda d: d.created_at, reverse=True)[0]
            latest_deck_id = latest_deck.id
            
        results.append({
            "id": s.id,
            "name": s.name,
            "website": s.website,
            "description": s.description,
            "created_at": s.created_at,
            "number_of_decks": deck_count,
            "latest_deck_id": latest_deck_id
        })
    return results

@app.get("/api/startups/{startup_id}")
def read_startup(startup_id: int, session: Session = Depends(get_session)):
    startup = session.get(Startup, startup_id)
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")
    
    return {
        "id": startup.id,
        "name": startup.name,
        "website": startup.website,
        "description": startup.description,
        "decks": [
            {"id": d.id, "created_at": d.created_at, "processed": d.processed}
            for d in startup.decks
        ]
    }

# Decks
@app.post("/api/decks", response_model=Deck)
def create_deck(startup_id: int, file: UploadFile = File(...), session: Session = Depends(get_session)):
    file_location = f"uploads/{file.filename}"
    # Ensure unique filename if needed, but for now simple overwrite or append timestamp
    # Let's append timestamp to be safe
    import time
    file_location = f"uploads/{int(time.time())}_{file.filename}"
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    deck = Deck(startup_id=startup_id, file_path=file_location)
    session.add(deck)
    session.commit()
    session.refresh(deck)
    return deck

@app.get("/api/decks/{deck_id}")
def read_deck(deck_id: int, session: Session = Depends(get_session)):
    deck = session.get(Deck, deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
        
    import json
    summary = json.loads(deck.summary_json) if deck.summary_json else None
    
    return {
        "id": deck.id,
        "startup_id": deck.startup_id,
        "created_at": deck.created_at,
        "processed": deck.processed,
        "summary": summary,
        "claims": deck.claims,
        "questions": deck.questions
    }
