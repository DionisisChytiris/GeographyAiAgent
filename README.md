# AiAgentWorldTrivia

A zero-dependency FastAPI microservice that:
- Accepts POST requests to `/api/main` with `{userId, question}`
- Limits each user to a daily quota of requests (default: 10 per UTC day)
- Calls OpenAI via LangChain to answer geography questions
- Keeps all state in RAM (restart = fresh state)

## Features

- **Geography Expert:** Only answers geography-related questions.
- **Daily Rate Limiting:** Each user (by userId + IP) is limited to 10 questions per day.
- **OpenAI Integration:** Uses LangChain and OpenAI's GPT models for answers.
- **CORS Enabled:** Ready for frontend integration (e.g., React Native).

## API

### POST `/api/main`

**Request Body:**
```json
{
  "userId": "string",
  "question": "string"
}
```

**Response:**
```json
{
  "answer": "string",
  "remaining": 7
}
```

- `remaining`: Number of questions left for the user today.

### Example

```bash
curl -X POST https://<your-vercel-url>/api/main \
  -H "Content-Type: application/json" \
  -d '{"userId": "alice", "question": "What is the capital of France?"}'
```
-----------------------------------------------------------------------------------------

## Run with Docker
1. Clone the repository:
git clone https://github.com/DionisisChytiris/GeographyAiAgent.git


2. Set your OpenAI API key:
Create a file named .env in the project root:

OPENAI_API_KEY=your-openai-key-here
Note: This file is ignored by Git. Interviewers must add their own key.

3. Build the Docker image:
docker build -t aiagentworldtrivia .

4. Run the container:
docker run --env-file .env -p 8000:8000 aiagentworldtrivia

5. Check on Postman
Post -> http://localhost:8000/api/main
Body 
json
  ## add your own userID and question
 {
   "userId":"1",  
   "question":"Where is the capital of the UK?" 
  }
--------------------------------------------------------------------------------

## Running Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your OpenAI API key:**
   - Create a `.env` file in the `api` folder:
     ```
     OPENAI_API_KEY=your-openai-key
     ```

3. **Start the server:**
   ```bash
   uvicorn api.main:app --reload
   ```

-----------------------------------------------------------------------------------------

## Deployment (Vercel)

- Use the provided `vercel.json` to deploy as a Python serverless function.
- Make sure to add your `OPENAI_API_KEY` as an environment variable in Vercel.

## Notes

- All usage data is stored in RAM; restarting the server resets usage limits.
- Only geography questions are answered. Non-geography questions receive a polite refusal.

---

**Made with FastAPI, LangChain, and OpenAI.**
