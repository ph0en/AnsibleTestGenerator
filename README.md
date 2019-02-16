# AnsibleTestGenerator
Generate and run pytest tests for ansible playbooks.
Works only with some features of yum, file ansible modules
###### RUN:
on localhost:
`pytest main.py`

on remote host: `pytest main.py --connection=ansible --ansible-inventory <path>/<to>/<your>/<inventory>/<file> --hosts=<host.from.inventory.file.tld>`
