"""
A zero‑dependency FastAPI micro‑service that:
1. accepts POST /ask  {username, question}
2. limits each user to DAILY_LIMIT requests per UTC day
3. calls OpenAI via LangChain to answer geography questions
Everything is stored in RAM; restart = fresh state.
"""

import os
import logging
from datetime import datetime, timezone
from collections import defaultdict
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your React Native app origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# ---------- simple in‑memory "database" ----------
DAILY_LIMIT = 10                # tweak as you like
usage_log = defaultdict(list)   # {username: [datetime, ...]}

# ---------- LangChain setup ----------
SYSTEM_TEMPLATE = """
You are a geography expert. You only answer questions strictly about geography.

If the question is unrelated to geography, reply with:
"I'm only able to answer geography-related questions."

Question: {question}
"""

prompt = PromptTemplate.from_template(SYSTEM_TEMPLATE)
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY,model="gpt-4o-mini", temperature=0.5)     # pick any model you have access to
# qa_chain = LLMChain(llm=llm, prompt=prompt)
chain = prompt | llm

# ---------- FastAPI ----------
app = FastAPI()

class AskRequest(BaseModel):
    # username: str
    userId: str
    question: str

@app.get("/")
def root():
    return {"message": "FastAPI backend is running. Use POST /api/main"}

@app.post("/api/main")
def ask(req: AskRequest):
    now = datetime.now(timezone.utc)
    today = now.date()

    # Keep only today’s usage
    usage_log[req.userId] = [
        ts for ts in usage_log[req.userId] if ts.date() == today
    ]

    logging.info(f"User {req.userId} asked: {req.question}")

    if len(usage_log[req.userId]) >= DAILY_LIMIT:
        raise HTTPException(status_code=429, detail="Daily free limit reached")

    # -- Call the chain --
    try:
        response = chain.invoke({"question": req.question})
        answer_text = response.content
    except Exception as e:
        logging.error(f"Error from LangChain/OpenAI for {req.userId}: {str(e)}")
        raise HTTPException(status_code=500, detail="AI service error.")

    # ✅ Record usage BEFORE returning
    usage_log[req.userId].append(now)

    return {
        "answer": answer_text,
        "remaining": DAILY_LIMIT - len(usage_log[req.userId])
    }
