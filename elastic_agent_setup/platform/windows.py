import subprocess
from .platform import Platform
from ..settings import Settings


class Windows(Platform):

    def install_certificate(self):
        return subprocess.run(f'certutil.exe -addstore root {Settings.certificate_authority}')

    def extract(self):
        from zipfile import ZipFile
        with ZipFile(Settings.download_path, 'r') as zipObj:
            zipObj.extractall('C:/elastic-agent')
