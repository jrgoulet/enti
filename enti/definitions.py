from enti.models import AttributeType

class TypeEnum:

    @staticmethod
    def list():
        pass


class AttributeTypeEnum(TypeEnum):

    INTEGER = AttributeType("integer", "Integer")
    ENTITY = AttributeType("entity", "Entity")
    NAMED_REF = AttributeType("named-reference", "Named Reference")
    DATE = AttributeType("date", "Date")
    STRING = AttributeType("string", "String")

    @staticmethod
    def list():
        return [
            AttributeTypeEnum.INTEGER,
            AttributeTypeEnum.ENTITY,
            AttributeTypeEnum.NAMED_REF,

        ]



