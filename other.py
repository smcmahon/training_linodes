from linode import Api
from mykeys import api_key

import pprint

pp = pprint.PrettyPrinter(indent=4)

api = Api(api_key)

pp.pprint(
    [(a['DATACENTERID'], a['ABBR']) for a in api.avail.datacenters()]
)

pp.pprint(
    [(a['KERNELID'], a['LABEL']) for a in api.avail.kernels()]
)

pp.pprint(
    [(a['DISTRIBUTIONID'], a['LABEL']) for a in api.avail.distributions()]
)

pp.pprint(
    [(a['PLANID'], a['LABEL']) for a in api.avail.linodeplans()]
)
