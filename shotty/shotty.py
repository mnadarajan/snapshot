import boto3
import click
import sys

session = boto3.Session()
ec2 = session.resource('ec2')

def filter_instances(name):
    instances = []

    if name:
        filter = [{'Name':'tag:Name', 'Values':[name]}]
        instances = ec2.instances.filter(Filters=filter)
    else:
        instances = ec2.instances.all()

    return instances


@click.group()
def instances():
    " Command for instances "

@instances.command('list')
@click.option('--supportcontacts', default=None, help="Only instances with SupportContats(tag SupportContatcs:<value>)")

def list_instances(supportcontacts):
    "List EC2 instances"
    instances = []

    if supportcontacts:
        filter = [{'Name':'tag:SupportContacts', 'Values':[supportcontacts]}]
        instances = ec2.instances.filter(Filters=filter)
    else:
        instances = ec2.instances.all()

    for i in instances:
        tags = {t['Key']:t['Value'] for t in i.tags or []}  # or [] in case tag is empty gives empty list
        print(', '.join((i.id,i.instance_type, i.placement['AvailabilityZone'],
                         i.state['Name'], str(i.platform), str(i.private_ip_address),
                         tags.get('Name','<No Name>'), tags.get('SupportContacts', '<No Support Contacts>'))))

    return


@instances.command('stop')
@click.option('--name', default=None, help="Only instances with SupportContats(tag SupportContatcs:<value>)")

def stop_instances(name):
    "Stop EC2 Instances"
    instances = filter_instances(name)

    for i in instances:
        print("Stopping {0} ....".format(i.id))
        i.stop()
    return

@instances.command('start')
@click.option('--name', default=None, help="Only instances with SupportContats(tag SupportContatcs:<value>)")

def start_instances(name):
    "Stop EC2 Instances"
    instances = []

    instances = filter_instances(name)

    for i in instances:
        print("Starting {0} ....".format(i.id))
        i.start()
    return


if __name__ == '__main__':
    #print(sys.argv)

    #list_instances() # After adding @group this is removed .
    instances()


