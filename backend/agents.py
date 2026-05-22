from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Resume Agent
def resume_agent(user_input):

    prompt = f"""
    You are a Resume Analysis Expert.

    Analyze this resume or resume-related query:

    {user_input}

    Give:
    - strengths
    - weaknesses
    - ATS suggestions
    - improvement tips
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

    return response.choices[0].message.content


# Career Agent
def career_agent(user_input):

    prompt = f"""
    You are an AI Career Coach.

    Answer this career question:

    {user_input}

    Give:
    - roadmap
    - learning path
    - technologies to learn
    - project ideas
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

    return response.choices[0].message.content


# Interview Agent
def interview_agent(user_input):

    prompt = f"""
    You are a Technical Interview Expert.

    Based on this topic:

    {user_input}

    Generate:
    - interview questions
    - answers
    - coding questions
    - preparation tips
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

    return response.choices[0].message.content


# Skill Gap Agent
def skill_gap_agent(user_input):

    prompt = f"""
    You are a Skill Gap Analysis Expert.

    Analyze this profile:

    {user_input}

    Find:
    - missing skills
    - industry-required skills
    - recommended technologies
    - improvement areas
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

    return response.choices[0].message.content


# Supervisor Agent
def supervisor_agent(user_input):

    user_input_lower = user_input.lower()

    # Resume Related
    if "resume" in user_input_lower or "cv" in user_input_lower:
        return resume_agent(user_input)

    # Interview Related
    elif "interview" in user_input_lower or "question" in user_input_lower:
        return interview_agent(user_input)

    # Skill Gap Related
    elif "skill" in user_input_lower or "missing" in user_input_lower:
        return skill_gap_agent(user_input)

    # Default Career Agent
    else:
        return career_agent(user_input)