import subprocess
from .platform import Platform
from ..settings import Settings


class MacOS(Platform):

    def install_certificate(self):
        subprocess.run(f'sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain {Settings.certificate_authority}')

    def extract(self):
        import tarfile
        tar = tarfile.open(Settings.download_path, "r:gz")
        tar.extractall()
        tar.close()
