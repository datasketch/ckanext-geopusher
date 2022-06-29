from ckanext.geopusher.lib import process

import ckanapi


def process_resource(resource_id, site_url, apikey, max_resource_size):
    ckan = ckanapi.RemoteCKAN(site_url, apikey=apikey)
    print("processing resource {0}".format(resource_id))
    process(ckan, resource_id, max_resource_size)
