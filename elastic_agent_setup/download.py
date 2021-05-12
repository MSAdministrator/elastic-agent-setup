from .core import Core, Settings


class Download(Core):

    host = 'https://artifacts.elastic.co/downloads/beats/elastic-agent/{endpoint}'
    endpoint = Settings.download_endpoint
    kwargs = {
        'stream': True
    }

    def parse_response(self, response):
        with open(Settings.download_endpoint, 'wb') as f:
            for chunk in response.raw.stream(1024, decode_content=False):
                if chunk:
                    f.write(chunk)
