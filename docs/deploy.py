
'''
Script de utilidad para desplegar los ficheros estáticos generados por apidoc en
un servidor.
'''

from logger import Logger
from os.path import dirname, join, basename, abspath, relpath
import os
from os import remove as remove_file
from zipfile import ZipFile
import requests


# Esta variable indica la url del servidor donde se despleguará la documentación.
DEPLOY_SERVER_URI = '{Deploy Server URL here}'


def deploy():
    apidocs_dir_path = join(dirname(__file__), 'apidocs')
    aipdocs_zip_path = join(dirname(apidocs_dir_path), 'apidocs.zip')

    try:
        with ZipFile(aipdocs_zip_path, 'w') as zipfile:
            for dir, folders, files in os.walk(apidocs_dir_path):
                for file in files:
                    file_path = abspath(join(dir, file))
                    file_name = relpath(file_path, dirname(apidocs_dir_path))
                    zipfile.write(file_path, file_name)


        with open(aipdocs_zip_path, 'rb') as zipfile:
            data = zipfile.read()
            Logger().debug('Deploying api doc files to "{}"'.format(DEPLOY_SERVER_URI))
            response = requests.post(url = join(DEPLOY_SERVER_URI, 'deploy'),
                                     data = data)
            if response.status_code != 200:
                raise Exception()
            print(response.text)
    except Exception as exc:
        raise Exception('Error deploying ApiDocs: {}'.format(str(exc)))

        remove_file(aipdocs_zip_path)

if __name__ == '__main__':
    deploy()