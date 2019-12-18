"""

 █████╗ ██████╗  █████╗ ███╗   ███╗ █████╗ ███╗   ██╗████████╗██╗██╗   ██╗███╗   ███╗
██╔══██╗██╔══██╗██╔══██╗████╗ ████║██╔══██╗████╗  ██║╚══██╔══╝██║██║   ██║████╗ ████║
███████║██║  ██║███████║██╔████╔██║███████║██╔██╗ ██║   ██║   ██║██║   ██║██╔████╔██║
██╔══██║██║  ██║██╔══██║██║╚██╔╝██║██╔══██║██║╚██╗██║   ██║   ██║██║   ██║██║╚██╔╝██║
██║  ██║██████╔╝██║  ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║   ██║   ██║╚██████╔╝██║ ╚═╝ ██║
╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝     ╚═╝

"""

from flask import (Flask,render_template, request)

import util
import zipfile
import os

app = Flask(__name__)

app.config.from_object(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'docx', 'pdf'}

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods = ['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        folder = app.config['UPLOAD_FOLDER'] + 'single'
        f.save(os.path.join(folder, f.filename))
        characteristics = util.getCharacteristics(folder + '/' + f.filename)
        util.removeAllFilesFrom(folder)
        return render_template("single-result.html", result = characteristics)

@app.route('/bulk-upload', methods = ['POST'])
def bulkUpload():
    if request.method == 'POST':
        f = request.files['file']

        with zipfile.ZipFile(f, 'r') as zip_ref:
            zip_ref.extractall(app.config['UPLOAD_FOLDER'] + 'bulk')

        characteristics = util.getCharacteristics('asdf')

        return render_template("bulk-result.html", resumesData = [characteristics])


if __name__ == '__main__':
   # app.run(debug = True)
    # app.run('127.0.0.1' , 5000 , debug=True)
    app.run('0.0.0.0' , 5000 , debug=True , threaded=True)
    
