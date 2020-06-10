Demo project to manage AWS EC2 instance snapshot

## About
This is using boto3 to list ec2 instance,
boto3 is installed in pipenv environment.

## Configuration.
aws configure has to be completed before running scirpt.
login using aws-azure-login
pipenv install click
#Running

pipenv run py shotty.py


# Click group is added as below.
pipenv run py shotty.py <command> <--name='Name>
*command* is list, start , stop
*name* is optional
#Sample commands
pipenv run py shotty/shotty.py list --supportcontacts=hello@email.com
#Stating ec2 with Name filter
$ pipenv run py shotty/shotty.py start --name='Streamset Data Collector'
#Stopping ec2 instance with Name
$ pipenv run py shotty/shotty.py stop --name='Streamset Data Collector'