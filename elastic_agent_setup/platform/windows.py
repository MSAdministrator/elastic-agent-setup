from .platform import Platform
from ..settings import Settings


class Windows(Platform):

    def extract(self):
        from zipfile import ZipFile
        with ZipFile(Settings.download_endpoint, 'r') as zipObj:
            zipObj.extractall('C:/elastic-agent')
