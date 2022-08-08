from datetime import datetime
from typing import Dict, List
from urllib import response
from uuid import uuid4

from ocpp.routing import on, after
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call, call_result
from ocpp.v16.enums import *
from v16.CPO.CRUD import crud
import logging


logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):

    """This Class is defining the message functions of the CPO.

    The Class is divided into a SEND and RECIEVE functions.
    The SEND functions are the ones which are defined as async functions.
    The RECIEVE functions are the ones with a @on decorator.
    The variables are named according to the OCPP 1.6 protocol.
    """

    #Implemented
    @on(Action.BootNotification)
    async def on_boot_notification(self, charge_point_vendor: str, charge_point_model: str, 
    charge_point_serial_number: str = None, firmware_version: str = None, charge_box_serial_number: str = None, iccid: str = None,
    imsi: str = None, meter_serial_number: str = None, meter_type: str = None):
        """
        Recieved information of Charge Point (Usually sent upon connecting to CPO)
        """
        print("A new connection from: ")
        response = call_result.BootNotificationPayload(
            current_time=datetime.now().isoformat(),
            interval=1000,
            status=RegistrationStatus.accepted
        )
        await crud.boot_notification_db(
            charge_point_id=self.id,
            boot_timestamp=response.current_time,
            charge_point_vendor=charge_point_vendor, 
            charge_point_model=charge_point_model,
            charge_point_serial_number=charge_point_serial_number, 
            firmware_version=firmware_version,
            charge_box_serial_number=charge_box_serial_number,
            iccid=iccid,
            imsi=imsi, 
            meter_serial_number=meter_serial_number, 
            meter_type=meter_type,
            heartbeat_interval=response.interval,
            status=response.status
        )
        return response

    #Implemented
    @after(Action.BootNotification)
    async def after_boot_notification(self, charge_point_vendor: str, charge_point_model: str, 
    charge_point_serial_number: str = None, firmware_version: str = None, charge_box_serial_number: str = None, iccid: str = None,
    imsi: str = None, meter_serial_number: str = None, meter_type: str = None):
        pass
        
    #Implemented
    @on(Action.Heartbeat)
    async def on_heartbeat(self, **kwargs):
        """
        Recieved "Keep Alive" message
        """
        response = call_result.HeartbeatPayload(
            current_time=datetime.now().isoformat()
        )
        await crud.heartbeat_db(self.id, timestamp=response.current_time)
        return response

    #Implemented
    @after(Action.Heartbeat)
    async def after_heartbeat(self):
        """
        Store status in DB
        """
        pass

    #Not Implemented
    @on(Action.Authorize)
    async def on_authorize(self, id_tag: str, **kwargs):
        """
        Recieved an authorization request
        """
        print("ID Token Accepted")
        response = call_result.AuthorizePayload(
            id_tag_info={
                "expiry_date": datetime.now().isoformat(),
                "parent_id_tag": 'parent_tag',

                "status": AuthorizationStatus.accepted
            }
        )
        await crud.authorize_db(self.id, id_tag, authorization_status=response.id_tag_info['status'], 
            expiry_date=response.id_tag_info['expiry_date'], parent_id_tag=response.id_tag_info['parent_id_tag'])
        return response

    #Implemented - Tested
    @on(Action.StatusNotification)
    async def on_status_notification(self, connector_id: int, error_code: str, status: str, timestamp: str = None, info: str = None,
    vendor_id: str = None, vendor_error_code: str = None):
        """
        Recieved an updated Status Notification
        """
        print("Status Update request recieved")
        await crud.status_db(self.id, connector_id, timestamp, error_code, status, info, vendor_id, vendor_error_code)
        return call_result.StatusNotificationPayload()

    #Implemented
    @after(Action.StatusNotification)
    async def after_status_notification(self, connector_id: int, error_code: str, status: str, timestamp: str = None, info: str = None,
    vendor_id: str = None, vendor_error_code: str = None):
        """
        Store Status of Charge Point/Connector in DB
        """
        pass

    #Implemented
    @on(Action.StartTransaction)
    async def on_start_transaction(self, connector_id: int, id_tag: str, meter_start: int, timestamp: str, reservation_id: int = None, **kwargs):
        """
        Notified that transaction has started
        """
        print("Starting transaction request recieved")
        transaction_id=uuid4().time_low
        authorization_status = AuthorizationStatus.accepted
        await crud.start_transaction_db(self.id,transaction_id, connector_id, id_tag, meter_start, timestamp, authorization_status, reservation_id)
        return call_result.StartTransactionPayload(
            transaction_id=transaction_id,
            id_tag_info={"status": authorization_status}
        )

    #Implemented
    @after(Action.StartTransaction)
    async def after_start_transaction(self, connector_id: int, id_tag: str, meter_start: int, timestamp: str, reservation_id: int= None):
        pass

    #Implemented
    @on(Action.StopTransaction)
    async def on_stop_transaction(self, transaction_id: int, meter_stop: int, timestamp: str, reason: str, id_tag: Dict, transaction_data: List = None, **kwargs):
        """
        Notified that transaction ended and recieved information about transaction
        """
        print("Stopping transaction request recieved")
        authorization_status = "Accepted"
        response = call_result.StopTransactionPayload(
            id_tag_info={'status': AuthorizationStatus.accepted}
        )
        await crud.stop_transaction_db(self.id, transaction_id, id_tag, meter_stop, timestamp, reason, authorization_status=authorization_status, transaction_data=transaction_data)
        return response

    #Implemented
    @after(Action.StopTransaction)
    async def after_stop_transaction(self, transaction_id: int, id_tag: str, meter_stop: int, timestamp: str, 
    reason: str = None, transaction_data: list = None):
        """
        Store finished transaction information in DB
        """
        pass

    #Implemented
    @on(Action.MeterValues)
    async def on_meter_values(self, connector_id: int, meter_value: list, transaction_id: int = None, *args, **kwargs):
        """
        Recieved Meter Values
        """
        await crud.meter_value_db(self.id, connector_id, meter_value, transaction_id)
        return call_result.MeterValuesPayload()

    #Implemented
    @after(Action.MeterValues)
    async def after_meter_values(self, connector_id: int, meter_value: list, transaction_id: int = None):
        """
        Store Values in DB
        """
        pass

    #Implemented
    @on(Action.DiagnosticsStatusNotification)
    async def on_diagnostics_status(self, status: str):
        """
        Recieved a Diagnostics Status Notification
        """
        await crud.diagnostics_status_db(self.id, status)
        return call_result.DiagnosticsStatusNotificationPayload()

    
    #Implemented
    @after(Action.DiagnosticsStatusNotification)
    def after_diagnostics_status(self, status: str):
        """
        Store Status in DB
        """
        pass
    
    #Implemented - Tested
    @on(Action.FirmwareStatusNotification)
    async def on_firmware_status(self, status: str):
        """
        Recieved a Firmware Status Notification
        """
        await crud.firmware_status_db(self.id, status)
        return call_result.FirmwareStatusNotificationPayload()

    #Implemented
    @after(Action.FirmwareStatusNotification)
    def after_firmware_status(self, status: str):
        """
        Store Status in DB
        """
        pass

    #Implemented - Tested
    @on(Action.DataTransfer)
    async def on_data_transfer(self, vendor_id:str, message_id:str, data:str):
        response_data = "Drifter"
        status = DataTransferStatus.accepted
        await crud.cp_data_transfer_db(self.id, vendor_id, message_id, request_data=data, response_data=response_data, response_status=status)
        return call_result.DataTransferPayload(status, data=response_data)

    @after(Action.DataTransfer)
    def after_data_transfer(self, vendor_id:str, message_id:str, data:str):
        pass

    #Implemented
    async def send_remote_start_transaction(self, id_tag: str, connector_id: int = None,
        charging_profile: dict= None, **kwargs):
        """
        Start charging remotely
        """
        print("Start remote transaction request")
        request = call.RemoteStartTransactionPayload(
            id_tag=id_tag
        )

        if connector_id:
            request.connector_id = connector_id

        if charging_profile:
            request.charging_profile = charging_profile

        response = await self.call(request)
        await crud.remote_start_db(self.id, id_tag=id_tag, connector_id=connector_id, 
            charging_profile=charging_profile, response_status=response.status)
        return response
        

    #Implemented
    async def send_remote_stop_transaction(self, transaction_id: int, **kwargs):
        """
        Stop charging remotely
        """
        print("Stop transaction request")
        request = call.RemoteStopTransactionPayload(
            transaction_id=transaction_id
        )

        response = await self.call(request)
        await crud.remote_stop_db(self.id, transaction_id, response_status=response.status)
        return response

    #Implemented - Tested
    async def send_change_availability(self, connector_id: int, type: AvailabilityType, **kwargs):
        """
        Change Charge Point availability.
        """
        print("Changing Availability request")
        request = call.ChangeAvailabilityPayload(
            connector_id=connector_id,
            type=type
        )

        response = await self.call(request)
        await crud.availability_db(self.id, connector_id, type, response_status=response.status)
        return response
    
    #Implemented
    async def send_get_schedule(self, connector_id: int, duration: int, charging_rate_unit: ChargingRateUnitType = None, **kwargs):
        """
        Get Charging Profile schedule
        """
        print("Get Composite Schedule request")
        request = call.GetCompositeSchedulePayload(
            connector_id=connector_id,
            duration=duration
        )

        if charging_rate_unit:
            request.charging_rate_unit = charging_rate_unit

        response = await self.call(request)
        await crud.get_composite_schedule_db(charge_point_id=self.id, connector_id=connector_id, duration=duration, charging_rate_unit=charging_rate_unit,
            schedule_start=response.schedule_start, response_status=response.status, charging_schedule=response.charging_schedule)
        return response

    #Implemented
    async def get_local_list(self, **kwargs):
        """
        Get authorized user list version
        """
        print("Get Local List request")
        request = call.GetLocalListVersionPayload(
        )

        response = await self.call(request)
        await crud.get_local_list_db(self.id, response.list_version)
        return response

    #Implemented
    async def send_local_list(self, list_version: int, update_type: UpdateType, local_authorization_list = None, **kwargs):
        """
        Send authorized users to Charge Point
        """
        print("Send Local List request")
        request = call.SendLocalListPayload(
            list_version=list_version,
            update_type=update_type
        )

        if local_authorization_list:                
            request.local_authorization_list = local_authorization_list

        response = await self.call(request)
        await crud.send_local_list(self.id, list_version, update_type, local_authorization_list, response_status=response.status)
        return response

    #Implemented - Tested
    async def send_change_configuration(self, key: str, value: str, **kwargs):
        """
        Change a configuration key in Charge Point
        """
        print("Changing Configuration request")
        request = call.ChangeConfigurationPayload(
            key=key,
            value=value
        )

        response = await self.call(request)
        await crud.configure_db(self.id, key, value, response_status=response.status)
        return response


    #Implemented - Tested
    async def send_get_configuration(self, key:list = None, **kwargs):
        """
        Get configuration information from a key in Charge Point
        """
        print("Get Configuration request")
        request = call.GetConfigurationPayload()

        if key:
            request.key = [key]

        response = await self.call(request)
        await crud.get_configuration_db(self.id, response.configuration_key, response.unknown_key)
        return response

    #Implemented - Tested
    async def send_clear_cache(self, **kwargs):
        """
        Clear authorization cache
        """
        print("Clearing Cache request")
        request = call.ClearCachePayload()

        response = await self.call(request)
        await crud.clear_cache_db(self.id, response_status=response.status)
        return response

    #Implemented - Tested
    async def send_reserve_now(self, connector_id: int, expiry_date:str, id_tag:str, reservation_id: int, parent_id_tag: str = None,  **kwargs):
        """
        Reserve a Charge Point for an ID
        """
        expiry_date=datetime.strftime(expiry_date, '%Y-%m-%dT%H:%M:%S.%f')
        print("Sending reservation request")
        request = call.ReserveNowPayload(
            connector_id=connector_id,
            expiry_date=expiry_date,
            id_tag=id_tag,
            reservation_id=reservation_id
        )

        if parent_id_tag:
            request.parent_id_tag = parent_id_tag

        response = await self.call(request)
        await crud.reservation_db(self.id, connector_id, id_tag, reservation_id, response_status=response.status, expiry_date=expiry_date, parent_id_tag=parent_id_tag)
        return response

    #Implemented - Tested
    async def send_cancel_reservation(self, reservation_id: int, **kwargs):
        """
        Cancel reservation
        """
        print("Sending cancel reservation request")
        request = call.CancelReservationPayload(
            reservation_id=reservation_id
        )

        response = await self.call(request)
        await crud.cancel_reservation_db(self.id, reservation_id, response_status=response.status)
        return response

    #Implemented - Tested
    async def send_reset(self, type: ResetType):
        """
        Reset Charge Point
        """
        print("Reset Charge Point")
        request = call.ResetPayload(
            type=type
        )

        response = await self.call(request)
        await crud.reset_db(self.id, type, response_status=response.status)
        return response

    #Implemented - Tested
    async def send_trigger(self, requested_message: str, connector_id: int = None, **kwargs):
        print("Sending Trigger Message request")
        """
        Trigger a Charge Point initiated message
        """
        request = call.TriggerMessagePayload(
            requested_message=requested_message
        )

        if connector_id:
            request.connector_id = connector_id

        response = await self.call(request)
        await crud.trigger_db(self.id, requested_message, connector_id, response_status=response.status)
        return response


    #Implemented
    async def send_unlock_connector(self, connector_id: int):
        """
        Unlock connector socket.
        """
        print("Unlocking Connector")
        request = call.UnlockConnectorPayload(
            connector_id=connector_id
        )

        response = await self.call(request)
        await crud.unlock_connector_db(self.id, connector_id, response_status=response.status)
        return response

    #Implemented
    async def send_charging_profile(self, connector_id: int, cs_charging_profiles):
        """
        Set a Charging Profile for Charge Point
        """
        request = call.SetChargingProfilePayload(
            connector_id=connector_id,
            cs_charging_profiles= cs_charging_profiles
        )
        response = await self.call(request)
        await crud.charging_profile_db(self.id, connector_id, cs_charging_profiles, response_status=response.status)
        return response

    #Implemented - Tested
    async def send_clear_charging_profile(self, id: int = None, connector_id: int = None,
    charging_profile_purpose: ChargingProfilePurposeType = None, stack_level: int = None, **kwargs):
        """
        Clear Charging Profile in Charge Point.
        """
        print("Sending clear charging profile request")
        request = call.ClearChargingProfilePayload()

        if id:
            request.id = id
        if connector_id:
            request.connector_id=connector_id
        if charging_profile_purpose:
            request.charging_profile_purpose=charging_profile_purpose
        if stack_level:
            request.stack_level=stack_level

        response = await self.call(request)
        await crud.clear_charging_profile_db(self.id, connector_id, id, stack_level, charging_profile_purpose, response_status=response.status)
        return response


    #Implemented
    async def get_diagnostics(self, location:str, retries: int = None, retry_interval: int = None,
        start_time:datetime = None, stop_time:datetime = None, **kwargs):
        """
        Get diagnostics from Charge Point.
        """
        request = call.GetDiagnosticsPayload(
            location=location
        )
        if retries:
            request.retries=retries
        if retry_interval:
            request.retry_interval=retry_interval
        if start_time:
            start_time = datetime.strftime(start_time, '%Y-%m-%dT%H:%M:%S.%f')
            request.start_time=start_time
        if stop_time:
            stop_time = datetime.strftime(stop_time, '%Y-%m-%dT%H:%M:%S.%f')
            request.stop_time=stop_time

        response = await self.call(request)
        await crud.get_diagnostics_db(self.id, location, retries, retry_interval, start_time, stop_time, response.file_name)
        return response

    #Implemented
    async def send_update_firmware(self, location: str, retrieve_date: datetime, retries: int = None, retry_interval: int = None, **kwargs):
        """
        Update firmware in Charge Point.
        Location refers to folder inside the Charge Point.
        """
        request = call.UpdateFirmwarePayload(
            location=location,
            retrieve_date= datetime.strftime(retrieve_date, '%Y-%m-%dT%H:%M:%S.%f')
        )
        if retries:
            request.retries=retries
        if retry_interval:
            request.retry_interval=retry_interval
        
        response = await self.call(request)
        await crud.update_firmware_db(self.id, location, retrieve_date, retries, retry_interval)
        return response


    #Implemented - Tested
    async def send_data_transfer(self, vendor_id: str, message_id: str = None, data: str = None, **kwargs):
        """
        Send data not supported by OCPP
        """
        request = call.DataTransferPayload(
            vendor_id=vendor_id   
        )
        if message_id:
            request.message_id=message_id
        if data:
            request.data=data

        response = await self.call(request)
        await crud.op_data_transfer_db(self.id, vendor_id, message_id, data, response_data=response.data, response_status=response.status)
        return response