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
*command* is instances , volumes or snapshots
*subcommand* - dependes upon command
*name*,*supportcontacts* is optional
#Sample commands
pipenv run py shotty/shotty.py list --supportcontacts=hello@email.com
#Stating ec2 with Name filter
$ pipenv run py shotty/shotty.py start --name='Streamset Data Collector'
#Stopping ec2 instance with Name
$ pipenv run py shotty/shotty.py stop --name='Streamset Data Collector'
#-------------------------------------------
#After adding instance and volumn group
$ pipenv run py shotty/shotty.py instances stop --name='Streamset Data Collector'

#Volume
$ pipenv run py shotty/shotty.py volumes list --supportcontacts=hello@time.com

#snapshots
$ pipenv run py shotty/shotty.py snapshots list --supportcontacts=hello@time.com
$ pipenv run py shotty/shotty.py snapshots list --all --supportcontacts=hello@time.com
#help
$ pipenv run py shotty/shotty.py --help
$ pipenv run py shotty/shotty.py instances --help