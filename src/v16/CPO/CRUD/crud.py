from resources.database import SessionLocal
from resources import models
from datetime import datetime

db = SessionLocal()

#Done -Fixa if-satser för alla möjliga scenarion
async def send_local_list(charge_point_id: str, list_version: int, update_type: str,
    response_status:str, local_authorization_list: list = None):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    if not local_authorization_list:
        local_list = models.LocalList16(
            charge_point_id=charge_point_id,
            timestamp=timestamp,
            list_version=list_version,
            update_type=update_type,
            response_status=response_status
        )
        db.add(local_list)
        db.commit()
        db.refresh(local_list)
    else:
        for list in local_authorization_list:
            id_tag=list.id_tag
            if list.id_tag_info:
                id_tag_info=list.id_tag_info
                if not id_tag_info.expiry_date:
                    if not id_tag_info.parent_id_tag:
                        status = id_tag_info.status
                        local_list = models.LocalList16(
                            charge_point_id=charge_point_id,
                            timestamp=timestamp,
                            list_version=list_version,
                            id_tag = id_tag,
                            authorization_status=status,
                            update_type=update_type,
                            response_status=response_status
                        )
                        db.add(local_list)
                        db.commit()
                        db.refresh(local_list)

                #Kanske behöer if parent_id_tag
                
                else:    
                    expiry_date = datetime.strptime(id_tag_info.expiry_date, '%Y-%m-%dT%H:%M:%SZ')
                    status = id_tag_info.status
                    local_list = models.LocalList16(
                        charge_point_id=charge_point_id,
                        timestamp=timestamp,
                        list_version=list_version,
                        id_tag = id_tag,
                        expiry_date=expiry_date,
                        parent_id_tag=id_tag_info.parent_id_tag,
                        authorization_status=status,
                        update_type=update_type,
                        response_status=response_status
                    )
                    db.add(local_list)
                    db.commit()
                    db.refresh(local_list)
    return local_list

#Done - Behöver testas vid laddning
async def meter_value_db(charge_point_id: str, connector_id: int, meter_value: list, transaction_id: int = None):
    if not meter_value:
        return
    else:
        for list in meter_value:
            timestamp = list['timestamp']
            timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
            sampled_value = list['sampled_value']
            if sampled_value:
                for sample in sampled_value:
                    current_measure = db.query(models.MeterValues16).filter_by(measurand=sample['measurand'], transaction_id=transaction_id).first()
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
    
#Done - Tested
async def status_db(charge_point_id:str, connector_id: int, timestamp:str, error_code: str, status: str, info: str = None,
    vendor_id: str = None, vendor_error_code: str = None):
    timestamp=datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    status_notification = models.ChargePointStatus16(
        charge_point_id=charge_point_id,
        timestamp=timestamp,
        connector_id=connector_id, 
        status = status,
        error_code= error_code,
        info=info, 
        vendor_id = vendor_id, 
        vendor_error_code = vendor_error_code
    )
    db.add(status_notification)
    db.commit()
    db.refresh(status_notification)
    return status_notification

#Done - Tested
async def boot_notification_db(charge_point_id: str, charge_point_vendor: str, boot_timestamp:str, charge_point_model: str, heartbeat_interval:int, status:str, 
    charge_point_serial_number: str = None, firmware_version: str = None, charge_box_serial_number: str = None, iccid: str = None, 
    imsi: str = None, meter_serial_number: str = None, meter_type: str = None):
    boot_timestamp = datetime.strptime(boot_timestamp, '%Y-%m-%dT%H:%M:%S.%f')
    boot = models.ChargePoint16(
        charge_point_id=charge_point_id,
        boot_timestamp = boot_timestamp,
        charge_point_vendor=charge_point_vendor,
        charge_point_model=charge_point_model, 
        charge_point_serial_number=charge_point_serial_number,
        firmware_version=firmware_version,
        charge_box_serial_number=charge_box_serial_number,
        iccid=iccid,
        imsi =imsi, 
        meter_serial_number = meter_serial_number, 
        meter_type = meter_type,
        heartbeat_interval=heartbeat_interval,
        status=status
        )
    db.add(boot)
    db.commit()
    db.refresh(boot)
    return boot

#Done - Tested
async def heartbeat_db(charge_point_id, timestamp):
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
    heartbeat = models.Heartbeat16(charge_point_id=charge_point_id,timestamp=timestamp)
    db.add(heartbeat)
    db.commit()
    db.refresh(heartbeat)
    return heartbeat

#Done - Tested
async def start_transaction_db(charge_point_id: str, transaction_id: int, connector_id: int, id_tag: str, meter_start:int, timestamp:str, authorization_status:str, 
    reservation_id: str= None, parent_id_tag:str = None, expiry_date:str =None):
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    if expiry_date:
        expiry_date = datetime.strptime(expiry_date, '%Y-%m-%dT%H:%M:%SZ')
    transaction = models.StartTransaction16(
        charge_point_id=charge_point_id,
        timestamp=timestamp,
        id_tag=id_tag,
        transaction_id=transaction_id,
        connector_id=connector_id,
        meter_start=meter_start,
        reservation_id=reservation_id,
        expiry_date=expiry_date,
        parent_id_tag=parent_id_tag,
        authorization_status=authorization_status
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

#Done - Tested
async def stop_transaction_db(charge_point_id:str, transaction_id: int, id_tag: str, meter_stop:int, timestamp:str, reason:str, 
    authorization_status:str, transaction_data:list = None, expiry_date:str=None, parent_id_tag:str =None):
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    if expiry_date:
        expiry_date = datetime.strptime(expiry_date, '%Y-%m-%dT%H:%M:%S.%f')
    if not transaction_data:
        transaction = models.StopTransaction16(
            charge_point_id=charge_point_id,
            timestamp=timestamp,
            transaction_id=transaction_id,
            id_tag=id_tag,
            meter_stop=meter_stop,
            reason=reason,
            expiry_date=expiry_date,
            parent_id_tag=parent_id_tag,
            authorization_status=authorization_status
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
    else:
        for list in transaction_data:
            sampled_value = list['sampled_value']
            for sample in sampled_value:
                transaction = models.StopTransaction16(
                    charge_point_id=charge_point_id,
                    timestamp=timestamp,
                    transaction_id=transaction_id,
                    id_tag=id_tag,
                    meter_stop=meter_stop,
                    reason=reason,
                    expiry_date=expiry_date,
                    parent_id_tag=parent_id_tag,
                    authorization_status=authorization_status,
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
    return transaction
                
#Done - Tested
async def clear_cache_db(charge_point_id:str, response_status:str):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    clear_cache = models.ClearCache16(
        charge_point_id=charge_point_id,
        timestamp=timestamp,
        response_status=response_status
    )
    db.add(clear_cache)
    db.commit()
    db.refresh(clear_cache)
    return clear_cache

#Done - Behöver testas vid laddning
async def authorize_db(charge_point_id:str, id_tag:str, authorization_status:str, expiry_date:str=None, parent_id_tag:str=None):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    expiry_date=datetime.strptime(expiry_date, '%Y-%m-%dT%H:%M:%SZ')
    authorize = models.Authorize16(
        charge_point_id=charge_point_id,
        timestamp=timestamp,
        id_tag=id_tag,
        expiry_date=expiry_date,
        parent_id_tag=parent_id_tag,
        authorization_status=authorization_status
    )
    db.add(authorize)
    db.commit()
    db.refresh(authorize)
    return authorize

#Done - Tested
async def firmware_status_db(charge_point_id:str, status:str):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    firmware_status=models.FirmwareStatusNotification16(
        charge_point_id=charge_point_id,
        timestamp=timestamp,
        status=status
    )
    db.add(firmware_status)
    db.commit()
    db.refresh(firmware_status)
    return firmware_status

#Done - Tested
async def diagnostics_status_db(charge_point_id:str, status:str):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    diagnostics_status=models.DiagnosticsStatusNotification16(
        charge_point_id=charge_point_id,
        timestamp=timestamp,
        status=status
    )
    db.add(diagnostics_status)
    db.commit()
    db.refresh(diagnostics_status)
    return diagnostics_status

#Done - Tested
async def configure_db(charge_point_id:str, key:str, value:str, response_status:str):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    configure=models.Configuration16(
        charge_point_id=charge_point_id,
        timestamp=timestamp,
        key=key,
        value=value,
        response_status=response_status
    )
    db.add(configure)
    db.commit()
    db.refresh(configure)
    return configure

#Done - Tested
async def availability_db(charge_point_id:str, connector_id:int, type:str, response_status:str):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    availability=models.Availability16(
        charge_point_id=charge_point_id,
        timestamp=timestamp,
        connector_id=connector_id,
        type=type,
        response_status=response_status
    )
    db.add(availability)
    db.commit()
    db.refresh(availability)
    return availability

#Done - Tested
async def reservation_db(charge_point_id:str, connector_id:int,id_tag:str,reservation_id:int, response_status:str,
    expiry_date:str=None, parent_id_tag:str=None):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    expiry_date=datetime.strptime(expiry_date, '%Y-%m-%dT%H:%M:%S.%f')
    reserve=models.Reservation16(
        charge_point_id=charge_point_id,
        timestamp=timestamp,
        connector_id=connector_id,
        id_tag=id_tag,
        reservation_id=reservation_id,
        expiry_date=expiry_date,
        parent_id_tag=parent_id_tag,
        response_status=response_status
    )
    db.add(reserve)
    db.commit()
    db.refresh(reserve)
    return reserve

#Done - Tested
async def cancel_reservation_db(charge_point_id:str, reservation_id:int, response_status:str):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    cancel_reservation=models.CancelReservation16(
        charge_point_id=charge_point_id,
        timestamp=timestamp,
        reservation_id=reservation_id,
        response_status=response_status
    )
    db.add(cancel_reservation)
    db.commit()
    db.refresh(cancel_reservation)
    return cancel_reservation

#Done - Tested
async def get_configuration_db(charge_point_id:str, configuration_key: list, unknown_key:str):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    for config in configuration_key:
        if not unknown_key:
            get_config=models.GetConfiguration16(
                    charge_point_id=charge_point_id,
                    timestamp=timestamp,
                    key=config['key'],
                    value=config['value'],
                    readonly=config['readonly']
                )
            db.add(get_config)
            db.commit()
            db.refresh(get_config)
        else:
            for unknown in unknown_key:
                get_config=models.GetConfiguration16(
                        charge_point_id=charge_point_id,
                        timestamp=timestamp,
                        key=config['key'],
                        value=config['value'],
                        readonly=config['readonly'],
                        unknown_key=unknown
                    )
                db.add(get_config)
                db.commit()
                db.refresh(get_config)

#Done - Fixa if-satser !!! Behöver testas
async def get_composite_schedule_db(charge_point_id:str, connector_id:int, duration:int, response_status:str,charging_schedule: dict=None, charging_rate_unit:str=None,
    schedule_start:str = None):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')

    if not schedule_start:
        if not charging_schedule['start_schedule']:
            if not charging_schedule:
                schedule=models.GetCompositeSchedule16(
                    charge_point_id=charge_point_id,
                    timestamp=timestamp,
                    connector_id=connector_id,
                    duration=duration,
                    charging_rate_unit=charging_rate_unit,
                    response_status=response_status
                )
                db.add(schedule)
                db.commit()
                db.refresh(schedule)

            else:
                charging_period=charging_schedule['charging_schedule_period']
                for period in charging_period:
                    schedule=models.GetCompositeSchedule16(
                        charge_point_id=charge_point_id,
                        timestamp=timestamp,
                        connector_id=connector_id,
                        duration=charging_schedule['duration'],
                        charging_rate_unit=charging_schedule['charging_rate_unit'],
                        start_period=period['start_period'],
                        limit=period['limit'],
                        number_phases=period['number_phases'],
                        min_charging_rate=charging_schedule['min_charging_rate'],
                        response_status=response_status
                    )
                    db.add(schedule)
                    db.commit()
                    db.refresh(schedule)
        else:
            charging_period=charging_schedule['charging_schedule_period']
            start_schedule = datetime.strptime(charging_schedule['start_schedule'], '%Y-%m-%dT%H:%M:%SZ')
            for period in charging_period:
                schedule=models.GetCompositeSchedule16(
                    charge_point_id=charge_point_id,
                    timestamp=timestamp,
                    connector_id=connector_id,
                    duration=charging_schedule['duration'],
                    charging_rate_unit=charging_schedule['charging_rate_unit'],
                    start_schedule=start_schedule,
                    start_period=period['start_period'],
                    limit=period['limit'],
                    number_phases=period['number_phases'],
                    min_charging_rate=charging_schedule['min_charging_rate'],
                    response_status=response_status
                )
                db.add(schedule)
                db.commit()
                db.refresh(schedule)
    
    else:
        charging_period=charging_schedule['charging_schedule_period']
        start_schedule = datetime.strptime(charging_schedule['start_schedule'], '%Y-%m-%dT%H:%M:%SZ')
        schedule_start = datetime.strptime(schedule_start, '%Y-%m-%dT%H:%M:%SZ')
        for period in charging_period:
            schedule=models.GetCompositeSchedule16(
                charge_point_id=charge_point_id,
                timestamp=timestamp,
                connector_id=connector_id,
                duration=charging_schedule['duration'],
                charging_rate_unit=charging_schedule['charging_rate_unit'],
                schedule_start=schedule_start,
                start_schedule=start_schedule,
                start_period=period['start_period'],
                limit=period['limit'],
                number_phases=period['number_phases'],
                min_charging_rate=charging_schedule['min_charging_rate'],
                response_status=response_status
            )
            db.add(schedule)
            db.commit()
            db.refresh(schedule)

#Done - Tested
async def trigger_db(charge_point_id:str, requested_message:str, connector_id:int, response_status:str):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    trigger=models.Trigger16(
        charge_point_id=charge_point_id,
        timestamp=timestamp,
        connector_id=connector_id,
        requested_message=requested_message,
        response_status=response_status
    )
    db.add(trigger)
    db.commit()
    db.refresh(trigger)
    return trigger

#Done - Behöver testas med riktig mjukvara
async def update_firmware_db(charge_point_id:str, location:str, retrieve_date:str, retries:int, retry_interval:int):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    update_firmware=models.UpdateFirmware16(
        charge_point_id=charge_point_id,
        timestamp=timestamp,
        location=location,
        retrieve_date=retrieve_date,
        retries=retries,
        retry_interval=retry_interval
    )
    db.add(update_firmware)
    db.commit()
    db.refresh(update_firmware)
    return update_firmware

#Done - Tested
async def op_data_transfer_db(charge_point_id:str, vendor_id:str, message_id:str, request_data:str, response_data:str,
    response_status:str):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    data_transfer=models.OperatorDataTransfer16(
        charge_point_id=charge_point_id,
        timestamp=timestamp,
        vendor_id=vendor_id,
        message_id=message_id,
        request_data=request_data,
        response_data=response_data,
        response_status=response_status
    )
    db.add(data_transfer)
    db.commit()
    db.refresh(data_transfer)
    return data_transfer

#Done - Behöver hitta testmetod
async def cp_data_transfer_db(charge_point_id:str, vendor_id:str, message_id:str, request_data:str, response_data:str,
    response_status:str):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    data_transfer=models.ChargePointDataTransfer16(
        charge_point_id=charge_point_id,
        timestamp=timestamp,
        vendor_id=vendor_id,
        message_id=message_id,
        request_data=request_data,
        response_data=response_data,
        response_status=response_status
    )
    db.add(data_transfer)
    db.commit()
    db.refresh(data_transfer)
    return data_transfer

#Done - Tested
async def get_diagnostics_db(charge_point_id:str, location:str, retries:int, retry_interval:int, start_time:str,
    stop_time:str, filename:str):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    start_time=datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%f')
    stop_time=datetime.strptime(stop_time, '%Y-%m-%dT%H:%M:%S.%f')
    diagnostics=models.GetDiagnostics16(
        charge_point_id=charge_point_id,
        timestamp=timestamp,
        location=location,
        retries=retries,
        retry_interval=retry_interval,
        start_time=start_time,
        stop_time=stop_time,
        filename=filename
    )
    db.add(diagnostics)
    db.commit()
    db.refresh(diagnostics)
    return diagnostics

#Done - Kolla upp RecurrencyKind Typo !!! Behöver testas
async def charging_profile_db(charge_point_id:str, connector_id:int, cs_charging_profiles: dict, response_status:str=None):
    charging_schedule = cs_charging_profiles.charging_schedule
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    charging_schedule_period = charging_schedule.charging_schedule_period
    if not cs_charging_profiles.valid_to:
        if not cs_charging_profiles.valid_from:
            if not charging_schedule.start_schedule:
                for period in charging_schedule_period:
                    profile=models.ChargingProfile16(
                        charge_point_id=charge_point_id,
                        timestamp=timestamp,
                        transaction_id=cs_charging_profiles.transaction_id,
                        connector_id=connector_id,
                        charging_profile_id=cs_charging_profiles.charging_profile_id,
                        stack_level=cs_charging_profiles.stack_level,
                        charging_profile_purpose=cs_charging_profiles.charging_profile_purpose,
                        charging_profile_kind=cs_charging_profiles.charging_profile_kind,
                        recurrency_kind=cs_charging_profiles.recurrency_kind,
                        duration=charging_schedule.duration,
                        charging_rate_unit=charging_schedule.charging_rate_unit,
                        start_period=period.start_period,
                        limit=period.limit,
                        number_phases=period.number_phases,
                        min_charging_rate=charging_schedule.min_charging_rate,
                        response_status=response_status
                    )
                    db.add(profile)
                    db.commit()
                    db.refresh(profile)
                return profile
            else:
                start_schedule = datetime.strptime(charging_schedule.start_schedule, '%Y-%m-%dT%H:%M:%SZ')
                for period in charging_schedule_period:
                    profile=models.ChargingProfile16(
                        charge_point_id=charge_point_id,
                        timestamp=timestamp,
                        transaction_id=cs_charging_profiles.transaction_id,
                        connector_id=connector_id,
                        charging_profile_id=cs_charging_profiles.charging_profile_id,
                        stack_level=cs_charging_profiles.stack_level,
                        charging_profile_purpose=cs_charging_profiles.charging_profile_purpose,
                        charging_profile_kind=cs_charging_profiles.charging_profile_kind,
                        recurrency_kind=cs_charging_profiles.recurrency_kind,
                        start_schedule=start_schedule,
                        duration=charging_schedule.duration,
                        charging_rate_unit=charging_schedule.charging_rate_unit,
                        start_period=period.start_period,
                        limit=period.limit,
                        number_phases=period.number_phases,
                        min_charging_rate=charging_schedule.min_charging_rate,
                        response_status=response_status
                    )
                    db.add(profile)
                    db.commit()
                    db.refresh(profile)
                return profile
        else:
            valid_from = datetime.strptime(cs_charging_profiles.valid_from, '%Y-%m-%dT%H:%M:%SZ')
            start_schedule = datetime.strptime(charging_schedule.start_schedule, '%Y-%m-%dT%H:%M:%SZ')
            for period in charging_schedule_period:
                profile=models.ChargingProfile16(
                    charge_point_id=charge_point_id,
                    timestamp=timestamp,
                    transaction_id=cs_charging_profiles.transaction_id,
                    connector_id=connector_id,
                    charging_profile_id=cs_charging_profiles.charging_profile_id,
                    stack_level=cs_charging_profiles.stack_level,
                    charging_profile_purpose=cs_charging_profiles.charging_profile_purpose,
                    charging_profile_kind=cs_charging_profiles.charging_profile_kind,
                    recurrency_kind=cs_charging_profiles.recurrency_kind,
                    duration=charging_schedule.duration,
                    charging_rate_unit=charging_schedule.charging_rate_unit,
                    start_schedule=start_schedule,
                    start_period=period.start_period,
                    limit=period.limit,
                    number_phases=period.number_phases,
                    min_charging_rate=charging_schedule.min_charging_rate,
                    valid_from=valid_from,
                    response_status=response_status
                )
                db.add(profile)
                db.commit()
                db.refresh(profile)
            return profile
    else:
        valid_to = datetime.strptime(cs_charging_profiles.valid_to, '%Y-%m-%dT%H:%M:%SZ')
        valid_from = datetime.strptime(cs_charging_profiles.valid_from, '%Y-%m-%dT%H:%M:%SZ')
        start_schedule = datetime.strptime(charging_schedule.start_schedule, '%Y-%m-%dT%H:%M:%SZ')
        for period in charging_schedule_period:
            profile=models.ChargingProfile16(
                charge_point_id=charge_point_id,
                timestamp=timestamp,
                transaction_id=cs_charging_profiles.transaction_id,
                connector_id=connector_id,
                charging_profile_id=cs_charging_profiles.charging_profile_id,
                stack_level=cs_charging_profiles.stack_level,
                charging_profile_purpose=cs_charging_profiles.charging_profile_purpose,
                charging_profile_kind=cs_charging_profiles.charging_profile_kind,
                recurrency_kind=cs_charging_profiles.recurrency_kind,
                duration=charging_schedule.duration,
                charging_rate_unit=charging_schedule.charging_rate_unit,
                start_schedule=start_schedule,
                start_period=period.start_period,
                limit=period.limit,
                number_phases=period.number_phases,
                min_charging_rate=charging_schedule.min_charging_rate,
                valid_from=valid_from,
                valid_to=valid_to,
                response_status=response_status
            )
            db.add(profile)
            db.commit()
            db.refresh(profile)
        return profile

#Done - Tested
async def clear_charging_profile_db(charge_point_id:str, connector_id:int, charging_profile_id:int, stack_level:int,
    charging_profile_purpose:str, response_status:str):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    clear=models.ClearChargingProfile16(
        charge_point_id=charge_point_id,
        timestamp=timestamp,
        connector_id=connector_id,
        charging_profile_id=charging_profile_id,
        stack_level=stack_level,
        charging_profile_purpose=charging_profile_purpose,
        response_status=response_status
    )
    db.add(clear)
    db.commit()
    db.refresh(clear)
    return clear

#Done - Tested
async def get_local_list_db(charge_point_id:str, list_version:int):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    version=models.GetLocalListVersion16(
        charge_point_id=charge_point_id,
        timestamp=timestamp,
        list_version=list_version
    )
    db.add(version)
    db.commit()
    db.refresh(version)
    return version

#Done - Tested 
async def reset_db(charge_point_id:str, type:str, response_status:str):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    reset=models.Reset16(
        charge_point_id=charge_point_id,
        timestamp=timestamp,
        type=type,
        response_status=response_status
    )
    db.add(reset)
    db.commit()
    db.refresh(reset)
    return reset

#Done - Tested
async def remote_start_db(charge_point_id:str, id_tag:str, response_status:str, connector_id:int, charging_profile:dict =None):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    if charging_profile:
        charging_schedule = charging_profile.charging_schedule
        charging_schedule_period = charging_schedule.charging_schedule_period
        remote_start=models.RemoteStartTransaction16(
            charge_point_id=charge_point_id,
            timestamp=timestamp,
            id_tag = id_tag,
            transaction_id=charging_profile.transaction_id,
            connector_id=connector_id,
            charging_profile_id=charging_profile.charging_profile_id,
            stack_level=charging_profile.stack_level,
            charging_profile_purpose=charging_profile.charging_profile_purpose,
            charging_profile_kind=charging_profile.charging_profile_kind,
            recurrency_kind=charging_profile.recurrency_kind,
            duration=charging_schedule.duration,
            start_schedule=charging_schedule.start_schedule,
            charging_rate_unit=charging_schedule.charging_rate_unit,
            start_period=charging_schedule_period.start_period,
            limit=charging_schedule_period.limit,
            number_phases=charging_schedule_period.number_phases,
            min_charging_rate=charging_schedule.min_charging_rate,
            valid_from=charging_profile.valid_from,
            valid_to=charging_profile.valid_to,
            response_status=response_status
        )
    else:
        remote_start=models.RemoteStartTransaction16(
            charge_point_id=charge_point_id,
            timestamp=timestamp,
            id_tag = id_tag,
            connector_id=connector_id,
            response_status=response_status
        )
    db.add(remote_start)
    db.commit()
    db.refresh(remote_start)
    return remote_start

#Done - Behöver testas vid laddning
async def remote_stop_db(charge_point_id:str, transaction_id:int, response_status:str):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    remote_stop=models.RemoteStopTransaction16(
        charge_point_id=charge_point_id,
        timestamp=timestamp,
        transaction_id=transaction_id,
        response_status=response_status
    )
    db.add(remote_stop)
    db.commit()
    db.refresh(remote_stop)
    return remote_stop

#Done - Tested
async def unlock_connector_db(charge_point_id:str, connector_id:int, response_status:str):
    timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    unlock=models.UnlockConnector16(
        charge_point_id=charge_point_id,
        timestamp=timestamp,
        connector_id=connector_id,
        response_status=response_status
    )
    db.add(unlock)
    db.commit()
    db.refresh(unlock)
    return unlock