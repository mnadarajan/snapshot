import boto3
import botocore
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
def cli():
    "To manage snapshots"


@cli.group('snapshots')
def snapshots():
    "Commands for volumes"
@snapshots.command('list')
@click.option('--supportcontacts', default=None, help="volumns for  for SupportContats(tag SupportContatcs:<value>)")
@click.option('--all', 'list_all', default=False,is_flag=True,help="List all snapshots for all volumns not just the most recent")
#if --all flat is set list_all will be true, default is false, so it will show only latest snapshot
def list_snapshots(supportcontacts,list_all):
    "List EC2 volumes"
    instances = []

    if supportcontacts:
        filter = [{'Name':'tag:SupportContacts', 'Values':[supportcontacts]}]
        instances = ec2.instances.filter(Filters=filter)
    else:
        instances = ec2.instances.all()

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%C")
                )))
                if s.state == 'completed' and not list_all: break  # to show only recent snapshots.
    return




@cli.group('volumes')
def volumes():
    "Commands for volumes"
@volumes.command('list')
@click.option('--supportcontacts', default=None, help="volumns for  for SupportContats(tag SupportContatcs:<value>)")

def list_volumes(supportcontacts):
    "List EC2 volumes"
    instances = []

    if supportcontacts:
        filter = [{'Name':'tag:SupportContacts', 'Values':[supportcontacts]}]
        instances = ec2.instances.filter(Filters=filter)
    else:
        instances = ec2.instances.all()

    for i in instances:
        for v in i.volumes.all():
            print(", ".join((
                v.id,
                i.id,
                v.state,
                str(v.size) + "GiB",
                v.encrypted and "Encrypted" or "Not Encrypted"
            )))

    return




@cli.group('instances')
def instances():
    " Command for instances "

@instances.command('snapshot')
@click.option('--name', default=None, help="Only instances with SupportContats(tag SupportContatcs:<value>)")
def create_snapshot(name):
    "Create snapshot for EC2 instances"
    instances = filter_instances(name)
    for i in instances:
        print("Stoppng  of {0}".format(i.id))
        i.stop()
        i.wait_until_stopped()
        for v in i.volumes.all():
            print("Creating snapshot of {0}".format(v.id))
            v.create_snapshot()
        print("Starting  of {0}".format(i.id))
        i.start()
        i.wait_until_running()

    print("Snapshots created")
    return

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
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print("Could not stop {0}. ".format(i.id) + str(e))
            continue
    return

@instances.command('start')
@click.option('--name', default=None, help="Only instances with SupportContats(tag SupportContatcs:<value>)")

def start_instances(name):
    "Stop EC2 Instances"
    instances = []

    instances = filter_instances(name)

    for i in instances:
        print("Starting {0} ....".format(i.id))
        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print("Could not start {0}. ".format(i.id) + str(e))
            continue

    return


if __name__ == '__main__':
    #print(sys.argv)
    #list_instances() # After adding @group this is removed .
    #instances()
    cli()


