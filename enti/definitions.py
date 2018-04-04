from enti.models import AttributeType, ArityType, EntityType, AttributeField

class TypeEnum:

    @staticmethod
    def list():
        raise Exception('Method not implemented')


class AttributeTypes(TypeEnum):

    INTEGER = AttributeType("integer", "Integer")
    ENTITY = AttributeType("entity", "Entity")
    NAMED_REF = AttributeType("named-reference", "Named Reference")
    DATE = AttributeType("date", "Date")
    STRING = AttributeType("string", "String")

    @staticmethod
    def list():
        return [
            AttributeTypes.INTEGER,
            AttributeTypes.ENTITY,
            AttributeTypes.NAMED_REF,
            AttributeTypes.DATE,
            AttributeTypes.STRING
        ]

class ArityTypes(TypeEnum):

    ONE = ArityType('one','One-to-One')
    FEW = ArityType('few','One-to-Few')
    MANY = ArityType('many','One-to-Many')

    @staticmethod
    def list():
        return [
            ArityTypes.ONE,
            ArityTypes.FEW,
            ArityTypes.MANY
        ]

class EntityTypes(TypeEnum):

    PERSON = EntityType('PERSON', 'Person')
    GPE = EntityType('GPE', 'Global Political Entity')
    LOCATION = EntityType ('LOCATION', 'Location')
    FIN_INST = EntityType('FIN_INST', 'Financial Institution')
    PHONE = EntityType('PHONE', 'Phone Number')
    ORGANIZATION = EntityType('ORGANIZATION', 'Organization')
    GOV_ORG = EntityType('GOV_ORG', 'Government Organization')
    MILITARY = EntityType('MILITARY', 'Military')
    BUSINESS = EntityType('BUSINESS', 'Business')
    ACADEMIC = EntityType('ACADEMIC', 'Academic Institution')

    @staticmethod
    def list():
        return [
            EntityTypes.PERSON,
            EntityTypes.GPE,
            EntityTypes.LOCATION,
            EntityTypes.FIN_INST,
            EntityTypes.PHONE,
            EntityTypes.ORGANIZATION,
            EntityTypes.GOV_ORG,
            EntityTypes.MILITARY,
            EntityTypes.BUSINESS,
            EntityTypes.ACADEMIC
        ]

class AttributeFields(TypeEnum):

    VALUE = AttributeField('v', 'Value')
    SID = AttributeField('sid', 'SID')
    SOURCE = AttributeField('source', 'Source')
    ID_TYPE = AttributeField('id-type', 'ID Type')
    ID_SEED = AttributeField('id-seed', 'ID Seed')
    NAME = AttributeField('name', 'Name')

    @staticmethod
    def list():
        return [
            AttributeFields.VALUE,
            AttributeFields.SID,
            AttributeFields.SOURCE,
            AttributeFields.ID_TYPE,
            AttributeFields.ID_SEED,
            AttributeFields.NAME
        ]