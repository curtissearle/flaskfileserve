from flask import Flask, send_from_directory, render_template, request, redirect, url_for
import os
import time
import urllib.parse
import argparse

app = Flask(__name__)
ALLOWED_EXTENSIONS =  {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp', 'svg', 'ico', 'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv', 'webm', 'mpeg', 'mpg', '3gp', 'm4v', 'ogv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    files = []
    for filename in os.listdir(app.config['FILE_FOLDER']):
        filepath = os.path.join(app.config['FILE_FOLDER'], filename)
        if os.path.isfile(filepath) and allowed_file(filepath):
            date_modified = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(filepath)))
            date_created = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getctime(filepath)))
            file_size = round(os.path.getsize(filepath) / (1024 * 1024), 3)  # File size in MB rounded to 3 decimal places
            files.append((filename, date_modified, date_created, file_size))
    return render_template('index.html', files=files)

@app.route('/files/<path:filename>')
def serve_file(filename):
    # Decode the filename
    filename = urllib.parse.unquote(filename)
    files = [f for f in os.listdir(app.config['FILE_FOLDER']) if allowed_file(f)]
    files.sort()  # Sort files to maintain a consistent order
    if filename not in files:
        return redirect(url_for('index'))  # Redirect to index if file is not found
    current_index = files.index(filename)
    return render_template('slideshow.html', filename=filename, files=files, current_index=current_index, total_files=(len(files) -1))

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['FILE_FOLDER'], filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask app with the specified upload folder.')
    parser.add_argument('--folder', required=True, help='Path to the file folder')
    args = parser.parse_args()

    app.config['FILE_FOLDER'] = args.folder
    app.run(debug=True)