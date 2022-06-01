import logging
from datetime import datetime
from urllib import response

from ocpp.routing import on, after
from ocpp.v201 import ChargePoint as cp
from ocpp.v201 import call, call_result
from ocpp.v201.enums import *
from ocpp.v201.enums import Action
from v201.CPO.CRUD import crud

logging.basicConfig(level=logging.INFO)


"""This Class is defining the message functions of the CPO.

The Class is divided into a SEND and RECIEVE functions.
The SEND functions are the ones which are defined as async functions.
The RECIEVE functions are the ones with a @on decorator.
The variables are named according to the OCPP 2.0.1 protocol.
Since this is a translated version it has not been properly tested.
"""
class ChargePoint(cp):

    @on(Action.Authorize)
    async def on_authorize(self, id_token:dict):
        return call_result.AuthorizePayload(
            id_token_info={"status": "Accepted", "cacheExpiryDateTime": datetime.now().isoformat(), "chargingPriority": 1, "language1": "SV", "evseId": [123], 
            "groupIdToken": id_token}
        )

    @on(Action.BootNotification)
    async def on_boot_notification(self, charging_station: dict, reason: str):
        print("A new connection from: ")
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=30,
            status=RegistrationStatusType.accepted
        )

    @after(Action.BootNotification)
    async def after_boot_notification(self, charging_station: dict, reason: str):
        pass

    @on(Action.Heartbeat)
    async def on_heartbeat(self):
        print("Recieved a heartbeat from: ")
        return call_result.HeartbeatPayload(
            current_time=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S') + "Z"
        )

    @after(Action.Heartbeat)
    async def after_heartbeat(self):
        timestamp = datetime.now()
        return await crud.heartbeat_db(self.id, timestamp)


    @on(Action.StatusNotification)
    async def on_status_notification(self, connector_id: int, error_code: str, status: str, timestamp: str = None, info: str = None,
    vendor_id: str = None, vendor_error_code: str = None):
        print("Status Update request recieved")
        return call_result.StatusNotificationPayload()

    @after(Action.StatusNotification)
    async def after_status_notification(self, connector_id: int, error_code: str, status: str, timestamp: str = None, info: str = None,
    vendor_id: str = None, vendor_error_code: str = None):
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

    @on(Action.TransactionEvent)
    def on_transaction_event(self, connector_id: int, id_tag: str, meter_start: int, timestamp: str, reservation_id: int= None):
        print("Transaction Event Updated")
        return call_result.TransactionEventPayload()

    @after(Action.TransactionEvent)
    async def after_start_transaction(self, connector_id: int, id_tag: str, meter_start: int, timestamp: str, reservation_id: int= None):
        timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
        await crud.transaction_db(self.id, connector_id, id_tag, meter_start, timestamp, reservation_id)


    @on(Action.MeterValues)
    async def on_meter_values(self, connector_id: int, meter_value: list, transaction_id: int = None):
        print("Meter Values request recieved")
        return call_result.MeterValuesPayload()

    @after(Action.MeterValues)
    async def after_meter_values(self, connector_id: int, meter_value: list, transaction_id: int = None):
        return await crud.meter_value_db(self.id, connector_id, meter_value, transaction_id)



    async def send_request_start_transaction(self, id_token: dict, remote_start_id: int, evse_id:int = None,
    group_id_token: dict = None, charging_profile: dict = None):
        """Send a start transaction request.
        Not tested"""
        print("Start remote transaction request")
        id_token.additional_info = [id_token.additional_info]
        request = call.RequestStartTransactionPayload(
            id_token=id_token,
            remote_start_id=remote_start_id,
            evse_id=evse_id,
            group_id_token=group_id_token,
            charging_profile=charging_profile
        )

        response = await self.call(request)
        return response


    async def send_request_stop_transaction(self, transaction_id: str):
        """Sends a Stop transaction request.
        Not tested"""
        print("Stop transaction request")
        request =call.RequestStopTransactionPayload(
            transaction_id=transaction_id
        )
        
        response = await self.call(request)
        return response

    async def send_reset(self, type: str, evse_id: int = None):
        """Sends a Reset request.
        Tested"""
        print("Reset Charge Point")
        request =call.ResetPayload(
            type=type
        )

        if evse_id:
            request.evse_id = evse_id
        
        response = await self.call(request)
        return response

    async def send_trigger(self, requested_message: MessageTriggerType, evse: dict = None, **kwargs):
        """Sends a Trigger request.
        Not tested"""
        print("Sending Trigger Message request")
        request = call.TriggerMessagePayload(
            requested_message=requested_message
        )
        if evse:
            request.evse = evse

        response = await self.call(request)
        return response


    async def send_unlock_connector(self, evse_id, connector_id: int):
        """Sends a Unlock request.
        Not tested"""
        print("Unlocking Connector")
        request = call.UnlockConnectorPayload(
            evse_id=evse_id,
            connector_id=connector_id
        )

        response = await self.call(request)
        return response


    async def send_get_variable(self, get_variable_data):
        """
        Request configured variables from charge station.
        """
        print("Get Variable request")
        request = call.GetVariablesPayload(
            get_variable_data=get_variable_data
        )

        response = await self.call(request)
        return response

    #Done
    async def send_get_report_base(self, request_id: int, report_base: str):
        """
        Request a predefined report from charge station.
        """
        print("Get Variable request")
        request = call.GetBaseReportPayload(
            request_id=request_id,
            report_base=report_base
        )

        response = await self.call(request)
        return response

    #Done
    async def send_set_network_profile(self, configuration_slot: int, connection_data: dict):
        """
        Request a predefined report from charge station.
        """
        print("Get Variable request")
        request = call.SetNetworkProfilePayload(
            configuration_slot=configuration_slot,
            connection_data=connection_data
        )

        response = await self.call(request)
        return response

    # async def send_change_availability(self, operational_status, **kwargs):
    #     """Sends a Change availability request.
    #     Not Tested"""
    #     print("Changing Availability request")
    #     return await self.call(call.ChangeAvailabilityPayload(
    #         operational_status=operational_status
    #     ))

    #Done
    async def send_set_variable(self, set_variable_data: list):
        """
        Sends a Change configuration request.
        """
        print("Set variable request")
        request = call.SetVariablesPayload(
            set_variable_data=set_variable_data
        )

        response = await self.call(request)
        return response

    # async def send_get_schedule(self, evse_id, duration, charging_rate_unit):
    #     """Sends a Get schedule request.
    #     Not tested"""
    #     print("Get Composite Schedule request")
    #     return await self.call(call.GetCompositeSchedulePayload(
    #         evse_id=evse_id,
    #         duration=duration,
    #         charging_rate_unit=charging_rate_unit
    #     ))

    async def send_get_local_list(self):
        """
        Sends a Get local list request.
        """
        print("Get Local List request")
        request = call.GetLocalListVersionPayload(
        )

        response = await self.call(request)
        return response

    async def send_local_list(self, version_number: int, update_type: str, local_authorization_list: list = None):
        """Sends Local list request.
        Not tested"""
        print("Send Local List request")
        request = call.SendLocalListPayload(
            version_number=version_number,
            update_type=update_type,
            local_authorization_list=local_authorization_list
        )

        response = await self.call(request)
        return response

    #Done
    async def send_clear_cache(self):
        """
        Sends a Clear Cache request.
        """
        print("Clearing Cache request")
        return await self.call(call.ClearCachePayload())


    # async def send_reserve_now(self, id, expiry_date, id_token, connector_type):
    #     """Sends a Reservation request.
    #     Not tested"""
    #     print("Sending reservation request")
    #     return await self.call(call.ReserveNowPayload(
    #         id=id,
    #         expiry_date=expiry_date,
    #         id_token={'id_token':'123abc',
    #         'type':'Local'},
    #         connector_type=connector_type
    #     ))

    # async def send_cancel_reservation(self, reservation_id):
    #     """Sends a Cancel reservation request.
    #     Not tested"""
    #     print("Sending cancel reservation request")
    #     return await self.call(call.CancelReservationPayload(
    #         reservation_id=reservation_id
    #     ))

    # async def send_clear_charging_profile(self, charging_profile_id):
    #     """Sends a Clear Charging profile request.
    #     Not tested"""
    #     print("Sending clear charging profile request")
    #     return await self.call(call.ClearChargingProfilePayload(
    #         charging_profile_id=charging_profile_id
    #     ))