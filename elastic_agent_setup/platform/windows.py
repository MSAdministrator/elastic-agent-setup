from .platform import Platform


class Windows(Platform):

    def extract(self):
        from zipfile import ZipFile
        with ZipFile(self.settings.download_endpoint, 'r') as zipObj:
            zipObj.extractall('C:/elastic-agent')
