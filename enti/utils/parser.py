from io import StringIO
import xml.etree.ElementTree as ET
from pprint import pprint
import yaml
from enti.settings import FileConfig

ENTITIES_TAG = 'entities'
ENTITY_TAG = 'entity'


def load_yml(filename):
    """Loads a YML document"""
    with open(filename) as f:
        return yaml.safe_load(f)


def load_xml(filename):
    """Loads XML document and strips the namespaces"""
    it = ET.iterparse(filename)
    for _, el in it:
        el.tag = el.tag.split('}', 1)[1]
    return it.root


def run_entity_extraction(filename):
    """Runs entity extraction from XML to dictionary format"""
    root = load_xml(filename)
    if root.tag == ENTITIES_TAG:
        return extract_entities(root)
    else:
        raise Exception("Invalid entity document. Could not parse the entity file.")


def extract_entities(node):
    """Extracts entities from root XML node"""
    entities = []
    for child in node:
        if child.tag == ENTITY_TAG:
            entities.append(extract_entity(child))
    return entities


def extract_entity(node):
    """Extracts an individual entity and attributes from an entity node"""
    entity = {
        'id': node.attrib.get('id'),
        'name': node.attrib.get('name'),
        'type': node.attrib.get('type'),
        'canonical': node.attrib.get('canonical')
    }
    attributes = []
    for child in node:
        attr_name = child.tag
        for attr in child:
            attributes.append({
                'id': attr_name,
                **attr.attrib
            })
    entity['attributes'] = attributes
    return entity


def export_entity_xml(entities, source='enti'):
    """Exports entities from pre-constructed dict format into an XML file

    :param entities: Pre-constructed entity dict
    :param source: Source attribute for root node
    """
    root_attrs = {
        'xmlns': 'digitalreasoning.com/entity/definitions',
        'source': source
    }
    root = ET.Element('entities', **root_attrs)
    for entity_id, entity in entities.items():
        entity_attrs = {
            'id': entity.get('id'),
            'name': entity.get('name'),
            'type': entity.get('type'),
            'canonical': str(entity.get('canonical')).lower()
        }
        node = ET.SubElement(root, 'entity', entity_attrs)
        for attribute_id, attribute in entity.get('attributes', {}).items():
            attr_node = ET.SubElement(node, attribute_id)
            for value in attribute.get('data', []):
                fields = {}
                for field in value.get('fields', []):
                    xml_id = field.get('xml_id', None)
                    fields[xml_id] = field['value']
                ET.SubElement(attr_node, 'value', fields)
    tree = ET.ElementTree(root)
    tree.write(FileConfig.EXPORT_FILE, encoding='utf-8', xml_declaration=True)
