import asyncio
import logging
from urllib import response

import websockets
from ocpp.routing import on, after
from ocpp.v201 import ChargePoint as cp
from ocpp.v201 import call, call_result
from ocpp.v201.enums import *
from datetime import datetime
from ocpp.v201.datatypes import *

logging.basicConfig(level=logging.INFO)

"""
This Class is defining the virtual Charge Point.
All of the functions are hard coded.
The proper tests are done on proper Charge Point Hardware.
This is only used to test the OCPP implementation and message routing between HTTP, CSMS and Charge Point.
Since this is a translated version it has not been properly tested.
"""

class ChargePoint(cp):

    async def send_authorize(self, id_token):
        request = call.AuthorizePayload(
            id_token={"idToken": "44AA", "type": "Central"}
        )
        response = await self.call(request)
        return response

    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charging_station={'model':'Drifter',
                'vendor_name':'Drifter',
                'serial_number': '1234Drifter',
                'firmware_version': 'v201',
                'modem': {
                    'iccid': '5G',
                    'imsi': 'Mobile'
                }},
            reason="PowerUp"
        )

        response = await self.call(request)

        if response.status == RegistrationStatusType.accepted:
            print("Connected to central system.")
            await self.send_heartbeat(response.interval)

    async def send_heartbeat(self, interval):
        request = call.HeartbeatPayload()
        while True:
            await self.call(request)
            await asyncio.sleep(interval)

    #Done
    @on(Action.SetVariables)
    def on_set_variable(self, set_variable_data: list):
        return call_result.SetVariablesPayload(
            set_variable_result=[{"attributeType": "Actual", "attributeStatus": "Accepted", "attributeStatusInfo":{"reasonCode": "Accepted", "additionalInfo": ""},
                "component": {"evse": {"id": 1, "connector_id": 1}, "name": "Outlet", "instance": "first_instance"},
                    "variable": {"name": "Socket", "instance": "first_instance"}}]
        )

    #Done
    @on(Action.GetVariables)
    async def on_get_config(self, get_variable_data):
        return call_result.GetVariablesPayload(
            get_variable_result=[{"attributeType": "Actual", "attributeValue": "200", "attributeStatus": "Accepted",
                "attributeStatusInfo":{"reasonCode": "Accepted", "additionalInfo": ""}, "component": {"evse": {"id": 1, "connector_id": 1}, 
                    "name": "Outlet", "instance": "first_instance"}, "variable": {"name": "Socket", "instance": "first_instance"}}]
        )

    #Done
    @on(Action.GetBaseReport)
    async def on_get_config(self, request_id, report_base):
        return call_result.GetBaseReportPayload(
            status="Accepted",
            status_info={"reasonCode": report_base, "additionalInfo": "None"}
        )

    @on(Action.ChangeAvailability)
    def on_change_availability(self, operational_status):
        return call_result.ChangeAvailabilityPayload(
            status=ChangeAvailabilityStatusType.accepted
        )

    @on(Action.RequestStartTransaction)
    async def on_request_start(self, id_token, remote_start_id, evse_id, group_id_token = None, charging_profile = None):
        return call_result.RequestStartTransactionPayload(
            status=RequestStartStopStatusType.accepted,
            status_info={"reason_code": "Start of transaction"},
            transaction_id="ABC123"
        )

    @after(Action.RequestStartTransaction)
    async def on_start_remote(self, id_token, remote_start_id, evse_id):
        await self.send_authorize(id_token)
        await self.transaction_event(id_token, remote_start_id, evse_id)
        return

    @on(Action.RequestStopTransaction)
    def on_stop_remote(self, transaction_id):
        return call_result.RequestStopTransactionPayload(
            status=RequestStartStopStatusType.accepted
        )

    @on(Action.ReserveNow)
    def on_reserve_now(self, id, expiry_date, id_token, connector_type):
        return call_result.ReserveNowPayload(
            status=ReserveNowStatusType.accepted
        )

    @on(Action.CancelReservation)
    def on_cancel_reservation(self, reservation_id):
        return call_result.CancelReservationPayload(
            status=CancelReservationStatusType.accepted
        )

    @on(Action.GetCompositeSchedule)
    def on_cancel_reservation(self, connector_id, duration, charging_rate_unit):
        return call_result.GetCompositeSchedulePayload(
            status=GenericStatusType.accepted
        )

    @on(Action.GetLocalListVersion)
    def on_get_local_list(self):
        return call_result.GetLocalListVersionPayload(
            version_number=1
        )

    @on(Action.SendLocalList)
    def on_send_local_list(self, list_version, local_authorization_list, update_type):
        return call_result.SendLocalListPayload(
            status=SendLocalListStatusType.accepted
        )

    @on(Action.ClearChargingProfile)
    def on_clear_charging_profile(self, charging_profile_id):
        return call_result.ClearChargingProfilePayload(
            status=ClearChargingProfileStatusType.accepted
        )


    @on(Action.ClearCache)
    def on_clear_cache(self):
        return call_result.ClearCachePayload(
            status=ClearCacheStatusType.accepted
        )

    #Done
    @on(Action.SetNetworkProfile)
    def on_set_network_profile(self, configuration_slot, connection_data):
        return call_result.SetNetworkProfilePayload(
            status=SetNetworkProfileStatusType.accepted,
            status_info={"reasonCode": "Set Network Profile", "additionalInfo": "None"}
        )

    async def send_data_transfer(self, vendor_id, message_id, data):
        request = call.DataTransferPayload(
            vendor_id=vendor_id,
            message_id=message_id,
            data=data
        )
        response = await self.call(request)

        if response.status == DataTransferStatusType.accepted:
            print("Transfer Accepted")

        elif response.status == DataTransferStatusType.rejected:
            print("Transfer Rejected")

        else:
            print("User Rejected")    

    async def send_meter_values(self, evse_id, meter_value):
        request = call.MeterValuesPayload(
            evse_id=evse_id,
            meter_value=meter_value
        )
        response = await self.call(request) 

    async def send_status_notification(self, timestamp: datetime, connector_status: str, evse_id:int, connector_id:int):
        request = call.StatusNotificationPayload(
            timestamp=datetime.utcnow().isoformat(),
            connector_status="Occupied",
            evse_id=1,
            connector_id=1
        )
        response = await self.call(request)

    @on(Action.Reset)
    def on_reset(self, type):
        return call_result.ResetPayload(
            status=ResetStatusType.accepted,
            status_info={"reasonCode": type, "additionalInfo": "None"}
        )
    
    async def transaction_event(self, id_token, remote_start_id, evse_id):
        request = call.TransactionEventPayload(
            event_type="Started",
            timestamp=datetime.now().isoformat(),
            trigger_reason="RemoteStart",
            seq_no=1,
            transaction_info=
                {"transaction_id":"ABC123",
                "charging_state":"EVConnected",
                "time_spent_charging": 0,
                "remote_start_id": "ABC123"},
            meter_value=[MeterValueType(
                timestamp= datetime.now().isoformat(), 
                sampled_value = [
                    SampledValueType(value= '200', context= 'Transaction.End', measurand= 'Current.Export', 
                        phase= 'L1', location= 'Outlet', unit_of_measure= 'A'),
                    SampledValueType(value= '50', context= 'Transaction.End', measurand= 'Current.Import', 
                        phase= 'L1', location= 'Outlet', unit_of_measure= 'A'),
                    SampledValueType(value= '12', context= 'Transaction.End', measurand= 'Current.Offered', 
                        phase= 'L1', location= 'Outlet', unit_of_measure= 'A'),
                    SampledValueType(value= '1000', context= 'Transaction.End', 
                        measurand= 'Energy.Active.Export.Register', phase= 'L1', location= 'Outlet', unit_of_measure= 'kWh'),
                    SampledValueType(value= '305', context= 'Transaction.End', 
                        measurand= 'Energy.Active.Import.Register', phase= 'L1', location= 'Outlet', unit_of_measure= 'kWh'),
                    SampledValueType(value= '740', context= 'Transaction.End',
                        measurand= 'Energy.Reactive.Export.Register', phase= 'L1', location= 'Outlet', unit_of_measure= 'kvarh'),
                    SampledValueType(value= '500', context= 'Transaction.End', 
                        measurand= 'Energy.Reactive.Import.Register', phase= 'L1', location= 'Outlet', unit_of_measure= 'kvarh'),
                    SampledValueType(value= '1', context= 'Transaction.End',
                        measurand= 'Energy.Active.Export.Interval', phase= 'L1', location= 'Outlet', unit_of_measure= 'kWh'),
                    SampledValueType(value= '90', context= 'Transaction.End', 
                        measurand= 'Energy.Active.Import.Interval', phase= 'L1', location= 'Outlet', unit_of_measure= 'kWh'),
                    SampledValueType(value= '20.1', context= 'Transaction.End',
                        measurand= 'Energy.Reactive.Export.Interval', phase= 'L1', location= 'Outlet', unit_of_measure= 'kvarh'),
                    SampledValueType(value= '521', context= 'Transaction.End', 
                        measurand= 'Energy.Reactive.Import.Interval', phase= 'L1', location= 'Outlet', unit_of_measure= 'kvarh'),
                    SampledValueType(value= '888', context= 'Transaction.End',
                        measurand= 'Frequency', phase= 'L1', location= 'Outlet', unit_of_measure= 'W'),
                    SampledValueType(value= '222', context= 'Transaction.End', measurand= 'Power.Active.Export', 
                        phase= 'L1', location= 'Outlet', unit_of_measure= 'W'),
                    SampledValueType(value= '333', context= 'Transaction.End', 
                        measurand= 'Power.Active.Import', phase= 'L1', location= 'Outlet', unit_of_measure= 'W'),
                    SampledValueType(value= '621', context= 'Transaction.End', measurand= 'Power.Factor', 
                        phase= 'L1', location= 'Outlet', unit_of_measure= 'W'),
                    SampledValueType(value= '19', context= 'Transaction.End', measurand= 'Power.Offered', 
                        phase= 'L1', location= 'Outlet', unit_of_measure= 'W'),
                    SampledValueType(value= '4000', context= 'Transaction.End', 
                        measurand= 'Power.Reactive.Export', phase= 'L1', location= 'Outlet', unit_of_measure= 'kvar'),
                    SampledValueType(value= '1431', context= 'Transaction.End', 
                        measurand= 'Power.Reactive.Import', phase= 'L1', location= 'Outlet', unit_of_measure= 'kvar'),
                    SampledValueType(value= '634', context= 'Transaction.End',
                        measurand= 'RPM', phase= 'L1', location= 'Outlet', unit_of_measure= 'W'),
                    SampledValueType(value= '80', context= 'Transaction.End', 
                        measurand= 'SoC', phase= 'L1', location= 'Outlet', unit_of_measure= 'Percent'),
                    SampledValueType(value= '25689', context= 'Transaction.End', measurand= 'Temperature', 
                        phase= 'L1', location= 'Outlet', unit_of_measure= 'Celsius'),
                    SampledValueType(value= '5', context= 'Transaction.End', measurand= 'Voltage', 
                        phase= 'L1', location= 'Outlet', unit_of_measure= 'V')
                    ])],
            offline=False,
            number_of_phases_used=1,
            cable_max_current=10,
            reservation_id=0,
            evse=
                {"id": 1,
                "connectorId": 1},
            id_token={
                'id_token':"ABC123",
                'type': "Local"}
        )
        response = await self.call(request)


    @on(Action.TriggerMessage)
    def unlock_connector(self, requested_message):
        return call_result.TriggerMessagePayload(
            status = TriggerMessageStatusType.accepted
        )


    @on(Action.UnlockConnector)
    def unlock_connector(self, evse_id, connector_id):
        return call_result.UnlockConnectorPayload(
            status = UnlockStatusType.unlocked
        )


async def main():
    async with websockets.connect(
        'ws://localhost:8000/ocpp/201/api/v201/CP',
        subprotocols=["ocpp2.0.1"]
    ) as ws:

        cp = ChargePoint('CP', ws)
        await asyncio.gather(cp.start(), cp.send_boot_notification())

if __name__ == '__main__':
    try:
        # asyncio.run() is used when
        #  running this example with Python 3.7 and
        # higher.
        asyncio.run(main())
    except AttributeError:
        # For Python 3.6 a bit more code is required to run the main() task on
        # an event loop.
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()
