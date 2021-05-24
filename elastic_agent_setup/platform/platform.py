import abc
import os
import subprocess
from ..settings import Settings


class Platform:

    def __init__(self):
        if not os.path.exists(Settings.download_path):
            from ..download import Download
            Download().run()

    @abc.abstractmethod
    def extract(self):
        raise NotImplemented

    @abc.abstractmethod
    def install_certificate(self):
        raise NotImplemented

    def run(self, subcommand='install'):
        self.extract()
        if Settings.certificate_authority:
            self.install_certificate()
        if Settings.platform == 'Linux' or Settings.platform == 'Darwin':
            split_on = '.tar.gz'
        elif Settings.platform == 'Windows':
            split_on = '.zip'
        command = Settings.agent_command_string.format(
            dir=os.path.join('/', Settings.download_endpoint.rsplit(split_on,1)[0]),
            subcommand=subcommand,
            force=Settings.force_enroll if Settings.force_enroll else '',
            kibana=Settings.kibana,
            token=Settings.enrollment_token,
            certificate_authorities=f'--certificate-authorities="{Settings.certificate_authority}"' if Settings.certificate_authority else '',
            insecure='--insecure' if Settings.verify_ssl else ''
        )
        return subprocess.run(command, shell=True, check=True, capture_output=True)
