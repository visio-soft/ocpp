from sqlalchemy import Column, Integer, String, Boolean, DateTime
from resources.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    mobile = Column(String)
    password = Column(String)

class Token(Base):
    __tablename__ = "token"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    token = Column(String)

class RfidTag(Base):
    __tablename__ = "rfid_tag"
    rfid = Column(String, primary_key=True)
    active = Column(Boolean)
    rfid_length = Column(Integer)

"""
OCPP version 1.6 models
"""
class ChargePoint16(Base):
    __tablename__ = "charge_point_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    charge_point_vendor = Column(String)
    charge_point_model = Column(String)
    charge_point_serial_number = Column(String)
    firmware_version = Column(String)
    charge_box_serial_number = Column(String)
    iccid = Column(String)
    imsi = Column(String)
    meter_serial_number = Column(String)
    meter_type = Column(String)
    heartbeat = Column(DateTime)

class OngoingChargePointSessions16(Base):
    __tablename__ = "charging_session_16"
    id_tag= Column(String, primary_key=True)
    transaction_id = Column(Integer)
    charge_point_id= Column(String)
    connector_id = Column(Integer)
    meter_start = Column(Integer)
    timestamp = Column(DateTime)
    reservation_id = Column(String)


class PastChargePointSessions16(Base):
    __tablename__ = "past_sessions_16"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer)
    id_tag = Column(String)
    charge_point_id = Column(String)
    meter_stop = Column(Integer)
    timestamp = Column(DateTime)
    reason = Column(String)
    measurand = Column(String) 
    value = Column(String)
    context = Column(String)
    format = Column(String)
    phase = Column(String)
    location = Column(String)
    unit = Column(String)

class ChargePointStatus16(Base):
    __tablename__ = "charge_point_status_16"
    charge_point_id = Column(String, primary_key=True, index=True)
    connector_id = Column(Integer)
    status = Column(String)
    error_code = Column(String)
    status_timestamp = Column(DateTime)
    info = Column(String)
    vendor_id = Column(String)
    vendor_error_code = Column(String)

class MeterValues16(Base):
    __tablename__ = "meter_values_16"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer)
    charge_point_id= Column(String)
    connector_id= Column(Integer)
    timestamp = Column(DateTime)
    measurand = Column(String) 
    value = Column(String)
    context = Column(String)
    format = Column(String)
    phase = Column(String)
    location = Column(String)
    unit = Column(String)

class Schedule16(Base):
    __tablename__ = "schedule_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id= Column(String)
    name= Column(String)
    active= Column(Boolean)
    start_hours= Column(Integer)
    start_minutes= Column(Integer)
    end_hours= Column(Integer)
    end_minutes= Column(Integer)
    time_zone= Column(String)
    monday= Column(Boolean)
    tuesday= Column(Boolean)
    wednesday= Column(Boolean)
    thursday= Column(Boolean)
    friday= Column(Boolean)
    saturday= Column(Boolean)
    sunday= Column(Boolean)
    connector_id_list= Column(String)


# """
# OCPP version 2.0.1 models
# """

# class ChargePoint201(Base):
#     __tablename__ = "charge_point_201"
#     id = Column(Integer, primary_key=True, index=True)
#     charge_point_id = Column(String)
#     charge_point_vendor = Column(String)
#     charge_point_model = Column(String)
#     charge_point_serial_number = Column(String)
#     firmware_version = Column(String)
#     charge_box_serial_number = Column(String)
#     iccid = Column(String)
#     imsi = Column(String)
#     meter_serial_number = Column(String)
#     meter_type = Column(String)
#     heartbeat = Column(DateTime)

# class ChargePointSessions201(Base):
#     __tablename__ = "charging_session_201"
#     transaction_id = Column(Integer, primary_key=True, index=True)
#     charge_point_id= Column(String)
#     connector_id = Column(Integer)
#     id_tag= Column(String)
#     meter_start = Column(Integer)
#     timestamp = Column(DateTime)
#     reservation_id = Column(String)

# class PastChargePointSessions201(Base):
#     __tablename__ = "past_sessions_201"
#     id = Column(Integer, primary_key=True, index=True)
#     transaction_id = Column(Integer)
#     charge_point_id = Column(String)
#     id_tag = Column(String)
#     meter_stop = Column(Integer)
#     timestamp = Column(DateTime)
#     reason = Column(String)


# class ChargePointStatus201(Base):
#     __tablename__ = "charge_point_status_201"
#     charge_point_id = Column(String, primary_key=True, index=True)
#     connector_id = Column(Integer)
#     status = Column(String)
#     error_code = Column(String)
#     status_timestamp = Column(DateTime)
#     info = Column(String)
#     vendor_id = Column(String)
#     vendor_error_code = Column(String)
    

# class MeterValues201(Base):
#     __tablename__ = "meter_values_201"
#     id = Column(Integer, primary_key=True, index=True)
#     transaction_id = Column(Integer)
#     charge_point_id= Column(String)
#     connector_id= Column(Integer)
#     timestamp = Column(DateTime)
#     measurand = Column(String) 
#     value = Column(String)
#     context = Column(String)
#     format = Column(String)
#     phase = Column(String)
#     location = Column(String)
#     unit = Column(String)

# class Schedule201(Base):
#     __tablename__ = "schedule_201"
#     id = Column(Integer, primary_key=True, index=True)
#     charge_point_id= Column(String)
#     name= Column(String)
#     active= Column(Boolean)
#     start_hours= Column(Integer)
#     start_minutes= Column(Integer)
#     end_hours= Column(Integer)
#     end_minutes= Column(Integer)
#     time_zone= Column(String)
#     monday= Column(Boolean)
#     tuesday= Column(Boolean)
#     wednesday= Column(Boolean)
#     thursday= Column(Boolean)
#     friday= Column(Boolean)
#     saturday= Column(Boolean)
#     sunday= Column(Boolean)
#     connector_id_list= Column(String)