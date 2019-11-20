#!/usr/bin/env python
"""
Vagrant external inventory script. Automatically finds the IP of the booted vagrant vm(s), and
returns it under the host group 'vagrant'

Example Vagrant configuration using this script:

    config.vm.provision :ansible do |ansible|
      ansible.playbook = "./provision/your_playbook.yml"
      ansible.inventory_file = "./provision/inventory/vagrant.py"
      ansible.verbose = true
    end
"""

# Adapted from Mark Mandel's implementation
# https://github.com/ansible/ansible/blob/stable-2.1/contrib/inventory/vagrant.py
# License: GNU General Public License, Version 3 <http://www.gnu.org/licenses/>

import argparse
import json
import paramiko
import subprocess
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Vagrant inventory script")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true')
    group.add_argument('--hosts')
    return parser.parse_args()


def list_running_hosts():
    cmd = "vagrant status --machine-readable"
    status = subprocess.check_output(cmd.split()).rstrip()
    hosts = []
    for line in status.split('\n'):
        (_, host, key, value) = line.split(',')[:4]
        if key == 'state' and value == 'running':
            hosts.append(host)
    return hosts


def get_hosts_details(host):
    cmd = "vagrant ssh-config {}".format(host)
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    config = paramiko.SSHConfig()
    config.parse(p.stdout)
    c = config.lookup(host)
    return {'ansible_host': c['hostname'],
            'ansible_port': c['port'],
            'ansible_user': c['user'],
            'ansible_private_key_file': c['identityfile'][0]}

def main():
    args = parse_args()
    if args.list:
        hosts = list_running_hosts()
        json.dump({'vagrant': hosts}, sys.stdout)
    else:
        details = get_hosts_details(args.hosts)
        json.dump(details, sys.stdout)


if __name__ == '__main__':
    main()
