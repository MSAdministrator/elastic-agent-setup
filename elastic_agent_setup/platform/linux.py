from .platform import Platform


class Linux(Platform):

    def extract(self):
        import tarfile
        tar = tarfile.open(self.settings.download_endpoint, "r:gz")
        tar.extractall()
        tar.close()
