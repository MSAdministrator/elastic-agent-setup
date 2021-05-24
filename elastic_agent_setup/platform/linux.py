import os
import shutil
import subprocess
from .platform import Platform
from ..settings import Settings


class Linux(Platform):

    def install_certificate(self):
        if not os.path.exists('/usr/local/share/ca-certificates/ca.crt'):
            shutil.copy(Settings.certificate_authority, '/usr/local/share/ca-certificates/ca.crt')
            subprocess.run('update-ca-certificates')

    def extract(self):
        import tarfile
        tar = tarfile.open(Settings.download_path, "r:gz")
        tar.extractall()
        tar.close()
