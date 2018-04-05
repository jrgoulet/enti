from enti.tasks import initialize_defaults, initialize_attributes
from enti.query import Query
from enti.database import session_scope
from enti.settings import FileConfig
from enti.utils.parser import run_entity_extraction
import os
from enti.extensions import log
from pprint import pprint

class Controller:

    def __init__(self):
        pass

    def initialize(self):
        initialize_defaults()
        initialize_attributes()

    def sync_attributes(self):

        with session_scope() as session:

            attr_json = {a.id:a.json() for a in Query.Attribute.all(session)}

            for attr_id in attr_json.keys():

                linked_fields = {
                    lf.field_id:Query.AttributeField.get(session, lf.field_id).json()
                    for lf in Query.LinkedAttributeField.filter(session, attr_id)
                }

                attr_json[attr_id]['fields'] = linked_fields

            return attr_json


    def upload_xml(self):

        for dirpath, dnames, fnames in os.walk(FileConfig.DATA_DIR):
            for f in fnames:
                filename = os.path.join(dirpath, f)
                if f.endswith(".xml"):
                    entities = run_entity_extraction(filename)
                    if entities is not None:
                        log.info('Entity extraction successful')
                        pprint(entities)
                os.remove(filename)




