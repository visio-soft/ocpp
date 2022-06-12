from sqlalchemy.orm import Session
from resources.database import SessionLocal
from resources import models
from datetime import datetime

db = SessionLocal()

async def get_charge_point(db: Session, charge_point_id: str):
    return db.query(models.ChargePoint16).filter(models.ChargePoint16.charge_point_id == charge_point_id).first()

async def get_all_charge_points(db: Session):
    return db.query(models.ChargePoint16).all()

async def get_charge_point_sessions(db: Session, charge_point_id: str):
    return db.query(models.PastChargePointSessions16).filter(models.PastChargePointSessions16.charge_point_id == charge_point_id).all()

async def get_charge_point_sessions_connector(db: Session, charge_point_id: str, connector_id: int = None):
    return db.query(models.OngoingChargePointSessions16).filter(models.OngoingChargePointSessions16.charge_point_id == charge_point_id,
        models.OngoingChargePointSessions16.connector_id == connector_id).all()

async def get_all_charge_point_session_id(db: Session, charge_point_id: str, id_tag: str):
    return db.query(models.PastChargePointSessions16).filter(models.PastChargePointSessions16.charge_point_id == charge_point_id, 
        models.PastChargePointSessions16.id_tag == id_tag).all()

async def get_charge_point_session_id(db: Session, charge_point_id: str, id_tag: str, transaction_id: int):
    return db.query(models.PastChargePointSessions16).filter(models.PastChargePointSessions16.charge_point_id == charge_point_id, 
        models.PastChargePointSessions16.id_tag == id_tag, models.PastChargePointSessions16.transaction_id == transaction_id).first()

async def get_ongoing_charge_point_session(db: Session, charge_point_id: str, transaction_id):
    return db.query(models.OngoingChargePointSessions16).filter(models.OngoingChargePointSessions16.charge_point_id == charge_point_id, 
        models.OngoingChargePointSessions16.transaction_id == transaction_id).first()

async def start_check_ongoing_charging_session(db: Session, charge_point_id: str, id_tag: str):
    return db.query(models.OngoingChargePointSessions16).filter_by(id_tag=id_tag, charge_point_id=charge_point_id).first()

async def stop_check_ongoing_charging_session(db: Session, charge_point_id: str, transaction_id: int):
    return db.query(models.OngoingChargePointSessions16).filter_by(transaction_id=transaction_id, charge_point_id=charge_point_id).first()

async def get_status(db: Session, charge_point_id: str):
    return db.query(models.ChargePointStatus16).filter(models.ChargePointStatus16.charge_point_id == charge_point_id).first()

async def send_local_list(db: Session, charge_point_id: str, list_version: int, update_type: str, local_authorization_list: list):
    for list in local_authorization_list:
        id_tag=list.id_tag
        id_exist = db.query(models.LocalList).filter_by(id_tag = id_tag)
        if list.id_tag_info:
            id_tag_info=list.id_tag_info
            expiry_date = id_tag_info.expiry_date
            expiry_date = datetime.strptime(expiry_date, '%Y-%m-%dT%H:%M:%S.%f')
            parent_id_tag = id_tag_info.parent_id_tag
            status = id_tag_info.status
        if not id_exist:
            local_list = models.LocalList(
                charge_point_id=charge_point_id,
                list_version=list_version,
                id_tag = id_tag,
                expiry_date=expiry_date,
                parent_id_tag=parent_id_tag,
                status=status,
                update_type=update_type,
            )
            db.add(local_list)
            db.commit()
            db.refresh(local_list)
        else:
            local_list = db.query(models.LocalList).filter(models.LocalList.id_tag == id_tag, models.LocalList.list_version == list_version).update({
                    "charge_point_id":charge_point_id,
                    "list_version":list_version,
                    "id_tag":id_tag,
                    "expiry_date":expiry_date,
                    "parent_id_tag":parent_id_tag,
                    "status":status,
                    "update_type":update_type,
                })
            db.commit()
    return

async def get_local_list(db: Session, charge_point_id: str, list_version: int):
    return db.query(models.LocalList).filter_by(charge_point_id=charge_point_id, list_version=list_version).all()

async def meter_value_db(charge_point_id: str, connector_id: int, meter_value: list, transaction_id: int = None):
    for list in meter_value:
        timestamp = list['timestamp']
        timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
        sampled_value = list['sampled_value']
        for sample in sampled_value:
            current_measure = db.query(models.MeterValues16).filter_by(measurand=sample['measurand']).first()
            if not current_measure:
                meter = models.MeterValues16(
                    transaction_id=transaction_id,
                    charge_point_id=charge_point_id,
                    timestamp=timestamp, 
                    connector_id=connector_id,  
                    measurand=sample['measurand'], 
                    value=sample['value'], 
                    context=sample['context'], 
                    format=sample['format'], 
                    phase=sample['phase'], 
                    location=sample['location'], 
                    unit=sample['unit']
                    )
                db.add(meter)
                db.commit()
                db.refresh(meter)
            else:
                meter = db.query(models.MeterValues16).filter(models.MeterValues16.transaction_id == transaction_id, models.MeterValues16.measurand == 
                sample['measurand']).update({
                    "transaction_id":transaction_id,
                    "charge_point_id":charge_point_id,
                    "timestamp":timestamp, 
                    "connector_id":connector_id,  
                    "measurand":sample['measurand'], 
                    "value":sample['value'], 
                    "context":sample['context'], 
                    "format":sample['format'], 
                    "phase":sample['phase'], 
                    "location":sample['location'], 
                    "unit":sample['unit']
                })
                db.commit()
    return meter
    
async def status_db(charge_point_id, connector_id: int, error_code: str, status: str, timestamp: str = None, info: str = None,
    vendor_id: str = None, vendor_error_code: str = None):
    new_status = models.ChargePointStatus16(
        charge_point_id=charge_point_id,
        connector_id=connector_id, 
        error_code= error_code,
        status = status, 
        status_timestamp=timestamp, 
        info=info, 
        vendor_id = vendor_id, 
        vendor_error_code = vendor_error_code
        )
    active_cp = db.query(models.ChargePointStatus16).filter(models.ChargePointStatus16.charge_point_id == charge_point_id).all()
    if not active_cp:
        db.add(new_status)
        db.commit()
        db.refresh(new_status)
        return new_status
    else:
        updated_status = db.query(models.ChargePointStatus16).filter(models.ChargePointStatus16.charge_point_id == charge_point_id).update({
        "charge_point_id":charge_point_id,
        "connector_id":connector_id, 
        "error_code": error_code,
        "status": status, 
        "status_timestamp":timestamp, 
        "info":info,
        "vendor_id": vendor_id, 
        "vendor_error_code": vendor_error_code
        })
        db.commit()
        return updated_status

async def boot_notification_db(charge_point_id: str, charge_point_vendor: str, charge_point_model: str, 
charge_point_serial_number: str = None, firmware_version: str = None, charge_box_serial_number: str = None, iccid: str = None, 
imsi: str = None, meter_serial_number: str = None, meter_type: str = None):
    boot = models.ChargePoint16(
        charge_point_id=charge_point_id,
        charge_point_vendor=charge_point_vendor,
        charge_point_model=charge_point_model, 
        charge_point_serial_number=charge_point_serial_number,
        firmware_version=firmware_version,
        charge_box_serial_number=charge_box_serial_number,
        iccid=iccid,
        imsi =imsi, 
        meter_serial_number = meter_serial_number, 
        meter_type = meter_type
        )
    active_cp = db.query(models.ChargePoint16).filter(models.ChargePoint16.charge_point_id == charge_point_id).all()
    if not active_cp:
        db.add(boot)
        db.commit()
        db.refresh(boot)
        return boot
    else:
        updated_boot = db.query(models.ChargePoint16).filter(models.ChargePoint16.charge_point_id == charge_point_id).update({
        "charge_point_id":charge_point_id,
        "charge_point_vendor":charge_point_vendor,
        "charge_point_model":charge_point_model, 
        "charge_point_serial_number":charge_point_serial_number,
        "firmware_version":firmware_version,
        "charge_box_serial_number":charge_box_serial_number,
        "iccid":iccid,
        "imsi":imsi, 
        "meter_serial_number": meter_serial_number, 
        "meter_type": meter_type
        })
        db.commit()
        return updated_boot

async def heartbeat_db(charge_point_id, timestamp):
    heartbeat = db.query(models.ChargePoint16).filter(models.ChargePoint16.charge_point_id == charge_point_id).update({'heartbeat': timestamp})
    db.commit()
    return heartbeat

async def transaction_db(charge_point_id: str, transaction_id: int, connector_id: int, id_tag: str, meter_start:int, timestamp:str, 
    reservation_id: str= None):
    transaction = models.OngoingChargePointSessions16(
        charge_point_id=charge_point_id,
        transaction_id=transaction_id,
        connector_id=connector_id,
        id_tag=id_tag,
        meter_start=meter_start,
        timestamp=timestamp,
        reservation_id=reservation_id
    )
    active_transaction = db.query(models.OngoingChargePointSessions16).filter(models.OngoingChargePointSessions16.charge_point_id == charge_point_id, 
        models.OngoingChargePointSessions16.connector_id == connector_id, models.OngoingChargePointSessions16.id_tag == id_tag, 
            models.OngoingChargePointSessions16.transaction_id == transaction_id).all()
    if not active_transaction:
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction
    else:
        return(f"Transaction already started.")

async def stop_transaction_db(charge_point_id:str, transaction_id: int, id_tag: str, meter_stop:int, timestamp:str, reason:str, transaction_data:list):
    for list in transaction_data:
        timestamp = list['timestamp']
        timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
        sampled_value = list['sampled_value']
        for sample in sampled_value:
            current_measure = db.query(models.PastChargePointSessions16).filter_by(transaction_id=transaction_id,measurand=sample['measurand']).first()
            if not current_measure:
                transaction = models.PastChargePointSessions16(
                    charge_point_id=charge_point_id,
                    transaction_id=transaction_id,
                    id_tag=id_tag,
                    meter_stop=meter_stop,
                    timestamp=timestamp,
                    reason=reason,  
                    measurand=sample['measurand'], 
                    value=sample['value'], 
                    context=sample['context'], 
                    format=sample['format'], 
                    phase=sample['phase'], 
                    location=sample['location'], 
                    unit=sample['unit']
                    )
                db.add(transaction)
                db.commit()
                db.refresh(transaction)
            else:
                transaction = db.query(models.PastChargePointSessions16).filter(models.PastChargePointSessions16.transaction_id == transaction_id, 
                    models.PastChargePointSessions16.measurand == sample['measurand']).update({
                    "charge_point_id":charge_point_id,
                    "transaction_id":transaction_id,
                    "id_tag":id_tag,
                    "meter_stop":meter_stop,
                    "timestamp":timestamp,
                    "reason":reason,
                    "timestamp":timestamp,   
                    "measurand":sample['measurand'], 
                    "value":sample['value'], 
                    "context":sample['context'], 
                    "format":sample['format'], 
                    "phase":sample['phase'], 
                    "location":sample['location'], 
                    "unit":sample['unit']
                })
                db.commit()
    return transaction
                