from flask import Flask, request, render_template
import requests
from pdfminer.high_level import extract_text
from io import BytesIO
app = Flask(__name__)

# Groq API endpoint (Replace with actual Groq API endpoint and key)
GROQ_API_URL = "https://api.groq.com/parse_resume"
GROQ_API_KEY = "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"
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'resume' not in request.files:
            return "No file part"

        file = request.files['resume']
        if file.filename == '':
            return "No selected file"

        if file and file.filename.endswith('.pdf'):
            # Convert the FileStorage object to a BytesIO object
            pdf_file = BytesIO(file.read())

            # Extract text from the PDF
            pdf_text = extract_text(pdf_file)

            # Prepare the request to Groq API
            headers = {'Authorization': f'Bearer {GROQ_API_KEY}'}
            response = requests.post(GROQ_API_URL, headers=headers, data={'text': pdf_text})

            if response.status_code == 200:
                data = response.json()
                # Extract relevant details
                name = data.get('name', 'Not found')
                phone = data.get('phone', 'Not found')
                email = data.get('email', 'Not found')
                experience = data.get('experience', 'Not found')

                return render_template('index.html', name=name, phone=phone, email=email, experience=experience)

            else:
                return "Error from Groq API"
        else:
            return "Invalid file format. Please upload a PDF file."

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

        
               
            
    