from datetime import datetime
from typing import Dict, List
from uuid import uuid4

from ocpp.routing import on, after
from ocpp.messages import _DecimalEncoder
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call, call_result
from ocpp.v16.enums import *
from v16.CPO.CRUD import crud
import simplejson
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
    async def on_boot_notification(self, charge_point_serial_number: str, charge_point_vendor: str, charge_point_model: str, **kwargs):
        """
        Recieved information of Charge Point (Usually sent upon connecting to CPO)
        """
        print("A new connection from: ")
        return call_result.BootNotificationPayload(
            current_time=datetime.now().isoformat(),
            interval=1000,
            status=RegistrationStatus.accepted
        )

    #Implemented
    @after(Action.BootNotification)
    async def after_boot_notification(self, charge_point_vendor: str, charge_point_model: str, 
    charge_point_serial_number: str = None, firmware_version: str = None, charge_box_serial_number: str = None, iccid: str = None,
    imsi: str = None, meter_serial_number: str = None, meter_type: str = None):
        """
        Store Charge Point information in DB
        """
        charge_point_id = self.id
        return await crud.boot_notification_db(
            charge_point_id,
            charge_point_vendor, 
            charge_point_model, 
            charge_point_serial_number, 
            firmware_version,
            charge_box_serial_number,
            iccid,
            imsi, 
            meter_serial_number, 
            meter_type
        )
        
    #Implemented
    @on(Action.Heartbeat)
    async def on_heartbeat(self, **kwargs):
        """
        Recieved "Keep Alive" message
        """
        print("Recieved a heartbeat from: ")
        return call_result.HeartbeatPayload(
            current_time=datetime.now().isoformat() + "Z"
        )

    #Implemented
    @after(Action.Heartbeat)
    async def after_heartbeat(self):
        """
        Store status in DB
        """
        timestamp = datetime.now()
        return await crud.heartbeat_db(self.id, timestamp)

    #Not Implemented
    @on(Action.Authorize)
    def on_authorize(self, id_tag: str, **kwargs):
        """
        Recieved an authorization request
        """
        print("ID Token Accepted")
        return call_result.AuthorizePayload(
            id_tag_info={
                # 'expiry_date': 'JAN13',
                # 'parent_id_tag': 'parent_tag',

                "status": AuthorizationStatus.accepted
            }
        )

    #Implemented
    @on(Action.StatusNotification)
    def on_status_notification(self, connector_id: int, error_code: str, status: str, timestamp: str = None, info: str = None,
    vendor_id: str = None, vendor_error_code: str = None):
        """
        Recieved an updated Status Notification
        """
        print("Status Update request recieved")
        return call_result.StatusNotificationPayload()

    #Implemented
    @after(Action.StatusNotification)
    async def after_status_notification(self, connector_id: int, error_code: str, status: str, timestamp: str = None, info: str = None,
    vendor_id: str = None, vendor_error_code: str = None):
        """
        Store Status of Charge Point/Connector in DB
        """
        timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
        return await crud.status_db(
            self.id,
            connector_id, 
            error_code,
            status,
            timestamp, 
            info, 
            vendor_id, 
            vendor_error_code,
            )

    #Implemented
    @on(Action.StartTransaction)
    async def on_start_transaction(self, connector_id: int, id_tag: str, meter_start: int, timestamp: str, reservation_id: int = None, **kwargs):
        """
        Notified that transaction has started
        """
        print("Starting transaction request recieved")
        transaction_id=uuid4().time_low
        timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
        await crud.transaction_db(self.id, transaction_id, connector_id, id_tag, meter_start, timestamp, reservation_id)
        return call_result.StartTransactionPayload(
            transaction_id=transaction_id,
            id_tag_info={"status": AuthorizationStatus.accepted}
        )

    #Implemented
    @after(Action.StartTransaction)
    async def after_start_transaction(self, connector_id: int, id_tag: str, meter_start: int, timestamp: str, reservation_id: int= None):
        pass

    #Implemented
    @on(Action.StopTransaction)
    def on_stop_transaction(self, transaction_id: int, meter_stop: int, timestamp: str, reason: str, id_tag: Dict, transaction_data: List, **kwargs):
        """
        Notified that transaction ended and recieved information about transaction
        """
        print("Stopping transaction request recieved")
        return call_result.StopTransactionPayload(
            id_tag_info={'status': AuthorizationStatus.accepted}
        )

    #Implemented
    @after(Action.StopTransaction)
    async def after_stop_transaction(self, transaction_id: int, id_tag: str, meter_stop: int, timestamp: str, 
    reason: str = None, transaction_data: list = None):
        """
        Store finished transaction information in DB
        """
        await crud.stop_transaction_db(self.id, transaction_id, id_tag, meter_stop, timestamp, reason, transaction_data)

    #Implemented
    @on(Action.MeterValues)
    def on_meter_values(self, connector_id: int, meter_value: list, transaction_id: int = None, *args, **kwargs):
        """
        Recieved Meter Values
        """
        print("Meter Values request recieved")
        print(f'{self.id} recieved MeterValue')
        return call_result.MeterValuesPayload()

    #Implemented
    @after(Action.MeterValues)
    async def after_meter_values(self, connector_id: int, meter_value: list, transaction_id: int = None):
        """
        Store Values in DB
        """
        return await crud.meter_value_db(self.id, connector_id, meter_value, transaction_id)

    #Implemented
    @on(Action.DiagnosticsStatusNotification)
    def on_diagnostics_status(self, *args, **kwargs):
        """
        Recieved a Diagnostics Status Notification
        """
        return call_result.DiagnosticsStatusNotificationPayload()

    
    #Implemented
    @after(Action.DiagnosticsStatusNotification)
    def after_diagnostics_status(self, status: str):
        """
        Store Status in DB
        """
        pass
    
    #Implemented
    @on(Action.FirmwareStatusNotification)
    def on_firmware_status(self, **kwargs):
        """
        Recieved a Firmware Status Notification
        """
        return call_result.FirmwareStatusNotificationPayload()

    #Implemented
    @after(Action.FirmwareStatusNotification)
    def after_firmware_status(self, status: str):
        """
        Store Status in DB
        """
        pass

    @on(Action.DataTransfer)
    def on_data_transfer(self):
        pass

    @after(Action.DataTransfer)
    def after_data_transfer(self):
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
        return response

    #Implemented
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

        #response.list_version

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
            request.local_authorization_list = [local_authorization_list]

        response = await self.call(request)
        return response

    #Implemented    
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
        return response


    #Implemented
    async def send_get_configuration(self, key = None, **kwargs):
        """
        Get configuration information from a key in Charge Point
        """
        print("Get Configuration request")
        request = call.GetConfigurationPayload()

        if key:
            request.key = [key]

        print(request)

        response = await self.call(request)
        return response

    #Implemented
    async def send_clear_cache(self, **kwargs):
        """
        Clear authorization cache
        """
        print("Clearing Cache request")
        request = call.ClearCachePayload()

        response = await self.call(request)
        return response

    #Implemented
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

        print(request)

        response = await self.call(request)
        return response

    #Implemented
    async def send_cancel_reservation(self, reservation_id: int, **kwargs):
        """
        Cancel reservation
        """
        print("Sending cancel reservation request")
        request = call.CancelReservationPayload(
            reservation_id=reservation_id
        )

        response = await self.call(request)
        return response

    #Implemented
    async def send_reset(self, type: ResetType):
        """
        Reset Charge Point
        """
        print("Reset Charge Point")
        request = call.ResetPayload(
            type=type
        )

        response = await self.call(request)
        return response

    #Implemented
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
        return response

    #Not completed // Fix data types in cs_charging_profiles
    async def send_charging_profile(self, connector_id: int, cs_charging_profiles):
        """
        Set a Charging Profile for Charge Point
        """
        request = call.SetChargingProfilePayload(
            connector_id=connector_id,
            cs_charging_profiles= cs_charging_profiles
        )
        response = await self.call(request)
        return response

    #Implemented
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

        print(request)
        response = await self.call(request)
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
        return response


    #Implemented.
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
        return response