from linode import Api
from mykeys import api_key

import pprint

pp = pprint.PrettyPrinter(indent=4)

api = Api(api_key)

for linode in api.linode.list():
    print linode['LABEL'],
    print api.linode.ip.list(LinodeID=linode['LINODEID'])[0]['IPADDRESS']

for domain in api.domain.list():
    print domain['DOMAIN']
    domain_id = domain['DOMAINID']
    resources = api.domain.resource.list(DomainID=domain_id)
    for resource in resources:
        print resource['NAME'], resource['TYPE'], resource['TARGET']
