# forensic_recovery_tool/app.py

import os
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from file_carver import scan_image
from utils import log_carving_activity

# Initialize Flask application
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuration
UPLOAD_FOLDER = 'uploads'
RECOVERED_FOLDER = 'recovered_files'
ALLOWED_EXTENSIONS = {'img', 'dsk', 'dd', 'iso', 'bin'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB limit

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RECOVERED_FOLDER, exist_ok=True)

# Flask configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    """
    Checks if the uploaded file has an allowed extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """
    Serves the upload page.
    """
    log_carving_activity("User accessed the upload page")
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    """
    Handles disk image upload and initiates file carving.
    """
    try:
        # Check if file was provided
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if file is empty
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file extension is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: img, dsk, dd, iso, bin'}), 400
        
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        log_carving_activity(f"File uploaded: {filename}")
        
        # Start file carving
        log_carving_activity(f"Starting file carving on {filename}")
        recovered_files = scan_image(file_path)
        
        # Clean up the uploaded file (read-only constraint)
        try:
            os.remove(file_path)
            log_carving_activity(f"Uploaded file {filename} deleted after processing")
        except Exception as e:
            log_carving_activity(f"Warning: Could not delete uploaded file {filename}: {e}")
        
        # Return results
        return jsonify({
            'success': True,
            'recovered_files': recovered_files,
            'total_files': len(recovered_files)
        }), 200
        
    except Exception as e:
        log_carving_activity(f"Error during upload/carving: {e}")
        return jsonify({'error': f'Processing error: {str(e)}'}), 500

@app.route('/results')
def results():
    """
    Serves the results page.
    """
    log_carving_activity("User accessed the results page")
    return render_template('results.html')

@app.route('/download/<filename>')
def download_file(filename):
    """
    Allows users to download recovered files.
    """
    try:
        # Secure the filename to prevent directory traversal attacks
        filename = secure_filename(filename)
        file_path = os.path.join(RECOVERED_FOLDER, filename)
        
        # Verify the file exists and is within the recovered folder
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        log_carving_activity(f"Downloading file: {filename}")
        return send_file(file_path, as_attachment=True)
        
    except Exception as e:
        log_carving_activity(f"Error downloading file {filename}: {e}")
        return jsonify({'error': 'Download error'}), 500

@app.route('/api/recovered-files')
def get_recovered_files():
    """
    Returns a list of all recovered files in JSON format.
    """
    try:
        files = []
        if os.path.exists(RECOVERED_FOLDER):
            for filename in os.listdir(RECOVERED_FOLDER):
                file_path = os.path.join(RECOVERED_FOLDER, filename)
                if os.path.isfile(file_path):
                    file_size = os.path.getsize(file_path)
                    file_type = filename.rsplit('.', 1)[-1] if '.' in filename else 'unknown'
                    files.append({
                        'filename': filename,
                        'type': file_type,
                        'size': file_size
                    })
        return jsonify(files), 200
    except Exception as e:
        log_carving_activity(f"Error retrieving recovered files: {e}")
        return jsonify({'error': 'Error retrieving files'}), 500

@app.route('/api/clear-results', methods=['POST'])
def clear_results():
    """
    Clears all recovered files (optional feature for cleanup).
    """
    try:
        if os.path.exists(RECOVERED_FOLDER):
            for filename in os.listdir(RECOVERED_FOLDER):
                file_path = os.path.join(RECOVERED_FOLDER, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        log_carving_activity("Recovered files cleared")
        return jsonify({'success': True}), 200
    except Exception as e:
        log_carving_activity(f"Error clearing results: {e}")
        return jsonify({'error': 'Error clearing results'}), 500

if __name__ == '__main__':
    log_carving_activity("Flask application started")
    app.run(debug=True, host='0.0.0.0', port=5000)
