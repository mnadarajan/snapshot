import boto3
import click
import sys

session = boto3.Session()
ec2 = session.resource('ec2')

@click.command()
def list_instances():
    "List EC2 instances"
    for i in ec2.instances.all():
        print(', '.join((i.id,i.instance_type, i.placement['AvailabilityZone'],
                         i.state['Name'], str(i.platform), str(i.private_ip_address))))

    return


if __name__ == '__main__':
    #print(sys.argv)
    list_instances()


