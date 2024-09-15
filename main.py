from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import openai
from openai import OpenAI
import PyPDF2
import io

app = FastAPI()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, can be restricted in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint to receive the OpenAI API key and the PDF
@app.post("/upload")
async def upload_pdf(api_key: str = Form(...), pdf: UploadFile = File(...)):
    try:
        # Read the PDF directly in memory without saving it to disk
        pdf_content = await pdf.read()

        # Use io.BytesIO to treat the bytes as a file for PyPDF2
        pdf_file = io.BytesIO(pdf_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Extract text from the PDF
        pdf_text = ""
        for page_num in range(len(pdf_reader.pages)):
            pdf_text += pdf_reader.pages[page_num].extract_text()

        # Check if any text is extracted from the PDF
        if not pdf_text.strip():
            return {"error": "No text could be extracted from the PDF"}

        # Set the OpenAI API key
        # openai.api_key = api_key

        client = OpenAI(
            api_key=api_key,
        )

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user", 
                    "content": f"You are an expert career coach and resume reviewer. Given a LinkedIn PDF profile as text, generate a structured HTML resume. The PDF text is: {pdf_text}",
                },
            ],
            model="gpt-3.5-turbo-instruct",
        )


        # Check if OpenAI generated a response
        if response and response.choices:
            html_resume = response.choices[0].message['content'].strip()
        else:
            return {"error": "No response from OpenAI"}

        # Return the generated HTML resume
        return HTMLResponse(content=html_resume, status_code=200)

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
