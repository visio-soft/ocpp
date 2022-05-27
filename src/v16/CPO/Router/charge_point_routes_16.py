from v16.CPO.Schemas import schemas
from resources.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from v16.CPO.ChargePointOp.cpo_class import ChargePoint
from v16.CPO.Websocket.websocket import WebsocketAdapter
from v16.CPO.ChargePointOp.charge_point_operator import CentralSystem
from ocpp.v16.enums import AvailabilityType, ResetType
from typing import List
from v16.CPO.CRUD import crud
import asyncio


router = APIRouter(tags=["Charge Point"])
cpo = CentralSystem()

#Done
@router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """
    Function to connect a Charge Point to the CPO through websockets
    """
    print(websocket.url.path)
    try:
        await websocket.accept(subprotocol="ocpp1.6")
        charge_point_id = websocket.url.path.strip("ocpp/16/api/v16")
        cp = ChargePoint(charge_point_id, WebsocketAdapter(websocket))
        queue = cpo.register_charger(cp)
        await queue.get()

    except WebSocketDisconnect:
        socket = WebsocketAdapter()
        await socket.disconnect(websocket)

#Done
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

#Done"
@router.put("/chargepoints/{charge_point_id}/connectors/{connector_id}/remotestart",
    summary="Remotely start a Charging Session from an application connected to the platform.")
async def remote_start( charge_point_id: str, id_tag: str, connector_id: int = None, db: Session = Depends(get_db)):
    """
    Start a Charging Session.
    """
    charging = await crud.start_check_ongoing_charging_session(db, charge_point_id, id_tag)
    if not charging:
        try:
            get_response = await cpo.start_remote(charge_point_id, id_tag, connector_id)
            print(f" The response from charger {get_response}")
            return get_response
        except Exception as e:
            return(f"Failed to start remote charging {charge_point_id}: {e}")
    else:
        return(f"This ID has already an ongoing transaction.")

#Done"
@router.put("/chargepoints/{charge_point_id}/remotestop",
    summary="Remotely stops a Charging Session from an application connected to the platform.")
async def remote_stop(charge_point_id: str, transaction_id: int, db: Session = Depends(get_db)):
    """
    Stop a Charging Session
    """
    charging = await crud.stop_check_ongoing_charging_session(db, charge_point_id, transaction_id)
    if charging:
        try:
            get_response = await cpo.stop_remote(charge_point_id, transaction_id)
            print(f" The response from charger {get_response}")
            return get_response
        except Exception as e:
            return(f"Failed to stop remote charging {charge_point_id}: {e}")
    else:
        return("Transaction ID could not be found.")

#Done
@router.get("/chargepoints/{charge_point_id}/configure",
    summary="Get configurations from a Charge Point. Specify with Configuration Key to get the value of wanted configuration.")
async def get_connector_config(charge_point_id:str, key: schemas.ConfigurationKey = None):
    """
    GET Configurations set to a connector
    """
    try:
        get_response = await cpo.get_configuration(charge_point_id, key)
        return get_response
    except Exception as e:
        return(f"Failed to get configuration of charge point {charge_point_id}: {e}")

#Done
@router.put("/chargepoints/{charge_point_id}/configure",
    summary="Remotely configure a Charge Point.")
async def put_connector_config(charge_point_id: str, key: schemas.ConfigurationKey, value: str):
    """
    PUT a request to change Configuration within the ConfigurationKey Enum
    """
    try:
        get_response = await cpo.change_configuration(charge_point_id, key, value)
        print(f" The response from charger {get_response}")
        return get_response
    except Exception as e:
        return(f"Failed to change configuration of charge point {charge_point_id}: {e}")

#Done
@router.put("/chargepoints/{charge_point_id}/connectors/{connector_id}/availability",
    summary="Change the availability of a Charge Point to either 'Operative' or 'Inoperative'")
async def put_connector_config(charge_point_id: str, connector_id: int, type: AvailabilityType):
    """
    Change Availability
    """
    try:
        get_response = await cpo.change_availability(charge_point_id, connector_id, type)
        print(f"The response from charger {get_response}")
        return get_response
    except Exception as e:
        return(f"Failed to change availability of charge point {charge_point_id}: {e}")

#Done
@router.put("/chargepoints/{charge_point_id}/reset",
    summary="Restart a Charge Point")
async def reset(charge_point_id: str, type: ResetType):
    """
    Reset Charge Point
    """
    try:
        get_response = await cpo.reset(charge_point_id, type)
        print(f" The response from charger {get_response}")
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
        asyncio.wait(1)
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

#Done
@router.post("/chargepoints/{charge_point_id}/updatefirmware",
    summary="Updates the firmware of the Charge Point. Sends the location of which the Charge Point can download the updated firmware.")
async def update_firmware(charge_point_id:str, request: schemas.UpdateFirmware):
    """
    Update the firmware of a Charge Point.
    """
    try:
        get_response = await cpo.update_firmware(charge_point_id, request.location, request.retrieve_data, 
            request.retries, request.retry_interval)
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
async def get_diagnostics(charge_point_id:str, request: schemas.Diagnostics):
    """
    Get diagnostics of a specific location of a Charge Point
    """
    try:
        get_response = await cpo.get_diagnostics(charge_point_id, request.location, request.retries, request.retry_interval, request.start_time, 
            request.stop_time)
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
async def get_local_list(charge_point_id: str, db: Session = Depends(get_db)):
    """
    Get the local authorization list version.
    """
    try:
        get_response = await cpo.get_local_list(charge_point_id)
        #local_list = await crud.get_local_list(db, charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to get local list {charge_point_id}: {e}")

#Done // Needs DB connection
@router.post("/chargepoints/{charge_point_id}/locallist",
    summary="Send a Local Authorization List to Charge Point.")
async def send_local_list(charge_point_id: str, request: schemas.LocalList):
    try:
        get_response = await cpo.send_local_list(charge_point_id, request.list_version, request.update_type, request.local_authorization_list)
        #local_list = await crud.send_local_list(db, charge_point_id)
        return get_response
    except Exception as e:
        return(f"Failed to send local list {charge_point_id}: {e}")

#Proper data type needed for cs_charging_profile
@router.post("/chargepoints/{charge_point_id}/chargingprofile/{connector_id}",
    summary="Set a Charging Profile of a Charge Point. Control the maximum output of a Charge Point during a period of time.")
async def charging_profile(charge_point_id: str, connector_id: int, request: schemas.SetChargingProfile):
    """
    Set Charging Profile allows Charge Point to set maximum "A" or "W" during a period of time.
    """
    try:
        get_response = await cpo.set_charging_profile(charge_point_id, connector_id, request.cs_charging_profile)
        return get_response
    except Exception as e:
        return(f"Failed to set charging profile {charge_point_id}: {e}")

#Done
@router.post("/chargepoints/{charge_point_id}/compositeschedule",
    summary="Get Composite Schedule of a Charge Point. The schedule referes to the Charging Profile schedule.")
async def charging_profile(charge_point_id: str, request: schemas.CompositeSchedule):
    """
    Get Composite Schedule sends all the Charging Profile Schedule of a Charge Point.
    """
    try:
        get_response = await cpo.get_schedule(charge_point_id, request.connector_id, request.duration, request.charging_rate_unit)
        return get_response
    except Exception as e:
        return(f"Failed to set charging profile {charge_point_id}: {e}")

#Done
@router.post("/chargepoints/{charge_point_id}/chargingprofile/clear/{connector_id}",
    summary="Clear Charging Profile erases a Charging Profile of a Charge Point.")
async def clear_charging_profile(charge_point_id: str, connector_id:int, request: schemas.ClearChargingProfile):
    """
    Clear Charging Profile erases the Charging Profile of a specific ID.
    """
    try:
        get_response = await cpo.clear_charging_profile(charge_point_id, request.id, connector_id, request.charging_profile_purpose,
            request.stack_level)
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
async def reservation(charge_point_id: str, request: schemas.Reservation):
    """
    Reservation allows an ID to reserve a Charge Point connector for a period of time
    """
    try:
        get_response = await cpo.reserve(charge_point_id, request.connector_id, request.expiry_date, request.id_tag, request.reservation_id,
            request.parent_id)
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
async def data_transfer(charge_point_id: str, request: schemas.DataTransfer):
    """
    Data Transfer sends a message not supported by OCPP to the Charge Point.
    """
    try:
        get_response = await cpo.data_transfer(charge_point_id, request.vendor_id, request.message_id, request.data)
        return get_response
    except Exception as e:
        return(f"Failed to clear charging profile {charge_point_id}: {e}")