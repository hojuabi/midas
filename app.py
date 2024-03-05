from flask import Flask, render_template, request, send_file, render_template_string
import os
import pandas as pd
from midas import *
from io import BytesIO

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'pdf'}
midas = Midas()
ops = pd.DataFrame()
ozet  = pd.DataFrame()
excel_buffer = BytesIO()

@app.route('/')
def welcome():
    return render_template('home.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('files')
    results = []
    filtered_files = [file for file in files if file and allowed_file(file.filename)]
    
    ops, ozet, excel_buffer=midas.calculate_tax_for_files(filtered_files,type='Excel')
    html_table = ozet.to_html(index=True)
    return render_template('result.html', html_table=html_table)
    excel_buffer.seek(0)
    
    return  send_file(
        excel_buffer,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='2023_Vergi_Hesap.xlsx'
    )

@app.route('/download_excel')
def download_excel():
 

    excel_buffer.seek(0)
    # Send Excel file for download
    return  send_file(
        excel_buffer,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='2023_Vergi_Hesap.xlsx'
    )


if __name__ == '__main__':  # Set your upload folder
    app.run(debug=True)