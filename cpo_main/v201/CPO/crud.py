from sqlalchemy.orm import Session
from v16.CPO import schemas
from database import models
from datetime import datetime
from database.database import SessionLocal

db = SessionLocal()

async def get_charge_point(db: Session, charge_point_id: str):
    return db.query(models.ChargePoint201).filter(models.ChargePoint201.charge_point_id == charge_point_id).first()

async def get_charge_point_sessions(db: Session, charge_point_id: str):
    return db.query(models.ChargePointSessions201).filter(models.ChargePointSessions201.charge_point_id == charge_point_id).all()

async def get_charge_point_sessions_connector(db: Session, charge_point_id: str, connector_id: int = None):
    return db.query(models.ChargePointSessions201).filter(models.ChargePointSessions201.charge_point_id == charge_point_id,
        models.ChargePointSessions.connector_id == connector_id).all()

async def get_charge_point_session(db: Session, charge_point_id: str, transaction_id):
    return db.query(models.ChargePointSessions2).filter(models.ChargePointSessions201.charge_point_id == charge_point_id, 
        models.ChargePointSessions.transaction_id == transaction_id).first()

async def get_status(db: Session, charge_point_id: str):
    return db.query(models.ChargePointStatus201).filter(models.ChargePointStatus201.charge_point_id == charge_point_id).first()

async def meter_value_db(charge_point_id: str, connector_id: int, meter_value: list, transaction_id: int = None):
    for list in meter_value:
        timestamp = list['timestamp']
        timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
        sampled_value = list['sampled_value']
        for sample in sampled_value:
            current_measure = db.query(models.MeterValues201).filter_by(measurand=sample['measurand']).first()
            if not current_measure:
                meter = models.MeterValues201(
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
                meter = db.query(models.MeterValues201).filter(models.MeterValues201.transaction_id == transaction_id, models.MeterValues201.measurand == 
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
    new_status = models.ChargePointStatus201(
        charge_point_id=charge_point_id,
        connector_id=connector_id, 
        error_code= error_code,
        status = status, 
        status_timestamp=timestamp, 
        info=info, 
        vendor_id = vendor_id, 
        vendor_error_code = vendor_error_code
        )
    active_cp = db.query(models.ChargePointStatus201).filter(models.ChargePointStatus201.charge_point_id == charge_point_id).all()
    if not active_cp:
        db.add(new_status)
        db.commit()
        db.refresh(new_status)
        return new_status
    else:
        updated_status = db.query(models.ChargePointStatus201).filter(models.ChargePointStatus201.charge_point_id == charge_point_id).update({
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
    boot = models.ChargePoint201(
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
    active_cp = db.query(models.ChargePoint201).filter(models.ChargePoint201.charge_point_id == charge_point_id).all()
    if not active_cp:
        db.add(boot)
        db.commit()
        db.refresh(boot)
        return boot
    else:
        updated_boot = db.query(models.ChargePoint201).filter(models.ChargePoint201.charge_point_id == charge_point_id).update({
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
    heartbeat = db.query(models.ChargePoint201).filter(models.ChargePoint201.charge_point_id == charge_point_id).update({'heartbeat': timestamp})
    db.commit()
    return heartbeat

async def transaction_db(charge_point_id: str, connector_id: int, id_tag: str, meter_start:int, timestamp:str, reservation_id: str= None):
    transaction = models.ChargePointSessions(
        charge_point_id=charge_point_id,
        connector_id=connector_id,
        id_tag=id_tag,
        meter_start=meter_start,
        timestamp=timestamp,
        reservation_id=reservation_id
    )
    active_transaction = db.query(models.ChargePointSessions201).filter(models.ChargePointSessions201.charge_point_id == charge_point_id).all()
    if not active_transaction:
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction
    else:
        updated_transaction = db.query(models.ChargePointSessions201).filter(models.ChargePointSessions201.charge_point_id == charge_point_id).update({
            "charge_point_id":charge_point_id,
            "id_tag":id_tag,
            "meter_start":meter_start,
            "timestamp":timestamp,
            "reservation_id":reservation_id
        })
        db.commit()
        return updated_transaction

async def stop_transaction_db(charge_point_id:str, transaction_id: int, id_tag: str, meter_stop:int, timestamp:str, reason:str, transaction_data:list):
    pass