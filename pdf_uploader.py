from flask import Flask, request, render_template, send_file
import os

app = Flask(__name__)

# Initialize an empty list to store uploaded PDF filenames
uploaded_files = []

@app.route('/a')
def a():
    return render_template('Test.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    uploaded_file = request.files['pdfFile']

    if uploaded_file.filename != '':
        # Save the uploaded PDF file to the "uploads" folder
        pdf_path = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(pdf_path)

        # Add the filename to the list of uploaded files
        uploaded_files.append(uploaded_file.filename)

        return f'PDF file "{uploaded_file.filename}" uploaded successfully. <a href="/download">View Downloads</a>'

    return 'No file selected for upload.'

@app.route('/download')
def download_pdfs():
    return render_template('download.html', uploaded_files=uploaded_files)

@app.route('/download/<filename>')
def download_pdf(filename):
    # Generate the full path to the uploaded PDF file
    pdf_path = os.path.join('uploads', filename)

    # Check if the file exists
    if os.path.exists(pdf_path):
        # Use Flask's send_file to send the file to the user's browser for download
        return send_file(pdf_path, as_attachment=True)
    else:
        return 'File not found.'

if __name__ == '__main__':
    app.run(debug=True)
