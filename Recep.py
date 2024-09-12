#Receptor 

from flask import Flask, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = './uploaded_files'  

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    # Guardar el archivo en el directorio especificado
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    return "Archivo subido y guardado exitosamente", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4444)
