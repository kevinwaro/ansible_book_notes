# Chapter 8

The secrets.yml file is encrypted. The password is `password`

## Usage

* To run the playbook:
```ansible-playbook --ask-vault-pass playbook.yml
```
* To view the content of the encrypted file:
```ansible-vault view --ask-vault-pass secrets.yml
```
