from v201.CPO import schemas, oauth2
from resources import models
from resources.database import get_db
from sqlalchemy.orm import Session
from v201.CPO.hashing import Hash
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from v201.cpo_class_v201 import ChargePoint
from v201.CPO.classes import WebsocketAdapter
from v201.charge_point_operator_v201 import CentralSystem
from ocpp.v201.enums import *
from v201.CPO.hashing import Hash
from v201.CPO import crud
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
        charge_point_id = websocket.url.path.strip("/ocpp/201")
        cp = ChargePoint(charge_point_id, WebsocketAdapter(websocket))
        queue = cpo.register_charger(cp)
        await queue.get()

    except WebSocketDisconnect:
        socket = WebsocketAdapter()
        await socket.disconnect(websocket)


"""
GET a Charge Point connected to the CPO
Done
"""

@router.get("/chargepoints/{charge_point_id}", response_model=List[schemas.ChargePoint])
async def get_charge_point(charge_point_id: str, db: Session = Depends(get_db)):
    try:
        charge_point = await crud.get_charge_point(db, charge_point_id)
        return charge_point
    except Exception as e:
        return(f"Failed to get charging session {charge_point_id}: {e}")

"""
GET all active Charging Sessions on a Charge Point
Under development
"""

@router.get("/chargepoints/{charge_point_id}/chargingsessions", response_model=List[schemas.ChargePointSessions], response_model_exclude={"connector_id"})
async def get_charge_point_session(charge_point_id: str, db: Session = Depends(get_db)):
    try:
        charge_point_session = await crud.get_charge_point_sessions(db, charge_point_id)
        return charge_point_session
    except Exception as e:
        return(f"Failed to get charging session {charge_point_id}: {e}")

"""
GET a specific Charging Session with session ID
Under development
"""

@router.get("/chargepoints/{charge_point_id}/chargingsessions/{transaction_id}", response_model=schemas.ChargePointSessions)
async def get_charge_point_session_id(charge_point_id: str, transaction_id: int, db: Session = Depends(get_db)):
    try:    
        charge_point_session = await crud.get_charge_point_session(db, charge_point_id, transaction_id)
        return charge_point_session
    except Exception as e:
        return(f"Failed to get charging session {charge_point_id}: {e}")


"""
GET the Charging Sessions relevant to a connector
Under development
"""

@router.get("/chargepoints/{charge_point_id}/connectors/{connector_id}/chargingsessions", response_model=List[schemas.ChargePointSessions])
async def get_connector_session(charge_point_id: str, connector_id: int, db: Session = Depends(get_db)):
    try:
        charge_point_session = await crud.get_charge_point_sessions_connector(db, charge_point_id, connector_id)
        return charge_point_session
    except Exception as e:
        return(f"Failed to get charging session {charge_point_id}: {e}")


"""
Start a Charging Session
Done
"""

@router.put("/chargepoints/{charge_point_id}/remotestart")
async def remote_start( charge_point_id: str,
request: schemas.RequestStartTransaction):
    try:
        get_response = await cpo.request_start(charge_point_id, request.id_token, request.remote_start_id, request.evse_id)
        return get_response
    except Exception as e:
        return(f"Failed to start remote charging: {e}")


"""
Stop a Charging Session
Need Transaction ID Implemented
"""

@router.put("/chargepoints/{charge_point_id}/connectors/{connector_id}/remotestop")
async def remote_stop(charge_point_id: str, connector_id: int, transaction_id: str):
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

@router.put("/chargepoints/{charge_point_id}/reset")
async def reset(charge_point_id: str, request: schemas.Reset,
):
    type = request.type
    try:
        get_response = await cpo.reset(charge_point_id, type)
        print(f"==> The response from charger==> {get_response}")
        return get_response
    except Exception as e:
        return(f"Failed to start remote charging: {e}")


"""
GET a Status Notification from a Charge Point by sending a Trigger Message
Done
"""

@router.get("/chargepoints/{charge_point_id}/status", response_model=schemas.ChargePointStatus)
async def get_status(charge_point_id:str, connector_id: int = None, db: Session = Depends(get_db)):
    try:
        get_response = await cpo.trigger_status(charge_point_id, connector_id)
        print(f" The response from charger {get_response}")
        status = await crud.get_status(db, charge_point_id)
        return status
    except Exception as e:
        return(f"Failed to get status of charge point {charge_point_id}: {e}")

"""
GET a Status Notification from a Charge Point by sending a Trigger Message
Done
"""

@router.post("/chargepoints/{charge_point_id}/metervalues")
async def get_meter(charge_point_id:str, connector_id: int = None):
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

"""
Ask Charge Point to send a "is alive" heartbeat signal. Should be used if heartbeat signal
is not sent during regular interval.
Done
"""

@router.post("/chargepoints/{charge_point_id}/heartbeat")
async def get_heartbeat(charge_point_id:str, connector_id: int = None):
    try:
        get_response = await cpo.trigger_heartbeat(charge_point_id, connector_id )
        print(f" The response from charger {get_response}")
        return get_response
    except Exception as e:
        return(f"Failed to GET Status: {e}")

"""
Unlocks Connector if cable is removable. Should be used if cable is not automatically removed
as the transaction ends or another error occurs.
Done
"""

@router.put("/chargepoints/{charge_point_id}/unlock")
async def put_unlock(charge_point_id:str, connector_id: int):
    try:
        get_response = await cpo.unlock_connector(charge_point_id, connector_id)
        print(f" The response from charger {get_response}")
        return get_response
    except Exception as e:
        return(f"Failed to unlock connector: {e}")




"""
GET all Charge Points that are connected to the CPO
Done
"""

@router.get("/chargepoints/owned", response_model=schemas.ChargePoint)
async def get_owned(request: schemas.ChargePoint, db: Session = Depends(get_db)):
    try:
        charge_points = db.query(models.ChargePoint).all()
        return charge_points
    except Exception as e:
        return(f"Failed to get charging session: {e}")
