from .platform import Platform
from ..settings import Settings


class Linux(Platform):

    def extract(self):
        import tarfile
        tar = tarfile.open(Settings.download_endpoint, "r:gz")
        tar.extractall()
        tar.close()
