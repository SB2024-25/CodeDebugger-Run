# CodeDebugger&Run

A local AI-powered Python code debugger that helps developers understand and fix errors through plain-English explanations, test execution, and static analysis.

Built with FastAPI and Gemini AI, this tool is designed for learning, teaching, and debugging Python code in a private, secure environment.


🚀 Features

- ✅ **Syntax & Runtime Error Detection**  
  Catches `SyntaxError` and exceptions like `ZeroDivisionError`.

- ✅ **Static Code Analysis**  
  Uses Python’s `ast` module to detect logic issues (e.g., redundant conditions).

- ✅ **Linting Support**  
  Integrates `flake8` and `pylint` for style and design feedback.

- ✅ **Test Case Execution**  
  Runs code safely and validates output against expected results.

- ✅ **AI-Powered Explanations**  
  Uses **Perplexity AI** to explain bugs in simple, beginner-friendly language.

- ✅ **REST API Backend**  
  Built with **FastAPI**, includes interactive documentation at `/docs`.

- ✅ **100% Local Development**  
  Runs entirely on your machine — no data leaves your system.

---

🛠️ Tech Stack

- **Backend**: Python 3.12
- **Framework**: FastAPI + Uvicorn
- **AI Integration**: Perplexity AI API (`llama-3-sonar-small-32k-chat`)
- **Analysis Tools**: `ast`, `flake8`, `pylint`
- **Testing**: In-memory execution with `input()` mocking
- **Environment Management**: `.env` file with `python-dotenv`


🔐 Setup

1. **Clone the repository**
   bash
   git clone https://github.com/SB2024-25/CodeDebugger-Run.git
   cd CodeDebugger-Run
   

2. **Install dependencies**
   bash
   pip install -r requirements.txt
   

3. **Set up environment variables**
   bash
   cp .env.example .env
   
   Open `.env` and add your OPENAI API key:
   env
   OPENAPI_API_KEY=your_api_key_here
   

4. **Run the server**
   bash
   uvicorn main:app --reload
   

5. **Open the API interface**
   Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)



 🧪 Example Request

Send a POST to `/debug`:
json
{
  "code": "def divide(a, b):\n    return a / b\nprint(divide(10, 0))",
  "test_cases": [
    { "input": "", "expected": "Error handled" }
  ]
}


You'll receive:
- Detection of `ZeroDivisionError`
- AI-generated explanation in plain English
- Linter and AST analysis (if applicable)



📁 Project Structure

CodeDebugger-Run/
├── main.py               # FastAPI entry point
├── debug_engine.py       # Core debugging logic
├── perplexity_ai.py      # AI explanation via Perplexity
├── test_runner.py        # Test execution with input mocking
├── utils.py              # AST and syntax checks
├── models.py             # Pydantic request/response models
├── .env.example          # Template for environment variables
├── requirements.txt      # Python dependencies
└── README.md             # This file


 🧹 Local-Only Design

This project is built to run **entirely offline**.  
No telemetry, no tracking, no forced cloud integration.

You control your data, your code, and your debugging workflow.


📝 License

This project is open source under the **THEUNILicense**.


✅ This `README.md`:
- Reflects your actual implementation
- Is self-contained and beginner-friendly
- Documents setup, usage, and structure
- Makes **no external promotions**
- Focuses on **your tool, your code, your goals**



