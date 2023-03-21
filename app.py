import os
import random
import string
from flask import Flask, request, redirect, render_template, url_for, send_from_directory
from redis import Redis
from werkzeug.utils import secure_filename

app = Flask(__name__)
redis = Redis()

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

#@app.route('/', methods=['GET', 'POST'])
#def index():
#    if request.method == 'POST':
#        url = request.form['url']
#        if not url:
#            flash('Please enter a URL')
#            return redirect(request.url)
#
#        short_id = random_string(6)
#        redis.set(short_id, url)
#        return render_template('index.html', short_url=f"{request.host_url}{short_id}")
#
#    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        if not url:
            flash('Please enter a URL')
            return redirect(request.url)

        short_id = random_string(6)
        redis.set(short_id, url)
        short_url = f"{request.host_url}{short_id}"
        return render_template('index.html', short_url=f"{request.host_url}{short_id}")

    else:
        short_ids = redis.keys()
        short_urls = []
        for short_id in short_ids:
            short_url = f"{request.host_url}{short_id.decode('utf-8')}"
            short_urls.append(short_url)

        file_names = os.listdir(app.config['UPLOAD_FOLDER'])
        file_urls = []
        for file_name in file_names:
            file_url = url_for('uploaded_file', filename=file_name)
            file_urls.append((file_name, file_url))

        return render_template('index.html', short_urls=short_urls, file_urls=file_urls)


@app.route('/<short_id>')
def redirect_url(short_id):
    original_url = redis.get(short_id)
    if original_url:
        return redirect(original_url.decode('utf-8'))
    else:
        return "URL not found.", 404

@app.route('/file_upload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('file_upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
