from setuptools import setup, find_packages

def parse_requirements(requirement_file):
    with open(requirement_file) as f:
        return f.readlines()

version = dict()
with open("./elastic_agent_setup/utils/version.py") as fp:
    exec(fp.read(), version)


setup(
    name='elastic-agent-setup',
    version=version['__version__'],
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A Python package used to install and enroll the Elastic Agent on multiple operating systems. Created using carcass',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=parse_requirements('./requirements.txt'),
    keywords=['carcass'],
    url='https://github.com/MSAdministrator/elastic-agent-setup',
    author='MSAdministrator',
    author_email='rickardja@live.com',
    python_requires='>=3.6, <4',
    package_data={
        'elastic_agent_setup':  ['data/logging.yml']
    },
    entry_points={
          'console_scripts': [
              'elastic-agent-setup = elastic_agent_setup.__main__:main'
          ]
    }
)