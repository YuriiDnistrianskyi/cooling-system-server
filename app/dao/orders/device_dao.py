from app.db.database import Device
from app.dao.general_dao import GeneralDao

class DeviceDao(GeneralDao[Device]):
    _class_type = Device
