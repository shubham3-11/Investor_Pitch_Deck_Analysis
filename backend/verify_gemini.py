import os
import sys
from llm_service import summarize_deck

print("Checking imports...")
try:
    import google.generativeai as genai
    print("google.generativeai imported successfully.")
except ImportError:
    print("Failed to import google.generativeai")
    sys.exit(1)

print("Checking llm_service...")
if "GEMINI_API_KEY" not in os.environ:
    print("GEMINI_API_KEY not set. Skipping live API test.")
else:
    print("GEMINI_API_KEY found. Attempting summary...")
    try:
        summary = summarize_deck("This is a test pitch deck content.")
        print("Summary result:", summary)
    except Exception as e:
        print(f"Error during summary: {e}")
