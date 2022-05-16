from webbrowser import get
from v16.CPO import schemas
from database.database import get_db
from database import models
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from v16.cpo_class import ChargePoint
from v16.CPO.classes import WebsocketAdapter
from v16.charge_point_operator import CentralSystem
from ocpp.v16.enums import AvailabilityType
from typing import List
from v16.CPO import crud
import asyncio


router = APIRouter(tags=["Charge Point"])
cpo = CentralSystem()


"""
Function to connect a Charge Point to the CPO through websockets
Done
"""

@router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
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
Done
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
Done
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
Done
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

@router.put("/chargepoints/{charge_point_id}/connectors/{connector_id}/remotestart")
async def remote_start( charge_point_id: str, id_tag: str, connector_id: int = None):
    try:
        get_response = await cpo.start_remote(charge_point_id, id_tag, connector_id)
        print(f" The response from charger {get_response}")
        return get_response
    except Exception as e:
        return(f"Failed to start remote charging {charge_point_id}: {e}")


"""
Stop a Charging Session
Done / Need to fix transaction id
"""

@router.put("/chargepoints/{charge_point_id}/connectors/{connector_id}/remotestop")
async def remote_stop(charge_point_id: str, connector_id: int, transaction_id: int):
    try:
        get_response = await cpo.stop_remote(charge_point_id, connector_id, transaction_id)
        print(f" The response from charger {get_response}")
        return get_response
    except Exception as e:
        return(f"Failed to stop remote charging {charge_point_id}: {e}")


"""
GET Configurations set to a connector
Done
"""

@router.get("/chargepoints/{charge_point_id}/configure")
async def get_connector_config( charge_point_id:str, key: schemas.ConfigurationKey = None):
    key = [key]
    try:
        get_response = await cpo.get_configuration(charge_point_id, key)
        print(f" The response from charger {get_response}")
        return get_response
    except Exception as e:
        return(f"Failed to get configuration of charge point {charge_point_id}: {e}")

"""
PUT a request to change Configuration within the ConfigurationKey Enum
Done
"""

@router.put("/chargepoints/{charge_point_id}/configure")
async def put_connector_config(charge_point_id: str, key: str, value: int):
    try:
        get_response = await cpo.change_configuration(charge_point_id, key, value)
        print(f" The response from charger {get_response}")
        return get_response
    except Exception as e:
        return(f"Failed to change configuration of charge point {charge_point_id}: {e}")

"""
Change Availability
Done
"""

@router.put("/chargepoints/{charge_point_id}/connectors/{connector_id}/availability")
async def put_connector_config(charge_point_id: str, connector_id: int, type: AvailabilityType):
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
async def reset(charge_point_id: str, request: schemas.Reset):
    type = request.type
    try:
        get_response = await cpo.reset(charge_point_id, type)
        print(f" The response from charger {get_response}")
        return get_response
    except Exception as e:
        return(f"Failed to reset charge point {charge_point_id}: {e}")


"""
GET a Status Notification from a Charge Point by sending a Trigger Message
Done
"""

@router.get("/chargepoints/{charge_point_id}/status", response_model=schemas.ChargePointStatus)
async def get_status(charge_point_id:str, connector_id: int = None, db: Session = Depends(get_db)):
    try:
        get_response = await cpo.trigger_status(charge_point_id, connector_id)
        print(f" The response from charger {get_response}")
        asyncio.wait(1)
        status = await crud.get_status(db, charge_point_id)
        return status
    except Exception as e:
        return(f"Failed to get status of charge point {charge_point_id}: {e}")

"""
GET Meter Values from a Charge Point by sending a Trigger Message
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

"""Firmware and Diagnostics Notification commented out since its not essential in version"""

# """
# Get Firmware Notification Message of Charge Point
# GET a Status Notification from a Charge Point by sending a Trigger Message
# Done
# """

# @router.get("/chargepoints/{charge_point_id}/firmwarestatus")
# async def get_firmware(charge_point_id:str, connector_id: int = None):
#     try:
#         get_response = await cpo.trigger_frimware_status(charge_point_id, connector_id)
#         print(f" The response from charger {get_response}")
#         return get_response
#     except Exception as e:
#         return(f"Failed to GET Status: {e}")

# """
# Get Diagnostics Message of Charge Point
# GET a Status Notification from a Charge Point by sending a Trigger Message
# Done
# """

# @router.get("/chargepoints/{charge_point_id}/diagnosticsnotification")
# async def get_diagnostics(charge_point_id:str, connector_id: int = None):
#     try:
#         get_response = await cpo.trigger_diagnostics(charge_point_id, connector_id)
#         print(f" The response from charger {get_response}")
#         return get_response
#     except Exception as e:
#         return(f"Failed to GET Status: {e}")

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
Ask Charge Point to send a "is alive" heartbeat signal. Should be used if 
heartbeat signal is not sent during regular interval.
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

# @router.get("/chargepoints/{charge_point_id}/locallist")
# async def get_local_list(charge_point_id: str, db: Session = Depends(get_db)):
#     try:
#         get_response = cpo.get_local_list(charge_point_id)
#         local_list = await crud.get_local_list(db, charge_point_id)
#         return get_response, local_list
#     except Exception as e:
#         return(f"Failed to get charging session {charge_point_id}: {e}")

# @router.post("/chargepoints/{charge_point_id}/locallist")
# async def get_local_list(charge_point_id: str, request: schemas.LocalList, db: Session = Depends(get_db)):
#     try:
#         get_response = cpo.send_local_list(charge_point_id, request.list_version, request.local_authorization_list, request.update_type)
#         local_list = await crud.send_local_list(db, charge_point_id)
#         return get_response, local_list
#     except Exception as e:
#         return(f"Failed to get charging session {charge_point_id}: {e}")


# """Schedule, Register and Connector Configuration commented out since it's not in first version."""

#"""
#Register a Charge Point
#PUT a Register request and store in database
#Done
#"""

# @router.put("/chargepoints/{charge_point_id}/register")
# async def register(charge_point_id: str, charge_point_serial_number: str,
# request: schemas.ChargePointRegistrationInfo, db: Session = Depends(get_db)):
#     if charge_point_serial_number == models.ChargePoint.charge_point_serial_number:
#         update_charge_point = models.ChargePoint(charge_point_id=request.charge_point_id, password=Hash.bcrypt(request.password),
#             charge_point_name = request.charge_point_name)
#         db.commit()
#         db.refresh(update_charge_point)
#         return update_charge_point

# """
# Unregister a Charge Point
# PUT a request to Unregister a Charge Point
# Done
# """

#@router.put("/chargepoints/{charge_point_id}/unregister")
#async def put_unregister(request: schemas.ChargePointAuth, charge_point_id: str, db: Session = Depends(get_db),
#get_current_user: schemas.User = Depends(oauth2.get_current_user)):
#    charge_point = db.query(models.ChargePoint).filter(models.ChargePoint.charge_point_id ==
#         request.charge_point_id, models.ChargePoint.password == request.password).delete(synchronize_session=False)
#    db.commit()
#    return {'status': 'Charge Point deleted'}

# """
# Get Charge Point Schedule
# GET all the Schedules registered to a Charge Point
# Under development
# Not Essential
# """

# @router.get("/chargepoints/{charge_point_id}/schedule", response_model=schemas.Schedule)
# async def get_schedule(charge_point_id: str, request: schemas.Schedule, db: Session = Depends(get_db)):
#     get_schedule = db.query(models.Schedule).all()
#     return get_schedule


# """
# Register a Schedule
# PUT a Schedule with charging behavior of a Charge Point
# Not Started
# Not Essential
# """

# @router.put("/chargepoints/{charge_point_id}/schedule")
# async def put_schedule(charge_point_id: str, request: schemas.Schedule, db: Session = Depends(get_db)):
#     db.query(models.Schedule).filter(models.Schedule.id ==
#         id).update(request)
#     db.commit()
#     return {'status': "Accepted"}


# """
# Register a Schedule
# POST a Schedule with charging behavior of a Charge Point
# Not started
# Not Essential
# """

# @router.post("/chargepoints/{charge_point_id}/schedule")
# async def post_schedule(charge_point_id: str, request: schemas.Schedule, db: Session = Depends(get_db)):
#     new_schedule = models.Schedule(
#         charge_point_id=request.charge_point_id,
#         name=request.name,
#         active=request.active,
#         start_hours=request.start_hours,
#         start_minutes=request.start_minutes,
#         end_hours=request.end_hours,
#         end_minutes=request.end_minutes,
#         time_zone=request.time_zone,
#         monday=request.monday,
#         tuesday=request.tuesday,
#         wednesday=request.wednesday,
#         thursday=request.thursday,
#         friday=request.friday,
#         saturday=request.saturday,
#         sunday=request.sunday,
#         connector_id_list=request.connector_id_list
#     )
#     db.add(new_schedule)
#     db.commit()
#     db.refresh(new_schedule)
#     return new_schedule


# """
# Get Schedule
# GET a specific Schedule of a Charge Point
# Not started
# Not Essential
# """

# @router.get("/chargepoints/{charge_point_id}/schedule/{schedule_id}", response_model=schemas.Schedule)
# async def get_schedule_id(charge_point_id: str, schedule_id: int, request: schemas.Schedule, db: Session = Depends(get_db)):
#     get_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
#     return get_schedule


# """
# Delete a Schedule
# Not started
# Not Essential
# """

# @router.delete("/chargepoints/{charge_point_id}/schedule/{schedule_id}")
# async def get_schedule_id(charge_point_id: str, schedule_id: int, request: schemas.Schedule, db: Session = Depends(get_db)):
#     schedule = db.query(models.Schedule).filter(models.Schedule.id ==
#          schedule_id).delete(synchronize_session=False)
#     db.commit()
#     return {"status": "Schedule Deleted"}


# """
# Get Charge Point Configurations
# GET a specific Configuration of a Charge Point
# Done
# """

# @router.get("/chargepoints/{charge_point_id}/configure", response_model=schemas.Configuration)
# async def get_config(charge_point_id:str, key: schemas.ConfigurationKey = None):
#     key = [key]
#     try:
#         get_response = await cpo.get_configuration(charge_point_id, key)
#         print(f" The response from charger {get_response}")
#         return get_response
#     except Exception as e:
#         return(f"Failed to get configuration: {e}")


# """
# Configure Charge Point
# PUT a Configure to a Charge Point within the ConfigurationKey Enum
# Done
# """

# @router.put("/chargepoints/{charge_point_id}/configure")
# async def put_config(request: schemas.Configuration, charge_point_id:str,
# get_current_user: schemas.User = Depends(oauth2.get_current_user)):
#     try:
#         get_response = await cpo.change_configuration(charge_point_id, request.key, request.value)
#         print(f" The response from charger {get_response}")
#         return get_response
#     except Exception as e:
#         return(f"Failed to change configuration: {e}")