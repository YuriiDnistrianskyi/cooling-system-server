from app.db.database import User
from app.dao.general_dao import GeneralDao

class UserDao(GeneralDao):
    _class_type = User
