from app.db.database import Object
from app.dao.general_dao import GeneralDao

class ObjectDao(GeneralDao[Object]):
    _class_type = Object
