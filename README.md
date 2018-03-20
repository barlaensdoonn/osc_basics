# osc_basics
Open Sound Control server and client in python via classes wrapped around [osc4py3](https://github.com/Xinne/osc4py3)

Configure parameters such as host, port, client name, and OSC message address in osc_config.yaml. The osc4py3 server works by binding a method to a particular OSC message address. This can be a single address, such as '/test', or an entire subset of addresses, such as '/test/\*'

This is using osc4py3.all_threads, but it can also be used in an event loop. Refer to osc4py3's [documentation](http://osc4py3.readthedocs.io/en/latest/) for more info
