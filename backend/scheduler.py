import json
from apscheduler.schedulers.background import BackgroundScheduler
from sqlmodel import Session, select
from database import engine
from models import Deck, Claim, Question
from deck_processing import extract_text_from_pdf
from llm_service import summarize_deck, extract_claims, assess_claim, generate_questions

scheduler = BackgroundScheduler()

def process_new_decks():
    # print("Running process_new_decks job...")
    with Session(engine) as session:
        statement = select(Deck).where(Deck.processed == False)
        decks = session.exec(statement).all()
        
        for deck in decks:
            print(f"Processing deck {deck.id}...")
            try:
                # 1. Extract text
                if not deck.raw_text:
                    text = extract_text_from_pdf(deck.file_path)
                    deck.raw_text = text
                    session.add(deck)
                    session.commit()
                    session.refresh(deck)
                
                if not deck.raw_text:
                    print(f"Could not extract text for deck {deck.id}")
                    continue

                # 2. Summarize
                summary = summarize_deck(deck.raw_text)
                deck.summary_json = json.dumps(summary)
                session.add(deck)
                session.commit()
                
                # 3. Extract Claims
                claims_data = extract_claims(summary)
                claims_objs = []
                for c in claims_data:
                    claim = Claim(
                        deck_id=deck.id,
                        text=c.get("text", ""),
                        category=c.get("category", "other")
                    )
                    # 4. Assess Claim
                    score, notes = assess_claim(claim.text, summary)
                    claim.plausibility_score = score
                    claim.notes = notes
                    claims_objs.append(claim)
                    session.add(claim)
                
                session.commit()
                
                # 5. Generate Questions
                # Re-query claims to get IDs if needed, but here we just need text/category for context
                # We can pass the dicts we already have
                questions_data = generate_questions(claims_data, summary)
                for q in questions_data:
                    question = Question(
                        deck_id=deck.id,
                        text=q.get("text", ""),
                        category=q.get("category", "other")
                    )
                    session.add(question)
                
                deck.processed = True
                session.add(deck)
                session.commit()
                print(f"Finished processing deck {deck.id}")

            except Exception as e:
                print(f"Error processing deck {deck.id}: {e}")
                session.rollback()

def start_scheduler():
    scheduler.add_job(process_new_decks, 'interval', minutes=1) # Run every minute for faster feedback in dev
    scheduler.start()
