import ckan.lib.jobs as jobs
import ckan.model as model
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.model.domain_object import DomainObjectOperation

from ckanext.geopusher.tasks import process_resource


class GeopusherPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IDomainObjectModification)

    def notify(self, entity, operation=None):
        if isinstance(entity, model.Resource):
            resource_id = entity.id
            state = entity.state
            file_format = entity.format
            
            is_new_or_update = operation in [DomainObjectOperation.new, DomainObjectOperation.changed]

            if is_new_or_update and file_format.upper() == 'SHP' and state != 'deleted':
                site_url = toolkit.config.get('ckan.site_url', 'http://localhost/')
                apikey = model.User.get('default').apikey
                max_resource_size = toolkit.config.get('ckan.max_resource_size', 10)

                jobs.enqueue(process_resource, [resource_id, site_url, apikey, max_resource_size])
