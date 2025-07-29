# gemini_ai.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not set in .env")

genai.configure(api_key=API_KEY)

# Use Gemini Pro
model = genai.GenerativeModel("gemini-1.5-pro-latest")


def get_ai_explanation(bug_summary: str) -> str:
    try:
        # --- PROMPT MODIFIED FOR STRICT, COMPACT, LIST-ONLY OUTPUT ---
        prompt = f"""
        You are an automated code analysis engine. Your sole function is to output a markdown bulleted list.
        Analyze the following code issues. For each issue, provide a main bullet point with the issue's title. Underneath, use sub-bullets to explain the issue and provide a suggested fix.

        **CRITICAL: Follow these formatting rules exactly:**
        1. Your entire response must be a single, compact markdown bulleted list.
        2. Start the response directly with the first bullet point. Do not use any introductory text.
        3. Do not include any blank lines between bullet points or sub-bullet points.
        4. Do not include any concluding summary, commentary, or conversational text after the list.

        **Issues to analyze:**
        {bug_summary}
        """

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return f"AI explanation failed: {str(e)}"