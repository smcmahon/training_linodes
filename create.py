from linode import Api
from mykeys import api_key

import pprint

pp = pprint.PrettyPrinter(indent=4)

api = Api(api_key)
domain_name = 'cloneplone.info'
soa_email = 'steve@dcn.org'
root_password = 'twerk45nonesuch'
start_at = 10
create_count = 1
base_label = 'training-'
data_center = 6  # Newark
plan_id = 1

# Make sure we have a DNS zone
domain_list = [a for a in api.domain.list() if a['DOMAIN'] == domain_name]
if domain_list:
    domain_id = domain_list[0]['DOMAINID']
    print "Found %s zone" % domain_name
else:
    rez = api.domain.create(
        Domain=domain_name,
        Type='master',
        SOA_Email=soa_email,
    )
    domain_id = rez['DOMAINID']
    print 'Created %s zone' % domain_name

# print domain_id

for counter in range(start_at, start_at + create_count):
    label = "%s%s" % (base_label, counter)

    # create a linode
    print "Creating %s" % label
    rez = api.linode.create(
        DatacenterID=data_center,
        PlanID=plan_id,
    )
    linode_id = rez['LinodeID']
    # print linode_id

    print "Labeling"
    rez = api.linode.update(
        LinodeID=linode_id,
        Label=label,
    )

    print "Creating boot disk"
    rez = api.linode.disk.createfromdistribution(
        LinodeID=linode_id,
        DistributionID=146,
        Label='root',
        Size=22 * 1024,
        rootPass=root_password,
    )
    # print rez

    disk_id = rez['DiskID']
    # print disk_id

    print "Creating swap disk"
    rez = api.linode.disk.create(
        LinodeID=linode_id,
        Label='swap',
        Type='swap',
        Size=2 * 1024,
    )
    swap_id = rez['DiskID']

    print "Creating config"
    rez = api.linode.config.create(
        LinodeID=linode_id,
        KernelID=138,
        Label='MYCONFIG',
        DiskList="%s,%s" % (disk_id, swap_id),
        RootDeviceNum=1,
    )
    # print rez

    print "Booting"
    rez = api.linode.boot(
        LinodeID=linode_id
    )

    # get the ip address
    rez = api.linode.ip.list(LinodeID=linode_id)
    # print rez
    ip_address = rez[0]['IPADDRESS']
    print ip_address

    print "Creating A record"
    rez = api.domain.resource.create(
        DomainID=domain_id,
        Type='A',
        Name=label,
        Target=ip_address,
        TTL_sec=300,
    )
    print "---------"
