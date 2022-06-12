from typing import Dict, List, Optional
from ocpp.v201.datatypes import *
from ocpp.v201 import enums
from enum import Enum
from datetime import datetime
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class Auth(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

class ChargePoint(BaseModel):
    id: int
    charge_point_id: str
    charge_point_vendor: str
    charge_point_model: str
    charge_point_serial_number: Optional[str] = None
    firmware_version: Optional[str] = None
    charge_box_serial_number: Optional[str] = None
    iccid: Optional[str] = None
    imsi: Optional[str] = None
    meter_serial_number: Optional[str] = None
    meter_type: Optional[str] = None
    heartbeat: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class ChargePointStatus(BaseModel):
    charge_point_id: str
    connector_id: int
    status: str
    error_code: str
    status_timestamp: datetime
    info: Optional[str] = None
    vendor_id: Optional[str] = None
    vendor_error_code: Optional[str] = None

    class Config:
        orm_mode = True

class MeterValues(BaseModel):
    id: int
    transaction_id: int
    charge_point_id: str
    connector_id: Optional[int]
    timestamp: datetime
    measurand: str
    value: str
    context: Optional[str]
    format: Optional[str]
    phase: Optional[str]
    location: Optional[str]
    unit: Optional[str]

    class Config:
        orm_mode = True

class ChargePointSessions(BaseModel):
    transaction_id: int
    charge_point_id: Optional[str] = None
    connector_id: Optional[int] = None
    id_tag: Optional[str] = None
    meter_start: Optional[int] = None
    timestamp: Optional[datetime] = None
    reservation_id: Optional[int] = None

    class Config:
        orm_mode = True

class ConfigurationKey(str, Enum):
    """
    Configuration Key Names.
    """

    # 9.1 Core Profile
    allow_offline_tx_for_unknown_id = "AllowOfflineTxForUnknownId"
    authorization_cache_enabled = "AuthorizationCacheEnabled"
    authorize_remote_tx_requests = "AuthorizeRemoteTxRequests"
    blink_repeat = "BlinkRepeat"
    clock_aligned_data_interval = "ClockAlignedDataInterval"
    connection_time_out = "ConnectionTimeOut"
    connector_phase_rotation = "ConnectorPhaseRotation"
    connector_phase_rotation_max_length = "ConnectorPhaseRotationMaxLength"
    get_configuration_max_keys = "GetConfigurationMaxKeys"
    heartbeat_interval = "HeartbeatInterval"
    light_intensity = "LightIntensity"
    local_authorize_offline = "LocalAuthorizeOffline"
    local_pre_authorize = "LocalPreAuthorize"
    max_energy_on_invalid_id = "MaxEnergyOnInvalidId"
    meter_values_aligned_data = "MeterValuesAlignedData"
    meter_values_aligned_data_max_length = "MeterValuesAlignedDataMaxLength"
    meter_values_sampled_data = "MeterValuesSampledData"
    meter_values_sampled_data_max_length = "MeterValuesSampledDataMaxLength"
    meter_value_sample_interval = "MeterValueSampleInterval"
    minimum_status_duration = "MinimumStatusDuration"
    number_of_connectors = "NumberOfConnectors"
    reset_retries = "ResetRetries"
    stop_transaction_on_ev_side_disconnect = "StopTransactionOnEVSideDisconnect"
    stop_transaction_on_invalid_id = "StopTransactionOnInvalidId"
    stop_txn_aligned_data = "StopTxnAlignedData"
    stop_txn_aligned_data_max_length = "StopTxnAlignedDataMaxLength"
    stop_txn_sampled_data = "StopTxnSampledData"
    stop_txn_sampled_data_max_length = "StopTxnSampledDataMaxLength"
    supported_feature_profiles = "SupportedFeatureProfiles"
    supported_feature_profiles_max_length = "SupportedFeatureProfilesMaxLength"
    transaction_message_attempts = "TransactionMessageAttempts"
    transaction_message_retry_interval = "TransactionMessageRetryInterval"
    unlock_connector_on_ev_side_disconnect = "UnlockConnectorOnEVSideDisconnect"
    web_socket_ping_interval = "WebSocketPingInterval"

    # 9.2 Local Auth List Management Profile
    local_auth_list_enabled = "LocalAuthListEnabled"
    local_auth_list_max_length = "LocalAuthListMaxLength"
    send_local_list_max_length = "SendLocalListMaxLength"

    # 9.3 Reservation Profile
    reserve_connector_zero_supported = "ReserveConnectorZeroSupported"

    # 9.4 Smart Charging Profile
    charge_profile_max_stack_level = "ChargeProfileMaxStackLevel"
    charging_schedule_allowed_charging_rate_unit = "ChargingScheduleAllowedChargingRateUnit"
    charging_schedule_max_periods = "ChargingScheduleMaxPeriods"
    connector_switch_3to1_phase_supported = "ConnectorSwitch3to1PhaseSupported"
    max_charging_profiles_installed = "MaxChargingProfilesInstalled"

class Configuration(BaseModel):
    key: ConfigurationKey
    value: str

class GetConfig(BaseModel):
    key: ConfigurationKey
    
class Reset(BaseModel):
     type: enums.ResetType

class Trigger(str, Enum):
    status_notification = "StatusNotification"
    meter_values = "MeterValues"
    diagnostics_status = "DiagnosticsStatusNotification"
    firmware_status = "FirmwareStatusNotification"


class RequestStartTransaction(BaseModel):
    id_token: IdTokenType
    remote_start_id: int
    evse_id: int
    group_id_token: Optional[IdTokenType] = None
    charging_profile: Optional[ChargingProfileType] = None