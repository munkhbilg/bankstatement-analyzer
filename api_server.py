from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
from main import BankStatementAnalyzer

app = FastAPI(title="Bank Statement Analyzer API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = BankStatementAnalyzer()

@app.post("/analyze-statement")
async def analyze_statement(file: UploadFile = File(...)):
    """API endpoint to analyze bank statements"""
    
    if not file.filename.lower().endswith(('.pdf', '.png', '.jpg', '.jpeg')):
        raise HTTPException(400, "Only PDF and image files are supported")
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_path = tmp_file.name
    
    try:
        # Process the statement
        result = analyzer.process_statement(tmp_path)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(500, f"Processing failed: {str(e)}")
    finally:
        # Clean up temporary file
        os.unlink(tmp_path)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Bank Statement Analyzer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)