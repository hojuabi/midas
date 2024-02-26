from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)


UPLOAD_FOLDER = 'uploads'  # Folder to store uploaded files
ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Function to process PDF files and generate Excel output
def process_pdfs(pdf_files):
    pass
    # Your PDF processing logic here
    # This function would take a list of PDF files and generate an Excel file as output
    # You can implement this logic using Python libraries like PyPDF2 and pandas

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        pdf_files = request.files.getlist('pdf_files')
        excel_file = process_pdfs(pdf_files)
        return send_file(excel_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
