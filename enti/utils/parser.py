from io import StringIO
import xml.etree.ElementTree as ET
from pprint import pprint
import yaml

ENTITIES_TAG = 'entities'
ENTITY_TAG = 'entity'


def run_entity_extraction(filename):
    root = load_xml(filename)

    print('<{}:{}>'.format(root.tag, root.attrib))

    if root.tag == ENTITIES_TAG:
        return extract_entities(root)

    else:
        print('Invalid XML document. Expected tag <{}>, but read <{}>'.format(ENTITIES_TAG, root.tag))

def load_yml(filename):
    """Loads a YML document"""
    with open(filename) as f:
        yml = yaml.safe_load(f)
        pprint(yml)
        return yml


def load_xml(filename):
    '''Loads XML document and strips the namespaces'''
    it = ET.iterparse(filename)
    for _, el in it:
        el.tag = el.tag.split('}', 1)[1]
    return it.root


def extract_entities(node):
    print('Extracting entities')

    entities = []

    for child in node:
        if child.tag == ENTITY_TAG:
            entities.append(extract_entity(child))

    pprint(entities)
    return entities


def extract_entity(node):
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


def extract_attributes():
    root = load_xml('../../res/attributes.xml')
    attributes = [
        {
            'type': child.tag,
            **child.attrib
        }
        for child in root
    ]
    pprint(attributes)


def build_entity_xml():
    entities = run_entity_extraction('../../res/enam.xml')

    root_attrs = {
        'xmlns': 'digitalreasoning.com/entity/definitions',
        'source': 'test'
    }
    root = ET.Element('entities', **root_attrs)

    for entity in entities:
        entity_attrs = {
            'id': entity.get('id'),
            'name': entity.get('name'),
            'type': entity.get('type'),
            'canonical': entity.get('canonical')
        }
        node = ET.SubElement(root, 'entity', entity_attrs)

        attr_dict = {}

        for attr in entity.get('attributes', []):

            pprint(attr)
            name = attr.pop('id', None)

            if attr_dict.get(name) is None:
                attr_dict[name] = [attr]
            else:
                attr_dict[name].append(attr)

        pprint(attr_dict)

        for k,v in attr_dict.items():

            val_node = ET.SubElement(node, k)

            for val in v:
                ET.SubElement(val_node, 'value', val)

    tree = ET.ElementTree(root)
    tree.write('../../res/out.xml', encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    # run()
    # build_entity_xml()
    load_yml('../schema/attributes.yml')