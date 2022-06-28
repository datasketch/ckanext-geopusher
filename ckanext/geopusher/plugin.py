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
            # new event is sent, then a changed event.
            if operation == DomainObjectOperation.changed:
                # There is a NEW or CHANGED resource. We should check if
                # it is a shape file and pass it off to Denis's code if
                # so it can process it
                site_url = toolkit.config.get('ckan.site_url', 'http://localhost/')
                apikey = model.User.get('default').apikey

                jobs.enqueue(process_resource, [resource_id, site_url, apikey])
