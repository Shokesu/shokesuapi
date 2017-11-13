

from flask import Flask, render_template, request, make_response
from os.path import dirname, join
from os import remove as remove_file
from zipfile import ZipFile
from threading import Lock

apidocs_folder = join(dirname(__file__), 'static', 'apidocs')

app = Flask(__name__,
            static_folder = apidocs_folder,
            static_url_path = ''
            )

lock = Lock()


@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
def serve():
    with lock:
        with open(join(apidocs_folder, 'index.html'),'r') as fh:
            return fh.read()

@app.route('/deploy', methods = ['POST'])
def deploy():
    with lock:
        try:
            apidocs_zip_path = join(dirname(__file__), 'apidocs.zip')
            with open(apidocs_zip_path, 'wb') as zipfile:
                zipfile.write(request.data)

            with ZipFile(apidocs_zip_path, 'r') as zipfile:
                zipfile.extractall(path = dirname(apidocs_folder))
            remove_file(apidocs_zip_path)

            return "API Docs Deployed correctly"
        except:
            return make_response('Error deploying ApiDocs', 500)

if __name__ == '__main__':
    app.run()