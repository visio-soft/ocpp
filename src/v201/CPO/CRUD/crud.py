from sqlalchemy.orm import Session
from resources.database import SessionLocal
from resources import models
from datetime import datetime

db = SessionLocal()

async def get_charge_point(db: Session, charge_point_id: str):
    return db.query(models.ChargePoint201).filter(models.ChargePoint201.charge_point_id == charge_point_id).first()

async def get_all_charge_points(db: Session):
    return db.query(models.ChargePoint201).all()

async def get_charge_point_sessions(db: Session, charge_point_id: str):
    return db.query(models.ChargePointSessions201).filter(models.ChargePointSessions201.charge_point_id == charge_point_id).all()

async def get_charge_point_sessions_connector(db: Session, charge_point_id: str, connector_id: int = None):
    return db.query(models.ChargePointSessions201).filter(models.ChargePointSessions201.charge_point_id == charge_point_id,
        models.ChargePointSessions201.connector_id == connector_id).all()

async def get_all_charge_point_session_id(db: Session, charge_point_id: str, id_tag: str):
    return db.query(models.ChargePointSessions201).filter(models.ChargePointSessions201.charge_point_id == charge_point_id, 
        models.ChargePointSessions201.id_tag == id_tag).all()

async def get_charge_point_session_id(db: Session, charge_point_id: str, id_tag: str, transaction_id: int):
    return db.query(models.ChargePointSessions201).filter(models.ChargePointSessions201.charge_point_id == charge_point_id, 
        models.ChargePointSessions201.id_tag == id_tag, models.ChargePointSessions201.transaction_id == transaction_id).first()

async def get_ongoing_charge_point_session(db: Session, charge_point_id: str, transaction_id):
    return db.query(models.ChargePointSessions201).filter(models.ChargePointSessions201.charge_point_id == charge_point_id, 
        models.ChargePointSessions201.transaction_id == transaction_id).first()

async def start_check_ongoing_charging_session(db: Session, charge_point_id: str, id_tag: str):
    return db.query(models.ChargePointSessions201).filter_by(id_tag=id_tag, charge_point_id=charge_point_id).first()

async def stop_check_ongoing_charging_session(db: Session, charge_point_id: str, transaction_id: int):
    return db.query(models.ChargePointSessions201).filter_by(transaction_id=transaction_id, charge_point_id=charge_point_id).first()

async def get_status(db: Session, charge_point_id: str):
    return db.query(models.ChargePointStatus201).filter(models.ChargePointStatus201.charge_point_id == charge_point_id).first()

async def meter_value_db(charge_point_id: str, meter_value: list, transaction_info: dict = None):
    for list in meter_value:
        timestamp = list['timestamp']
        timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
        sampled_value = list['sampled_value']
        for sample in sampled_value:
            if sample['unit_of_measure']:
                unit_of_measure=sample['unit_of_measure']
                unit=unit_of_measure['unit']
                multiplier=unit_of_measure['multiplier']
            if sample['signed_meter_value']:
                signed_data=sample['signed_meter_value']
                signed_meter_data=signed_data['signed_meter_data']
                signing_method=signed_data['signing_method']
                encoding_method=signed_data['encoding_method']
                public_key=signed_data['public_key']
            current_measure = db.query(models.MeterValues201).filter_by(measurand=sample['measurand']).first()
            if not current_measure:
                meter = models.MeterValues201(
                    transaction_id=transaction_info['transaction_id'],
                    charge_point_id=charge_point_id,
                    timestamp=timestamp,  
                    measurand=sample['measurand'], 
                    value=sample['value'], 
                    context=sample['context'], 
                    phase=sample['phase'], 
                    location=sample['location'],
                    signed_meter_data=signed_meter_data,
                    signing_method=signing_method,
                    encoding_method=encoding_method,
                    public_key=public_key,
                    unit=unit,
                    multiplier=multiplier
                    )
                db.add(meter)
                db.commit()
                db.refresh(meter)
            else:
                meter = db.query(models.MeterValues201).filter(models.MeterValues201.transaction_id == transaction_info['transaction_id'],
                models.MeterValues201.measurand == sample['measurand']).update({
                    "transaction_id":transaction_info['transaction_id'],
                    "charge_point_id":charge_point_id,
                    "timestamp":timestamp,  
                    "measurand":sample['measurand'], 
                    "value":sample['value'], 
                    "context":sample['context'],
                    "phase":sample['phase'], 
                    "location":sample['location'], 
                    "signed_meter_data":signed_meter_data,
                    "signing_method":signing_method,
                    "encoding_method":encoding_method,
                    "public_key":public_key,
                    "unit":unit,
                    "multiplier":multiplier
                })
                db.commit()
    return meter
    
async def status_db(charge_point_id: str, connector_id: int, error_code: str, status: str, timestamp: str = None, info: str = None,
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

async def boot_notification_db(charge_point_id: str, charging_station: dict, reason: str):
    modem=charging_station['modem']
    boot = models.ChargePoint201(
        charge_point_id=charge_point_id,
        charge_point_vendor=charging_station['vendor_name'],
        charge_point_model=charging_station['model'], 
        charge_point_serial_number=charging_station['serial_number'],
        firmware_version=charging_station['firmware_version'],
        iccid=modem['iccid'],
        imsi =modem['imsi'],
        boot_reason=reason
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
        "charge_point_vendor":charging_station['vendor_name'],
        "charge_point_model":charging_station['model'], 
        "charge_point_serial_number":charging_station['serial_number'],
        "firmware_version":charging_station['firmware_version'],
        "iccid":modem['iccid'],
        "imsi":modem['imsi'],
        "boot_reason":reason
        })
        db.commit()
        return updated_boot

async def heartbeat_db(charge_point_id, timestamp):
    heartbeat = db.query(models.ChargePoint201).filter(models.ChargePoint201.charge_point_id == charge_point_id).update({'heartbeat': timestamp})
    db.commit()
    return heartbeat

async def transaction_db(charge_point_id: str, event_type: str, timestamp: str, trigger_reason: str, seq_no: int, 
        transaction_info: dict, offline: bool = None, number_of_phases_used: int = None,
        cable_max_current: int = None, reservation_id: int = None, evse: dict = None, id_token: dict = None):
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
    active_transaction = db.query(models.ChargePointSessions201).filter(models.ChargePointSessions201.charge_point_id == charge_point_id, 
        models.ChargePointSessions201.id_token == id_token['id_token'], models.ChargePointSessions201.transaction_id == transaction_info['transaction_id'], 
        models.ChargePointSessions201.remote_start_id == transaction_info['remote_start_id']).all()
    if not active_transaction:
        transaction = models.ChargePointSessions201(
            charge_point_id=charge_point_id,
            event_type=event_type, 
            timestamp=timestamp, 
            trigger_reason=trigger_reason,
            seq_no=seq_no,
            transaction_id=transaction_info['transaction_id'],
            charging_state=transaction_info['charging_state'],
            time_spent_charging=transaction_info['time_spent_charging'],
            stopped_reason=transaction_info['stopped_reason'],
            remote_start_id=transaction_info['remote_start_id'],
            offline=offline,
            number_of_phases_used=number_of_phases_used,
            cable_max_current=cable_max_current, 
            reservation_id=reservation_id, 
            evse_id=evse['id'],
            connector_id=evse['connector_id'],
            id_token=id_token['id_token'],
            type=id_token['type']
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
    else:
        transaction = db.query(models.ChargePointSessions201).filter(models.ChargePointSessions201.charge_point_id == charge_point_id, 
            models.ChargePointSessions201.id_token == id_token['id_token'],
            models.ChargePointSessions201.transaction_id == transaction_info['transaction_id']).update({
            'charge_point_id':charge_point_id,
            'event_type':event_type, 
            'timestamp':timestamp, 
            'trigger_reason':trigger_reason,
            'seq_no':seq_no,
            'transaction_id':transaction_info['transaction_id'],
            'charging_state':transaction_info['charging_state'],
            'time_spent_charging':transaction_info['time_spent_charging'],
            'stopped_reason':transaction_info['stopped_reason'],
            'remote_start_id':transaction_info['remote_start_id'],
            'offline':offline,
            'number_of_phases_used':number_of_phases_used,
            'cable_max_current':cable_max_current, 
            'reservation_id':reservation_id, 
            'evse_id':evse['id'],
            'connector_id':evse['connector_id'],
            'id_token':id_token['id_token'],
            'type':id_token['type']
        })
        db.commit()
    return transaction