from enum import Enum
from typing import Dict, List, Optional, Union
from datetime import datetime
from ocpp.v16.enums import *

from pydantic import BaseModel

class RfidTagCreate(BaseModel):
    rfid_length: int
    rfid: str

class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    mobile: str
    rfid: RfidTagCreate
    password: str

class Auth(BaseModel):
    email: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

class ChargePointSessions(BaseModel):
    id_tag: str
    charge_point_id: Optional[str] = None
    connector_id: Optional[int] = None
    meter_start: Optional[int] = None
    timestamp: Optional[datetime] = None
    reservation_id: Optional[int] = None

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
     type: ResetType

class TokenRefresh(BaseModel):
    token: Optional[str] = None
    password: Optional[str] = None


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

class Trigger(str, Enum):
    status_notification = "StatusNotification"
    meter_values = "MeterValues"
    diagnostics_status = "DiagnosticsStatusNotification"
    firmware_status = "FirmwareStatusNotification"

class IdTagStatus(str, Enum):
    accepted = "Accepted"
    blocked = "Blocked"
    expired = "Expired"
    invalid ="Invalid"
    concurrent_tx = "ConcurrentTx"

class UpdateType(str, Enum):
    full = "Full"
    differential = "Differential"

class IdTagInfo(BaseModel):
    expiry_date: datetime
    parent_id_tag: str
    status: IdTagStatus

class LocalAuthorizationList(BaseModel):
    id_tag: str
    id_tag_info: IdTagInfo

class LocalList(BaseModel):
    list_version: int
    local_authorization_list: List[LocalAuthorizationList] = None
    update_type: UpdateType

class ChargingSchedulePeriod(BaseModel):
    start_period: int
    limit: float
    number_phases: Optional[int] = None

class ChargingSchedule(BaseModel):
    duration: Optional[int] = None
    start_schedule: Optional[str] = None
    charging_rate_unit: ChargingRateUnitType
    charging_schedule_period: list[ChargingSchedulePeriod]
    min_charging_rate: Optional[float] = None

class CompositeSchedule(BaseModel):
    connector_id: int
    duration: int
    charging_rate_unit: Optional[ChargingRateUnitType] = None

class csChargingProfile(BaseModel):
    """
    A ChargingProfile consists of a ChargingSchedule, describing the
    amount of power or current that can be delivered per time interval.
    """

    charging_profile_id: int
    transaction_id: Optional[int] = None
    stack_level: int
    charging_profile_purpose: ChargingProfilePurposeType
    charging_profile_kind: ChargingProfileKindType
    recurrency_kind: Optional[RecurrencyKind] = None
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None
    charging_schedule: ChargingSchedule

class ChargingProfile(BaseModel):
    connector_id: int
    cs_charging_profile: csChargingProfile

class ClearChargingProfile(BaseModel):
    id: int
    connector_id: int
    charging_profile_purpose: ChargingProfilePurposeType
    stack_level: int

class Reservation(BaseModel):
    connector_id: int
    expiry_date: datetime
    id_tag: str
    reservation_id: int
    parent_id: str

class Diagnostics(BaseModel):
    location: str
    retries: Optional[int] = None
    retry_interval: Optional[int] = None
    start_time: Optional[datetime] = None
    stop_time: Optional[datetime] = None

class UpdateFirmware(BaseModel):
    location: str
    retrieve_data: datetime
    retries: Optional[int] = None
    retry_interval: Optional[int] = None

class DataTransfer(BaseModel):
    vendor_id: str
    message_id: Optional[str] = None
    data: Optional[str] = None