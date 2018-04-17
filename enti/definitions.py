from enti.models import AttributeType, ArityType, EntityType, AttributeField, Setting
from enti.settings import AppConfig

class AttributeTypes:
    """Enumeration of default attribute types"""

    INTEGER = AttributeType("integer", "Integer")
    ENTITY = AttributeType("entity", "Entity")
    NAMED_REF = AttributeType("named-reference", "Named Reference")
    DATE = AttributeType("date", "Date")
    STRING = AttributeType("string", "String")

    @staticmethod
    def list():
        """Return a list of defaults for database initialization"""
        return [
            AttributeTypes.INTEGER,
            AttributeTypes.ENTITY,
            AttributeTypes.NAMED_REF,
            AttributeTypes.DATE,
            AttributeTypes.STRING
        ]

class ArityTypes:
    """Enumeration of default arity types"""

    ONE = ArityType('one','One-to-One')
    FEW = ArityType('few','One-to-Few')
    MANY = ArityType('many','One-to-Many')

    @staticmethod
    def list():
        """Return a list of defaults for database initialization"""
        return [
            ArityTypes.ONE,
            ArityTypes.FEW,
            ArityTypes.MANY
        ]

class EntityTypes:
    """Enumeration of default entity types"""

    PERSON = EntityType('PERSON', 'Person')
    GPE = EntityType('GPE', 'Geopolitical Entity')
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
        """Return a list of defaults for database initialization"""
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

class AttributeFields:
    """Enumeration of default attribute fields"""

    VALUE = AttributeField('v', 'Value')
    SID = AttributeField('sid', 'SID')
    SOURCE = AttributeField('source', 'Source')
    ID_TYPE = AttributeField('id-type', 'ID Type')
    ID_SEED = AttributeField('id-seed', 'ID Seed')
    NAME = AttributeField('name', 'Name')

    @staticmethod
    def list():
        """Return a list of defaults for database initialization"""
        return [
            AttributeFields.VALUE,
            AttributeFields.SID,
            AttributeFields.SOURCE,
            AttributeFields.ID_TYPE,
            AttributeFields.ID_SEED,
            AttributeFields.NAME
        ]

class ApplicationDefaults:
    """Enumeration of default application settings"""

    # ENTITIES_SRC = Setting('ee_source','Entities Source', AppConfig.ENTITIES_SRC, False, False)
    # SYNTHESYS_HOST = Setting('synthesys_host','Synthesys Host', AppConfig.SYNTHESYS_HOST, True, False)
    # SYNTHESYS_PORT = Setting('synthesys_port','Synthesys Port', AppConfig.SYNTHESYS_PORT, True, False)
    # SYNTHESYS_SSL = Setting('synthesys_ssl', 'Synthesys SSL', AppConfig.SYNTHESYS_SSL, False, False)
    # SYNTHESYS_USER = Setting('synthesys_user', 'Synthesys User', AppConfig.SYNTHESYS_USER, True, False)
    # SYNTHESYS_PASS = Setting('synthesys_pass', 'Synthesys Pass', AppConfig.SYNTHESYS_PASS, True, True)
    #
    # @staticmethod
    # def list():
    #     """Return a list of defaults for database initialization"""
    #     return [
    #         ApplicationDefaults.ENTITIES_SRC,
    #         ApplicationDefaults.SYNTHESYS_HOST,
    #         ApplicationDefaults.SYNTHESYS_PORT,
    #         ApplicationDefaults.SYNTHESYS_SSL,
    #         ApplicationDefaults.SYNTHESYS_USER,
    #         ApplicationDefaults.SYNTHESYS_PASS
    #     ]

    @staticmethod
    def list():
        return []