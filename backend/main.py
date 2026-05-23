from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader
from agents import supervisor_agent
from graph import app_graph
from fastapi import FastAPI
import os

load_dotenv()

app = FastAPI()
stored_resume_text = ""

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

@app.get("/")
def home():
    return {"message": "AI Career Copilot Backend Running"}

@app.get("/chat")
def chat(message: str):

    message_lower = message.lower()

    # Use resume context only for specific queries
    if (
        "resume" in message_lower
        or "interview" in message_lower
        or "skill" in message_lower
        or "missing" in message_lower
    ):

        enhanced_message = f"""
        User Question:
        {message}

        Resume Context:
        {stored_resume_text}
        """

    else:
        enhanced_message = message

    result = app_graph.invoke({
        "user_input": enhanced_message
    })

    return {
        "response": result["response"]
    }
    
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    global stored_resume_text

    with open(file.filename, "wb") as f:
        f.write(await file.read())

    reader = PdfReader(file.filename)

    resume_text = ""

    for page in reader.pages:
        resume_text += page.extract_text()

    stored_resume_text = resume_text

    prompt = f"""
    Analyze this resume.

    Give:
    1. Candidate strengths
    2. Missing skills
    3. Career suggestions
    4. ATS score
    5. Improvement suggestions

    Resume:
    {resume_text}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    analysis = response.choices[0].message.content

    return {
        "analysis": analysis
    }