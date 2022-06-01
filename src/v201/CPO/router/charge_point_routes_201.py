from v201.CPO.Schemas import schemas
from v201.CPO.Auth import oauth2
from resources import models
from resources.database import get_db
from sqlalchemy.orm import Session
from v201.CPO.Hashing.hashing import Hash
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from v201.CPO.ChargePointOp.cpo_class_v201 import ChargePoint
from v201.CPO.Websocket.websocket import WebsocketAdapter
from v201.CPO.ChargePointOp.charge_point_operator_v201 import CentralSystem
from ocpp.v201.enums import *
from ocpp.v201.datatypes import *
from v201.CPO.Hashing.hashing import Hash
from v201.CPO.CRUD import crud
from typing import List


router = APIRouter(tags=["Charge Point"])
cpo = CentralSystem()


"""
Function to connect a Charge Point to the CPO through websockets
Done
"""

@router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    try:
        await websocket.accept(subprotocol="ocpp2.0.1")
        charge_point_id = websocket.url.path.strip("/ocpp/201/api/v201/")
        cp = ChargePoint(charge_point_id, WebsocketAdapter(websocket))
        queue = cpo.register_charger(cp)
        await queue.get()

    except WebSocketDisconnect:
        socket = WebsocketAdapter()
        await socket.disconnect(websocket)


@router.get("/chargepoints/{charge_point_id}", response_model=schemas.ChargePoint, 
    summary="Get a Charge Point connected to the CPO. The response contains boot information about the Charge Point.")
async def get_charge_point(charge_point_id: str, db: Session = Depends(get_db)):
    """
    GET a Charge Point connected to the CPO
    """
    try:
        charge_point = await crud.get_charge_point(db, charge_point_id)
        return charge_point
    except Exception as e:
        return(f"Failed to get charging session {charge_point_id}: {e}")

#Done // Not getting response
@router.get("/chargepoints/owned", response_model=List[schemas.ChargePoint],
    summary="Get all Charge Points connected to the CPO. The response contains boot information about the Charge Point.")
async def get_all_charge_points(db: Session = Depends(get_db)):
    """
    GET all Charge Points that are connected to the CPO
    """
    try:
        charge_points = await crud.get_all_charge_points(db)
        return charge_points
    except Exception as e:
        return(f"Failed to get charge points: {e}")

#Done
@router.get("/chargepoints/{charge_point_id}/chargingsessions", response_model=List[schemas.ChargePointSessions],
    summary="Get all past Charging Sessions of a Charge Point.")
async def get_charge_point_session(charge_point_id: str, db: Session = Depends(get_db)):
    """
    GET all active Charging Sessions of a Charge Point
    """
    try:
        charge_point_session = await crud.get_charge_point_sessions(db, charge_point_id)
        return charge_point_session
    except Exception as e:
        return(f"Failed to get charging session {charge_point_id}: {e}")

#Done
@router.get("/chargepoints/{charge_point_id}/chargingsessions/{id_tag}", response_model=List[schemas.ChargePointSessions],
    summary="Get an past Charging Sessions of a Charge Point. ID Tag and Transaction ID specifies the session.")
async def get_charge_point_session_id(charge_point_id: str, id_tag: str, db: Session = Depends(get_db)):
    """
    GET a Charging Session specific to an ID Tag
    """
    try:    
        charge_point_session = await crud.get_all_charge_point_session_id(db, charge_point_id, id_tag)
        return charge_point_session
    except Exception as e:
        return(f"Failed to get charging session {charge_point_id}: {e}")

#Done
@router.get("/chargepoints/{charge_point_id}/chargingsessions/{id_tag}/transaction/{transaction_id}", response_model=schemas.ChargePointSessions,
    summary="Get an past Charging Sessions of a Charge Point. ID Tag specifies the session.")
async def get_charge_point_session_id(charge_point_id: str, id_tag: str, transaction_id: int, db: Session = Depends(get_db)):
    """
    GET a Charging Session specific to an ID Tag
    """
    try:    
        charge_point_session = await crud.get_charge_point_session_id(db, charge_point_id, id_tag, transaction_id)
        return charge_point_session
    except Exception as e:
        return(f"Failed to get charging session {charge_point_id}: {e}")

#Done
@router.get("/chargepoints/{charge_point_id}/connectors/{connector_id}/chargingsessions", response_model=List[schemas.ChargePointSessions],
    summary="Get all past Charging Sessions of a one connector of a Charge Point.")
async def get_connector_session(charge_point_id: str, connector_id: int, db: Session = Depends(get_db)):
    """
    GET the Charging Sessions relevant to a connector
    """
    try:
        charge_point_session = await crud.get_charge_point_sessions_connector(db, charge_point_id, connector_id)
        return charge_point_session
    except Exception as e:
        return(f"Failed to get charging session {charge_point_id}: {e}")

#Done
@router.get("/chargepoints/{charge_point_id}/connectors/{connector_id}/chargingsessions/ongoing", response_model=List[schemas.ChargePointSessions],
    summary="Get all ongoing Charging Sessions of a one connector of a Charge Point.")
async def get_connector_session(charge_point_id: str, connector_id: int, db: Session = Depends(get_db)):
    """
    GET ongoing Charging Sessions relevant to a connector
    """
    try:
        charge_point_session = await crud.get_ongoing_charge_point_session(db, charge_point_id, connector_id)
        return charge_point_session
    except Exception as e:
        return(f"Failed to get charging session {charge_point_id}: {e}")

#Not done
@router.put("/chargepoints/{charge_point_id}/remotestart")
async def remote_start( charge_point_id: str,
id_token: IdTokenType, remote_start_id: int, evse_id: int, charging_profile: ChargingProfileType):
    """
    Start a Charging Session
    """
    try:
        get_response = await cpo.request_start(charge_point_id, id_token, remote_start_id, evse_id, 
            charging_profile)
        return get_response
    except Exception as e:
        return(f"Failed to start remote charging: {e}")

#Not Done
@router.put("/chargepoints/{charge_point_id}/connectors/{connector_id}/remotestop")
async def remote_stop(charge_point_id: str, connector_id: int, transaction_id: str):
    """
    Stop a Charging Session
    Need Transaction ID Implemented
    """
    try:
        get_response = await cpo.request_stop(charge_point_id, connector_id, transaction_id)
        return get_response
    except Exception as e:
        return(f"Failed to stop remote charging: {e}")


"""
GET a specific Configuration of a Charge Point
Done
"""

@router.get("/chargepoints/{charge_point_id}/configure")
async def get_config(charge_point_id:str, key: schemas.ConfigurationKey,
):
    key = [key]
    try:
        get_response = await cpo.get_configuration(charge_point_id, key)
        print(f"==> The response from charger==> {get_response}")
        return get_response
    except Exception as e:
        return(f"Failed to get configuration: {e}")


"""
PUT a Configure to a Charge Point within the ConfigurationKey Enum
Done
"""

@router.put("/chargepoints/{charge_point_id}/configure")
async def put_config(request: schemas.Configuration, charge_point_id:str,
):
    key = request.key
    value = request.value
    try:
        get_response = await cpo.change_configuration(charge_point_id, key, value)
        print(f"==> The response from charger==> {get_response}")
        return get_response
    except Exception as e:
        return(f"Failed to change configuration: {e}")

"""
Change Availability
"""

@router.put("/chargepoints/{charge_point_id}/connectors/{connector_id}/availability")
async def put_connector_config(charge_point_id: str, connector_id: int, type: ChangeAvailabilityStatusType):
    try:
        get_response = await cpo.change_availability(charge_point_id, connector_id, type)
        print(f"The response from charger {get_response}")
        return get_response
    except Exception as e:
        return(f"Failed to change availability of charge point {charge_point_id}: {e}")

"""
Reset Charge Point
Done
"""

#Done
@router.put("/chargepoints/{charge_point_id}/reset",
    summary="Restart a Charge Point")
async def reset(charge_point_id: str, type: ResetType):
    """
    Reset Charge Point
    """
    try:
        get_response = await cpo.reset(charge_point_id, type)
        return get_response
    except Exception as e:
        return(f"Failed to reset charge point {charge_point_id}: {e}")


#Done
@router.get("/chargepoints/{charge_point_id}/status", response_model=schemas.ChargePointStatus,
    summary="Get the status of a Charge Point.")
async def trigger_status(charge_point_id:str, connector_id: int = None, db: Session = Depends(get_db)):
    """
    GET a Status Notification from a Charge Point by sending a Trigger Message
    """
    try:
        get_response = await cpo.trigger_status(charge_point_id, connector_id)
        print(f" The response from charger {get_response}")
        status = await crud.get_status(db, charge_point_id)
        return status
    except Exception as e:
        return(f"Failed to get status of charge point {charge_point_id}: {e}")

#Done
@router.post("/chargepoints/{charge_point_id}/metervalues",
    summary="Get The Meter Values of a Charge Point. The meter values refer to electrical measured output and input signals.")
async def trigger_meter(charge_point_id:str, connector_id: int = None):
    """
    GET Meter Values from a Charge Point by sending a Trigger Message
    """
    try:
        get_response = await cpo.trigger_meter_values(charge_point_id, connector_id)
        print(f" The response from charger {get_response}")
        return get_response
    except Exception as e:
        return(f"Failed to get meter values of charge point {charge_point_id}: {e}")


"""
Ask Charge Point to send Boot Notification message.
Done
"""

@router.post("/chargepoints/{charge_point_id}/boot")
async def get_boot(charge_point_id:str, connector_id: int = None):
    try:
        get_response = await cpo.trigger_boot(charge_point_id, connector_id )
        print(f" The response from charger {get_response}")
        return get_response
    except Exception as e:
        return(f"Failed to GET Status: {e}")

#Not done
@router.post("/chargepoints/{charge_point_id}/updatefirmware",
    summary="Updates the firmware of the Charge Point. Sends the location of which the Charge Point can download the updated firmware.")
async def update_firmware(charge_point_id:str):
    """
    Update the firmware of a Charge Point.
    """
    try:
        get_response = await cpo.update_firmware(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to GET Status: {e}")

#Done
@router.get("/chargepoints/{charge_point_id}/firmwarestatus",
    summary="Get the update status of the firmware update.")
async def trigger_firmware(charge_point_id:str, connector_id: int = None):
    """
    Get Firmware Notification Message of Charge Point
    """
    try:
        get_response = await cpo.trigger_frimware_status(charge_point_id, connector_id)
        print(f" The response from charger {get_response}")
        return get_response
    except Exception as e:
        return(f"Failed to GET Status: {e}")

#Done
@router.post("/chargepoints/{charge_point_id}/diagnostics",
    summary="Get diagnostics from a Charge Point. Specify the location to which it should be sent to.")
async def get_diagnostics(charge_point_id:str):
    """
    Get diagnostics of a specific location of a Charge Point
    """
    try:
        get_response = await cpo.get_diagnostics(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to GET Status: {e}")

#Done
@router.get("/chargepoints/{charge_point_id}/diagnosticsnotification",
    summary="Get the status of the ongoing diagnostics transfer.")
async def trigger_diagnostics(charge_point_id:str, connector_id: int = None):
    """
    Get Diagnostics Message of Charge Point
    """
    try:
        get_response = await cpo.trigger_diagnostics(charge_point_id, connector_id)
        return get_response
    except Exception as e:
        return(f"Failed to GET Status: {e}")

#Done
@router.post("/chargepoints/{charge_point_id}/boot",
    summary="Charge Point resends the boot notification message.")
async def trigger_boot(charge_point_id:str, connector_id: int = None):
    """
    Charge Point send a Boot Notification message
    """
    try:
        get_response = await cpo.trigger_boot(charge_point_id, connector_id )
        return get_response
    except Exception as e:
        return(f"Failed to GET Status: {e}")

#Done
@router.post("/chargepoints/{charge_point_id}/heartbeat",
    summary="Charge Point sends a 'Keep alive' signal to CPO. Sets the time interval to 30 seconds.")
async def trigger_heartbeat(charge_point_id:str, connector_id: int = None):
    """
    Ask Charge Point to send a "is alive" heartbeat signal. Should be used if 
    heartbeat signal is not sent during regular interval.
    """
    try:
        get_response = await cpo.trigger_heartbeat(charge_point_id, connector_id )
        return get_response
    except Exception as e:
        return(f"Failed to GET Status: {e}")

#Done
@router.put("/chargepoints/{charge_point_id}/unlock",
    summary="Unlock a connector of a Charge Point. This works only if the charging cable is removable. Any ongoing transactions will be terminated.")
async def put_unlock(charge_point_id:str, connector_id: int):
    """
    Unlocks Connector if cable is removable. Automatically stops any ongoing transactions.
    """
    try:
        get_response = await cpo.unlock_connector(charge_point_id, connector_id)
        return get_response
    except Exception as e:
        return(f"Failed to unlock connector: {e}")

#Done // Needs DB connection
@router.get("/chargepoints/{charge_point_id}/locallist",
    summary="Get the Local Authorization List version of a Charge Point.")
async def get_local_list(charge_point_id: str):
    """
    Get the local authorization list version.
    """
    try:
        get_response = await cpo.get_local_list(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to get local list {charge_point_id}: {e}")

#local_authorization_list: AuthorizationData Needs to be solved
@router.post("/chargepoints/{charge_point_id}/locallist",
    summary="Send a Local Authorization List to Charge Point.")
async def send_local_list(charge_point_id: str, version_number: int, update_type: UpdateType):
    try:
        get_response = await cpo.send_local_list(charge_point_id,version_number)
        return get_response
    except Exception as e:
        return(f"Failed to send local list {charge_point_id}: {e}")

#Proper data type needed for cs_charging_profile
@router.post("/chargepoints/{charge_point_id}/chargingprofile/{connector_id}",
    summary="Set a Charging Profile of a Charge Point. Control the maximum output of a Charge Point during a period of time.")
async def charging_profile(charge_point_id: str, connector_id: int):
    """
    Set Charging Profile allows Charge Point to set maximum "A" or "W" during a period of time.
    """
    try:
        get_response = await cpo.set_charging_profile(charge_point_id, connector_id)
        return get_response
    except Exception as e:
        return(f"Failed to set charging profile {charge_point_id}: {e}")

#Done
@router.post("/chargepoints/{charge_point_id}/compositeschedule",
    summary="Get Composite Schedule of a Charge Point. The schedule referes to the Charging Profile schedule.")
async def charging_profile(charge_point_id: str):
    """
    Get Composite Schedule sends all the Charging Profile Schedule of a Charge Point.
    """
    try:
        get_response = await cpo.get_schedule(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to set charging profile {charge_point_id}: {e}")

#Done
@router.post("/chargepoints/{charge_point_id}/chargingprofile/clear/{connector_id}",
    summary="Clear Charging Profile erases a Charging Profile of a Charge Point.")
async def clear_charging_profile(charge_point_id: str, connector_id:int):
    """
    Clear Charging Profile erases the Charging Profile of a specific ID.
    """
    try:
        get_response = await cpo.clear_charging_profile(charge_point_id,)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

#Done
@router.post("/chargepoints/{charge_point_id}/clearcache",
    summary="Clear Cache erases the list of previous authorized users of a Charge Point.")
async def clear_cache(charge_point_id: str):
    """
    Clear Cache erases the Local Authorization Cache which is stored locally in the Charge Point
    """
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

#Done
@router.post("/chargepoints/{charge_point_id}/reservation",
    summary="Reserve a connector to an ID.")
async def reservation(charge_point_id: str):
    """
    Reservation allows an ID to reserve a Charge Point connector for a period of time
    """
    try:
        get_response = await cpo.reserve(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

#Done
@router.post("/chargepoints/{charge_point_id}/reservation/cancel",
    summary="Cancel a previous reservation.")
async def cancel_reservation(charge_point_id: str, reservation_id: int):
    """
    Cancel Reservation erases a pervious reservation ID.
    """
    try:
        get_response = await cpo.cancel_reservation(charge_point_id, reservation_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

#Done
@router.post("/chargepoints/{charge_point_id}/datatransfer",
    summary="Send data to Charge Point that is not supported by OCPP.")
async def data_transfer(charge_point_id: str):
    """
    Data Transfer sends a message not supported by OCPP to the Charge Point.
    """
    try:
        get_response = await cpo.data_transfer(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/clearmessagedisplay")
async def clear_message_display(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/clearedlimit")
async def cleared_charging_limit(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/clearmonitoring")
async def clear_variable_monitoring(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/costupdated")
async def cost_updated(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/customerinfo")
async def cumstomer_info(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/deletecertification")
async def delete_certification(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/get15118")
async def get_15118_certification(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/getbasereport")
async def get_base_report(charge_point_id: str, request_id: int, report_base: ReportBaseType):
    try:
        get_response = await cpo.get_base_report(charge_point_id, request_id, report_base)
        return get_response
    except Exception as e:
        return(f"Failed to get base report from charger {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/getcertificatestatus")
async def get_certificate_status(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/getchargingprofiles")
async def get_charging_profiles(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/getdisplaymessage")
async def get_display_message(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/getistalledcertificate")
async def get_installed_certificate(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/getlog")
async def get_log(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/getmonitoringreport")
async def get_monitoring_report(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/getreport")
async def get_report(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/gettransactionstatus")
async def get_transaction_status(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.get("/chargepoints/{charge_point_id}/variables")
async def get_variables(charge_point_id: str):
#get_variable_data: List[GetVariableDataType]
    try:
        get_response = await cpo.get_variable(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to get variable data from charger {charge_point_id}: {e}")

#Done
@router.put("/chargepoints/{charge_point_id}/variables")
async def set_variables(charge_point_id: str, set_variable_data: List[SetVariableDataType]):
    try:
        get_response = await cpo.set_variable(charge_point_id, set_variable_data)
        return get_response
    except Exception as e:
        return(f"Failed to set variables of charger {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/installcertificate")
async def install_certificate(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/logstatusnotification")
async def log_status_notification(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/notifycharginglimit")
async def notify_charging_limit(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/notifycustomerinformation")
async def notify_customer_information(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/notifydisplaymessages")
async def notify_display_messages(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/notifyevchargingneeds")
async def notify_ev_charging_needs(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/notifyevchargingschedule")
async def notify_ev_charging_schedule(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/notifyevent")
async def notify_event(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/notifymonitoringreport")
async def notify_monitoring_report(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/notifyreport")
async def notify_report(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/publishfirmware")
async def publish_firmware(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/publishfirmwarestatus")
async def publish_firmware_status_notification(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/reportchargingprofiles")
async def report_charging_profiles(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/reservationstatusupdate")
async def reservation_status_update(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/securityeventnotification")
async def security_event_notification(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/setdisplaymessage")
async def set_display_message(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/setmonitoringbase")
async def set_monitoring_base(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/setmonitoringlevel")
async def set_monitoring_level(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

#Done
@router.post("/chargepoints/{charge_point_id}/setnetworkprofile")
async def set_network_profile(charge_point_id: str, configuration_slot: int, connection_data: NetworkConnectionProfileType):
    try:
        get_response = await cpo.set_network_profile(charge_point_id, configuration_slot, connection_data)
        return get_response
    except Exception as e:
        return(f"Failed to set network profile of charger {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/setvariablemonitoring")
async def set_variable_monitoring(charge_point_id: str,):
    try:
        get_response = await cpo.set_variable(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/signcertificate")
async def sign_certificate(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")

@router.post("/chargepoints/{charge_point_id}/unpublishfirmware")
async def unpublish_firmware(charge_point_id: str):
    try:
        get_response = await cpo.clear_cache(charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")