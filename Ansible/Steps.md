## Install Ansible on Ubuntu

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible
```

[Installation Link Ansible](https://docs.ansible.com/ansible/latest/installation_guide/installation_distros.html#installing-ansible-on-ubuntu)

## Use Ansible to Update Docker

1. Make Sure hosts are added as Known_host
2. Run Ansible Playbook

```bash
ansible-playbook -i host playbook.yml
```
