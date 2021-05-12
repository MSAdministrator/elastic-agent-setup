# elastic-agent-setup

A python package to install and enroll an Elastic Agent on multiple host operating systems.

## Getting Started

In order to use this package you must configure general settings for your environment. Here is an example of the configuration options:

```python
from elastic_agent_setup import ElasticAgent

agent = ElasticAgent()
agent.configure(
    username='admin', 
    password='some_password'
    elasticsearch='https://elasticsearch:9200',
    kibana='https://kibana:5601',
    certificate_authority=None,
    verify_ssl=True
)
```

Once you have configured the `elastic-agent-setup` package you can either `install` or `enroll` your elastic-agent.

> Please see Elatics documentation on the differences between enrolling and installing an agent.

Here is an example of installing an Elastic Agent:

```python
from elastic_agent_setup import ElasticAgent

agent = ElasticAgent()
agent.configure(
    username='admin', 
    password='some_password'
    elasticsearch='https://elasticsearch:9200',
    kibana='https://kibana:5601',
    certificate_authority=None,
    verify_ssl=True
)

response = agent.install(
    version='7.12.1,
    preflight_check=True
)

print(response)
```

## Built With

* [carcass](https://github.com/MSAdministrator/carcass) - Python packaging template

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. 

## Authors

* Josh Rickard - *Initial work* - [MSAdministrator](https://github.com/MSAdministrator)

See also the list of [contributors](https://github.com/MSAdministrator/elastic-agent-setup/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details
