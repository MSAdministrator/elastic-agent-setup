from .core import Core, Settings


class Download(Core):

    host = 'https://artifacts.elastic.co/downloads/beats/elastic-agent/{endpoint}'
    endpoint = Settings.download_endpoint
    kwargs = {
        'stream': True
    }

    def parse_response(self, response):
        self.__logger.debug('Saving file to download path: {}'.format(Settings.download_path))
        with open(Settings.download_path, 'wb+') as f:
            for chunk in response.raw.stream(1024, decode_content=False):
                if chunk:
                    f.write(chunk)
        self.__logger.debug('File saved successfully')
