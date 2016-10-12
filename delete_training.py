from linode import Api
from mykeys import api_key

import pprint
import sys
import time

base_label = 'training-'

pp = pprint.PrettyPrinter(indent=4)

api = Api(api_key)


def wait_jobs(linode_id, job_id):
    while True:
        rez = api.linode.job.list(LinodeID=linode_id, JobID=job_id, pendingOnly=True)
        if rez[0]['HOST_SUCCESS'] == 1:
            return
        print '.',
        sys.stdout.flush()
        time.sleep(1)

for linode in api.linode.list():
    label = linode['LABEL']
    if label.startswith(base_label):
        print "Deleting %s" % label,
        sys.stdout.flush()
        linode_id = linode['LINODEID']
        if linode['STATUS'] == 1:
            job_id = api.linode.shutdown(linode_id)['JobID']
            wait_jobs(linode_id, job_id)
        for disk in api.linode.disk.list(linode_id):
            job_id = api.linode.disk.delete(LinodeID=linode_id, DiskID=disk['DISKID'])['JobID']
            wait_jobs(linode_id, job_id)
        api.linode.delete(linode_id)
        print
        sys.stdout.flush()

for domain in api.domain.list():
    dname = domain['DOMAIN']
    domain_id = domain['DOMAINID']
    for resource in api.domain.resource.list(DomainID=domain_id):
        name = resource['NAME']
        if name.startswith(base_label):
            print "Deleting DNS resource %s.%s" % (dname, name)
            sys.stdout.flush()
            api.domain.resource.delete(DomainID=domain_id, ResourceID=resource['RESOURCEID'])
