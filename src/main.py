from fastapi import FastAPI
from resources import models
from resources.database import engine
from v16.CPO.Router import authentication_16, charge_point_routes_16
from v201.CPO.Router import authentication_201, charge_point_routes_201
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Drifter World API", description="Welcome to Drifter World Charge Point Operator API")

app16 = FastAPI(title="Drifter World API",version="v16", description="v16 supports Drifter Charge Point Operator version 1.6 of OCPP")
app201 = FastAPI(title="Drifter World API",version="v201", description="v201 supports Drifter Charge Point Operator version 2.0.1 of OCPP")
app.mount("/ocpp/16", app16)
app.mount("/ocpp/201", app201)

app16.include_router(authentication_16.router, prefix="/api")
app201.include_router(authentication_201.router, prefix="/api")
app16.include_router(charge_point_routes_16.router, prefix="/api")
app201.include_router(charge_point_routes_201.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)