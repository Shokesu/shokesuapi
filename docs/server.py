

from flask import Flask, render_template
from os.path import dirname, join

app = Flask(__name__,
            static_folder = 'apidocs',
            static_url_path = ''
            )


@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
def serve():
    with open(join(dirname(__file__), 'apidocs', 'index.html')) as fh:
        return fh.read()


if __name__ == '__main__':
    app.run()