# PitchSniff Backend

This is the FastAPI backend for the Startup Idea Evaluator.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `.\venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

Run the following command from the `pitchsniff` directory:

```bash
.\venv\Scripts\uvicorn api:app --reload
```

The API will be available at `http://localhost:8000`.
API Documentation: `http://localhost:8000/docs`.
