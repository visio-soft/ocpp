from sqlalchemy import Column, Integer, String, Boolean, DateTime
from ocpp import charge_point
from resources.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)

class Token(Base):
    __tablename__ = "token"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password = Column(String)
    token = Column(String)

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
    id = Column(Integer, primary_key=True, index = True)
    id_tag= Column(String)
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
    timestamp = Column(DateTime)
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

class LocalList(Base):
    __tablename__ = "local_list_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    list_version = Column(Integer)
    id_tag = Column(String)
    expiry_date = Column(DateTime)
    parent_id_tag = Column(String)
    status = Column(String)
    update_type = Column(String)

"""
OCPP version 2.0.1 models
"""
class ChargePoint201(Base):
    __tablename__ = "charge_point_201"
    charge_point_id = Column(String, primary_key=True, index=True)
    charge_point_vendor = Column(String)
    charge_point_model = Column(String)
    charge_point_serial_number = Column(String)
    firmware_version = Column(String)
    iccid = Column(String)
    imsi = Column(String)
    boot_reason = Column(String)
    heartbeat = Column(DateTime)

class ChargePointSessions201(Base):
    __tablename__ = "charging_session_201"
    id = Column(Integer, primary_key = True, index = True)
    id_token = Column(String)
    charge_point_id = Column(String)
    event_type = Column(String)
    timestamp = Column(DateTime)
    trigger_reason = Column(String)
    seq_no = Column(Integer)
    transaction_id = Column(String)
    charging_state = Column(String)
    time_spent_charging = Column(Integer)
    stopped_reason = Column(String)
    remote_start_id = Column(Integer)
    offline = Column(Boolean)
    number_of_phases_used = Column(Integer)
    cable_max_current = Column(String)
    reservation_id = Column(String)
    evse_id = Column(Integer)
    connector_id = Column(Integer)
    type = Column(String)

class ChargePointStatus201(Base):
    __tablename__ = "charge_point_status_201"
    charge_point_id = Column(String, primary_key=True, index=True)
    connector_id = Column(Integer)
    status = Column(String)
    error_code = Column(String)
    status_timestamp = Column(DateTime)
    info = Column(String)
    vendor_id = Column(String)
    vendor_error_code = Column(String)
    

class MeterValues201(Base):
    __tablename__ = "meter_values_201"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer)
    charge_point_id= Column(String)
    connector_id= Column(Integer)
    timestamp = Column(DateTime)
    measurand = Column(String) 
    value = Column(String)
    context = Column(String)
    phase = Column(String)
    location = Column(String)
    signed_meter_data = Column(String)
    signing_method = Column(String)
    encoding_method = Column(String)
    public_key = Column(String)
    unit = Column(String)
    multiplier = Column(Integer)