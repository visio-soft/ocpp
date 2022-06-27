from sqlalchemy import Column, Float, Integer, String, Boolean, DateTime
from resources.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)

class Token(Base):
    __tablename__ = "token"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password = Column(String)
    token = Column(String)

"""
OCPP version 1.6 models
"""
class ChargePoint16(Base):
    __tablename__ = "charge_point_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    boot_timestamp = Column(DateTime)
    charge_point_vendor = Column(String)
    charge_point_model = Column(String)
    charge_point_serial_number = Column(String)
    firmware_version = Column(String)
    charge_box_serial_number = Column(String)
    iccid = Column(String)
    imsi = Column(String)
    meter_serial_number = Column(String)
    meter_type = Column(String)
    heartbeat_interval = Column(Integer)
    status = Column(String)

class StartTransaction16(Base):
    __tablename__ = "start_transaction_16"
    id = Column(Integer, primary_key=True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    id_tag= Column(String)
    transaction_id = Column(Integer)
    connector_id = Column(Integer)
    meter_start = Column(Integer)
    reservation_id = Column(String)
    expiry_date = Column(DateTime)
    parent_id_tag = Column(String)
    authorization_status = Column(String)


class StopTransaction16(Base):
    __tablename__ = "stop_transaction_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    transaction_id = Column(Integer)
    id_tag = Column(String)
    expiry_date = Column(DateTime)
    parent_id_tag = Column(String)
    authorization_status = Column(String)
    meter_stop = Column(Integer)
    reason = Column(String)
    measurand = Column(String) 
    value = Column(String)
    context = Column(String)
    format = Column(String)
    phase = Column(String)
    location = Column(String)
    unit = Column(String)

class ChargePointStatus16(Base):
    __tablename__ = "charge_point_status_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    connector_id = Column(Integer)
    status = Column(String)
    error_code = Column(String)
    info = Column(String)
    vendor_id = Column(String)
    vendor_error_code = Column(String)

class MeterValues16(Base):
    __tablename__ = "meter_values_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    transaction_id = Column(Integer)
    connector_id= Column(Integer)
    measurand = Column(String) 
    value = Column(String)
    context = Column(String)
    format = Column(String)
    phase = Column(String)
    location = Column(String)
    unit = Column(String)

class ClearCache16(Base):
    __tablename__ = "clear_cache_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    response_status = Column(String)

class LocalList16(Base):
    __tablename__ = "local_list_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    list_version = Column(Integer)
    id_tag = Column(String)
    expiry_date = Column(DateTime)
    parent_id_tag = Column(String)
    authorization_status = Column(String)
    update_type = Column(String)
    response_status = Column(String)

class Authorize16(Base):
    __tablename__ = "authorize_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    id_tag = Column(String)
    expiry_date = Column(DateTime)
    parent_id_tag = Column(String)
    authorization_status = Column(String)

class FirmwareStatusNotification16(Base):
    __tablename__ = "firmware_status_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    status = Column(String)

class DiagnosticsStatusNotification16(Base):
    __tablename__ = "diagnostics_status_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    status = Column(String)

class Configuration16(Base):
    __tablename__ = "configuration_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    key = Column(String)
    value = Column(String)
    response_status = Column(String)

class Availability16(Base):
    __tablename__ = "availability_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    connector_id = Column(Integer)
    type = Column(String)
    response_status = Column(String)

class Reservation16(Base):
    __tablename__ = "reservation_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    connector_id = Column(Integer)
    expiry_date = Column(DateTime)
    id_tag = Column(String)
    reservation_id = Column(Integer)
    parent_id_tag = Column(String)
    response_status = Column(String)

class CancelReservation16(Base):
    __tablename__ = "cancel_reservation_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    reservation_id = Column(Integer)
    response_status = Column(String)

class GetConfiguration16(Base):
    __tablename__ = "get_configuration_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    key = Column(String)
    readonly = Column(Boolean)
    value = Column(String)
    unknown_key = Column(String)

class GetCompositeSchedule16(Base):
    __tablename__ = "get_composite_schedule_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    connector_id = Column(Integer)
    duration = Column(Integer)
    charging_rate_unit = Column(String)
    schedule_start = Column(DateTime)
    start_schedule = Column(DateTime)
    start_period = Column(String)
    limit = Column(Integer)
    number_phases = Column(Integer)
    min_charging_rate = Column(Integer)
    response_status = Column(String)

class Trigger16(Base):
    __tablename__ = "trigger_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    requested_message = Column(String)
    connector_id = Column(Integer)
    response_status = Column(String)

class UpdateFirmware16(Base):
    __tablename__ = "update_firmware_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    location = Column(String)
    retrieve_date = Column(DateTime)
    retries = Column(Integer)
    retry_interval = Column(Integer)

class OperatorDataTransfer16(Base):
    __tablename__ = "operator_data_transfer_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    vendor_id = Column(String)
    message_id = Column(String)
    request_data = Column(String)
    response_data = Column(String)
    response_status = Column(String)

class ChargePointDataTransfer16(Base):
    __tablename__ = "charge_point_data_transfer_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    vendor_id = Column(String)
    message_id = Column(String)
    request_data = Column(String)
    response_data = Column(String)
    response_status = Column(String)

class GetDiagnostics16(Base):
    __tablename__ = "get_diagnostics_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    location = Column(String)
    retries = Column(Integer)
    retry_interval = Column(Integer)
    start_time = Column(DateTime)
    stop_time = Column(DateTime)
    filename = Column(String)

class ChargingProfile16(Base):
    __tablename__ = "charging_profile_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    transaction_id = Column(Integer)
    connector_id = Column(Integer)
    charging_profile_id = Column(Integer)
    stack_level = Column(Integer)
    charging_profile_purpose = Column(String)
    charging_profile_kind = Column(String)
    recurrency_kind = Column(String)
    duration = Column(Integer)
    start_schedule = Column(DateTime)
    charging_rate_unit = Column(String)
    start_period = Column(String)
    limit = Column(Float)
    number_phases = Column(Integer)
    min_charging_rate = Column(Float)
    valid_from = Column(DateTime)
    valid_to = Column(DateTime)
    response_status = Column(String)

class ClearChargingProfile16(Base):
    __tablename__ = "clear_charging_profile_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    charging_profile_id = Column(Integer)
    connector_id = Column(Integer)
    charging_profile_purpose = Column(String)
    stack_level = Column(Integer)
    response_status = Column(String)

class GetLocalListVersion16(Base):
    __tablename__ = "get_local_version_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    list_version = Column(Integer)

class Reset16(Base):
    __tablename__ = "reset_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    type = Column(String)
    response_status = Column(String)

class UnlockConnector16(Base):
    __tablename__ = "unlock_connector_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    connector_id = Column(Integer)
    response_status = Column(String)

class Heartbeat16(Base):
    __tablename__ = "heartbeat_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)

class RemoteStartTransaction16(Base):
    __tablename__ = "remote_start_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    id_tag = Column(String)
    connector_id = Column(Integer)
    charging_profile_id = Column(Integer)
    transaction_id = Column(Integer)
    stack_level = Column(Integer)
    charging_profile_purpose = Column(String)
    charging_profile_kind = Column(String)
    recurrency_kind = Column(String)
    duration = Column(Integer)
    valid_from = Column(DateTime)
    valid_to = Column(DateTime)
    start_schedule = Column(DateTime)
    charging_rate_unit = Column(String)
    start_period = Column(DateTime)
    limit = Column(Integer)
    number_phases = Column(Integer)
    min_charging_rate = Column(Integer)
    response_status = Column(String)

class RemoteStopTransaction16(Base):
    __tablename__ = "remote_stop_16"
    id = Column(Integer, primary_key=True, index=True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    transaction_id = Column(Integer)
    response_status = Column(String)


"""
OCPP version 2.0.1 models
"""
class ChargePoint201(Base):
    __tablename__ = "charge_point_201"
    charge_point_id = Column(String, primary_key=True, index=True)
    boot_timestamp = Column(DateTime)
    model = Column(String)
    vendor_name = Column(String)
    serial_number = Column(String)
    firmware_version = Column(String)
    iccid = Column(String)
    imsi = Column(String)
    boot_reason = Column(String)
    interval = Column(Integer)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)
    
class Heartbeat201(Base):
    __tablename__ = "heartbeat_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)

class Authorize201(Base):
    __tablename__ = "authorize_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    timestamp = Column(DateTime)
    id_token = Column(String)
    id_token_type = Column(String)
    certificate = Column(String)
    hash_algorithm = Column(String)
    issuer_name_hash = Column(String)
    issuer_key_hash = Column(String)
    serial_number = Column(String)
    responder_url = Column(String)
    certificate_status = Column(String)
    authorization_status = Column(String)
    cache_expiry_data = Column(DateTime)
    charging_priority = Column(Integer)
    language_1 = Column(String)
    evse_id = Column(Integer)
    language_2 = Column(String)
    group_id_token = Column(String)
    group_id_token_type = Column(String)
    message_format = Column(String)
    message_langauge = Column(String)
    message_content = Column(String)

class ClearedChargingLimit201(Base):
    __tablename__ = "cleared_charging_limit_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    timestamp = Column(DateTime)
    charging_limit_source = Column(String)
    evse_id = Column(Integer)

class FirmwareStatusNotification201(Base):
    __tablename__ = "firmware_status_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    timestamp = Column(DateTime)
    status = Column(String)
    request_id = Column(Integer)

class Get15118EVCertificate201(Base):
    __tablename__ = "get_15118_certificate_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    iso_15118_schema_version = Column(String)
    action = Column(String)
    exi_request = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)
    exi_response = Column(String)

class GetCertificateStatus201(Base):
    __tablename__ = "get_certificate_status_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    hash_algorithm = Column(String)
    issuer_name_hash = Column(String)
    issuer_key_hash = Column(String)
    serial_number = Column(String)
    responder_url = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)
    ocsp_result = Column(String)

class LogStatusNotification201(Base):
    __tablename__ = "log_status_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    status = Column(String)
    request_id = Column(Integer)

class MeterValue201(Base):
    __tablename__ = "meter_value_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    evse_id = Column(Integer)
    measurand = Column(String)
    value = Column(Integer)
    context = Column(String)
    phase = Column(String)
    location = Column(String)
    signed_meter_data = Column(String)
    signing_method = Column(String)
    encoding_method = Column(String)
    public_key = Column(String)
    unit = Column(String)
    multiplier = Column(Integer)

class NotifyChargingLimit201(Base):
    __tablename__ = "notify_charging_limit_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    evse_id = Column(Integer)
    charging_limit_source = Column(String)
    is_grid_critical = Column(Boolean)
    charging_schedule_id = Column(Integer)
    start_schedule = Column(DateTime)
    duration = Column(Integer)
    charging_rate_unit = Column(String)
    min_charging_rate = Column(Integer)
    start_period = Column(Integer)
    limit = Column(Integer)
    number_phases = Column(Integer)
    phases_to_use = Column(Integer)
    sales_tariff_id = Column(Integer)
    sales_tariff_description = Column(String)
    num_e_price_levels = Column(Integer)
    e_price_level = Column(Integer)
    relative_time_interval_start = Column(Integer)
    relative_time_interval_duration = Column(Integer)
    consumption_start_value = Column(Integer)
    cost_kind = Column(String)
    amount = Column(Integer)
    amount_multiplier = Column(Integer)

class NotifyCostumerInformation201(Base):
    __tablename__ = "notify_costumer_info_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    data = Column(String)
    tbc = Column(Boolean)
    seq_no = Column(Integer)
    generated_at = Column(DateTime)
    request_id = Column(Integer)

class NotifyDisplayMessage201(Base):
    __tablename__ = "notify_display_message_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    request_id = Column(Integer)
    tbc = Column(Boolean)
    message_id = Column(String)
    priority = Column(String)
    state = Column(String)
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    transaction_id = Column(String)
    message_format = Column(String)
    message_language = Column(String)
    message_content = Column(String)
    display_name = Column(String)
    display_instance = Column(String)
    evse_id = Column(Integer)
    connector_id = Column(Integer)

class NotifyEVChargingNeeds201(Base):
    __tablename__ = "notify_ev_charging_needs_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    max_schedule_tuples = Column(Integer)
    evse_id = Column(Integer)
    charging_needs = Column(String)
    requested_energy_transfer = Column(String)
    departure_time = Column(String)
    energy_amount_ac = Column(Integer)
    ev_min_current_ac = Column(Integer)
    ev_max_current_ac = Column(Integer)
    ev_max_voltage_ac = Column(Integer)
    ev_max_current_dc = Column(Integer)
    ev_max_voltage_dc = Column(Integer)
    energy_amount_dc = Column(Integer)
    ev_max_power_dc = Column(Integer)
    state_of_charge = Column(Integer)
    ev_energy_capacity = Column(Integer)
    full_state_of_charge = Column(Integer)
    bulk_state_of_charge = Column(Integer)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class NotifyEVChargingSchedule201(Base):
    __tablename__ = "notify_ev_charging_schedule_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    time_base = Column(String)
    evse_id = Column(String)
    charging_schedule = Column(String)
    charging_schedule_id = Column(String)
    start_schedule = Column(String)
    duration = Column(String)
    charging_rate_unit = Column(String)
    min_charging_rate = Column(String)
    start_period = Column(String)
    limit = Column(String)
    number_phases = Column(String)
    phases_to_use = Column(String)
    sales_tariff_id = Column(String)
    sales_tariff_description = Column(String)
    num_e_price_levels = Column(String)
    e_price_level = Column(String)
    relative_time_interval_start = Column(String)
    relative_time_interval_duration = Column(String)
    consumption_start_value = Column(String)
    cost_kind = Column(String)
    amount = Column(String)
    amount_multiplier = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class NotifyEvent201(Base):
    __tablename__ = "notify_event_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    generated_at = Column(DateTime)
    tbc = Column(Boolean)
    seq_no = Column(Integer)
    event_id = Column(Integer)
    trigger = Column(String)
    cause = Column(Integer)
    actual_value = Column(String)
    tech_code = Column(String)
    tech_info = Column(String)
    cleared = Column(Boolean)
    transaction_id = Column(String)
    variable_monitoring_id = Column(Integer)
    event_notification_type = Column(String)
    component_name = Column(String)
    component_instance = Column(String)
    evse_id = Column(Integer)
    connector_id = Column(Integer)
    variable_name = Column(String)
    variable_instance = Column(String)

class NotifyMonitoringReport201(Base):
    __tablename__ = "notify_monitoring_report_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    request_id = Column(Integer)
    tbc = Column(Boolean)
    seq_no = Column(Integer)
    generated_at = Column(DateTime)
    component_name = Column(String)
    component_instance = Column(String)
    evse_id = Column(Integer)
    connector_id = Column(Integer)
    variable_name = Column(String)
    variable_instance = Column(String)
    monitoring_id = Column(Integer)
    transaction = Column(Boolean)
    monitor_value = Column(Integer)
    monitor_type = Column(String)
    severity = Column(Integer)

class NotifyReport201(Base):
    __tablename__ = "notify_report_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    request_id = Column(Integer)
    generated_at = Column(DateTime)
    tbc = Column(Boolean)
    seq_no = Column(Integer)
    component_name = Column(String)
    component_instance = Column(String)
    evse_id = Column(Integer)
    connector_id = Column(Integer)
    variable_name = Column(String)
    variable_instance = Column(String)
    attribute_type = Column(String)
    mutability = Column(String)
    attribute_value = Column(String)
    persistent = Column(Boolean)
    constant = Column(Boolean)
    unit = Column(String)
    data_type = Column(String)
    min_limit = Column(Integer)
    max_limit = Column(Integer)
    values_list = Column(String)
    supports_monitoring = Column(Boolean)

class PublishFirmwareStatusNotification201(Base):
    __tablename__ = "publish_firmware_status_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    status = Column(String)
    location = Column(String)
    request_id = Column(Integer)

class ReportChargingProfiles201(Base):
    __tablename__ = "report_charging_profiles_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    request_id = Column(Integer)
    charging_limit_source = Column(String)
    tbc = Column(Boolean)
    evse_id = Column(Integer)
    charging_profile_id = Column(Integer)
    stack_level = Column(Integer)
    charging_profile_purpose = Column(String)
    charging_profile_kind = Column(String)
    recurrency_kind = Column(String)
    valid_from = Column(DateTime)
    valid_to = Column(DateTime)
    transaction_id = Column(String)
    charging_schedule_id = Column(Integer)
    start_schedule = Column(DateTime)
    duration = Column(Integer)
    charging_rate_unit = Column(String)
    min_charging_rate = Column(Integer)
    start_period = Column(Integer)
    limit = Column(Integer)
    number_phases = Column(Integer)
    phases_to_use = Column(Integer)
    sales_tariff_id = Column(Integer)
    sales_tariff_description = Column(String)
    num_e_price_levels = Column(Integer)
    e_price_level = Column(Integer)
    relative_time_interval_start = Column(Integer)
    relative_time_interval_duration = Column(Integer)
    consumption_start_value = Column(Integer)
    cost_kind = Column(String)
    amount = Column(Integer)
    amount_multiplier = Column(Integer)

class ReservationStatus201(Base):
    __tablename__ = "reservation_status_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    reservation_id = Column(Integer)
    reservation_update_status = Column(String)

class SecurityEventNotification201(Base):
    __tablename__ = "security_event_notification_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    type = Column(String)
    tech_info = Column(String)

class SignCertificate201(Base):
    __tablename__ = "sign_certificate_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    csr = Column(String)
    certificate_type = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class StatusNotification201(Base):
    __tablename__ = "status_notification_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    connector_status = Column(Integer)
    evse_id = Column(Integer)
    connector_id = Column(Integer)

class TransactionEvent201(Base):
    __tablename__ = "transaction_event_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    event_type = Column(String)
    trigger_reason = Column(String)
    seq_no = Column(Integer)
    offline = Column(Boolean)
    number_of_phases_used = Column(Integer)
    cable_max_current = Column(Integer)
    reservation_id = Column(Integer)
    transaction_id = Column(String)
    charging_state = Column(String)
    time_spent_charging = Column(Integer)
    stopped_reason = Column(String)
    remote_start_id = Column(Integer)
    id_token = Column(String)
    id_token_type = Column(String)
    evse_id = Column(Integer)
    connector_id = Column(Integer)
    measurand = Column(String)
    value = Column(String)
    context = Column(String)
    phase = Column(String)
    location = Column(String)
    signed_meter_data = Column(String)
    signing_method = Column(String)
    encoding_method = Column(String)
    public_key = Column(String)
    unit = Column(String)
    multiplier = Column(Integer)
    total_cost = Column(Integer)
    charging_priority = Column(Integer)
    authorization_status = Column(String)
    cache_expiry_data = Column(DateTime)
    language_1 = Column(String)
    evse_id = Column(Integer)
    language_2 = Column(String)
    group_id_token = Column(String)
    group_id_token_type = Column(String)
    message_format = Column(String)
    message_langauge = Column(String)
    message_content = Column(String)
    updated_message_format = Column(String)
    updated_message_language = Column(String)
    updated_message_content = Column(String)

class ClearVariableMonitoring201(Base):
    __tablename__ = "clear_variable_monitoring_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    monitor_id = Column(Integer)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class CostUpdate201(Base):
    __tablename__ = "cost_update_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    total_cost = Column(Integer)
    transaction_id = Column(String)

class CostumerInformation201(Base):
    __tablename__ = "costumer_information_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    request_id = Column(Integer)
    report = Column(Boolean)
    clear = Column(Boolean)
    customer_identifier = Column(String)
    id_token = Column(String)
    id_token_type = Column(String)
    hash_algorithm = Column(String)
    issuer_name_hash = Column(String)
    issuer_key_hash = Column(String)
    serial_number = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class ChargePointDataTransfer201(Base):
    __tablename__ = "charge_point_data_transfer_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    message_id = Column(String)
    request_data = Column(String)
    response_data = Column(String)
    vendor_id = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class OperatorDataTransfer201(Base):
    __tablename__ = "operator_data_transfer_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    message_id = Column(String)
    request_data = Column(String)
    response_data = Column(String)
    vendor_id = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class DeleteCertificate201(Base):
    __tablename__ = "delete_certificate_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    hash_algorithm = Column(String)
    issuer_name_hash = Column(String)
    issuer_key_hash = Column(String)
    serial_number = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class ReserveNow201(Base):
    __tablename__ = "reserve_now_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    reservation_id = Column(Integer)
    expiry_date_time = Column(DateTime)
    connector_type = Column(String)
    evse_id = Column(Integer)
    id_token = Column(String)
    id_token_type = Column(String)
    group_id_token = Column(String)
    group_id_token_type = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class Reset201(Base):
    __tablename__ = "reset_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    type = Column(String)
    evse_id = Column(Integer)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class SendLocalList201(Base):
    __tablename__ = "send_local_list_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    version_number = Column(Integer)
    update_type = Column(String)
    id_token = Column(String)
    id_token_type = Column(String)
    authorization_status = Column(String)
    cache_expiry_datetime = Column(DateTime)
    charging_priority = Column(String)
    language_1 = Column(String)
    evse_id = Column(Integer)
    language_2 = Column(String)
    group_id_token = Column(String)
    group_id_type = Column(String)
    personal_message = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class SetChargingProfile201(Base):
    __tablename__ = "set_charging_profile"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    evse_id = Column(Integer)
    charging_profile = Column(String)
    charging_profile_id = Column(Integer)
    stack_level = Column(Integer)
    charging_profile_purpose = Column(String)
    charging_profile_kind = Column(String)
    recurrency_kind = Column(String)
    valid_from = Column(DateTime)
    valid_to = Column(DateTime)
    transaction_id = Column(String)
    charging_schedule_id = Column(Integer)
    start_schedule = Column(DateTime)
    duration = Column(Integer)
    charging_rate_unit = Column(String)
    min_charging_rate = Column(Integer)
    start_period = Column(Integer)
    limit = Column(Integer)
    number_phases = Column(Integer)
    phases_to_use = Column(Integer)
    sales_tariff_id = Column(Integer)
    sales_tariff_description = Column(String)
    num_e_price_levels = Column(Integer)
    e_price_level = Column(Integer)
    relative_time_interval_start = Column(Integer)
    relative_time_interval_duration = Column(Integer)
    consumption_start_value = Column(Integer)
    cost_kind = Column(String)
    amount = Column(Integer)
    amount_multiplier = Column(Integer)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class GetBaseReport(Base):
    __tablename__ = "get_base_report_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    request_id = Column(Integer)
    report_base = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class GetChargingProfiles201(Base):
    __tablename__ = "get_charging_profiles_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    request_id = Column(Integer)
    evse_id = Column(Integer)
    charging_profile_purpose = Column(String)
    stack_level = Column(Integer)
    charging_profile_id = Column(Integer)
    charging_limit_source = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class GetCompositeSchedule201(Base):
    __tablename__ = "get_composite_schedule_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    duration = Column(Integer)
    charging_rate_unit = Column(String)
    evse_id = Column(Integer)
    status = Column(String)
    schedule_start = Column(DateTime)
    start_period = Column(Integer)
    limit = Column(Integer)
    number_phases = Column(Integer)
    phases_to_use = Column(Integer)
    reason_code = Column(String)
    additional_info = Column(String)

class GetDisplayMessage201(Base):
    __tablename__ = "get_display_message_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    message_id = Column(Integer)
    request_id = Column(Integer)
    priority = Column(String)
    state = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class GetInstalledCertificateIds201(Base):
    __tablename__ = "get_installed_certificate_ids_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    certificate_type = Column(String)
    status = Column(String)
    hash_algorithm = Column(String)
    issuer_name_hash = Column(String)
    issuer_key_hash = Column(String)
    serial_number = Column(String)
    child_hash_algorithm = Column(String)
    child_issuer_name_hash = Column(String)
    child_issuer_key_hash = Column(String)
    child_serial_number = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class SetMonitorBase201(Base):
    __tablename__ = "set_monitor_base_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    monitoring_base = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class SetMonitorLevel201(Base):
    __tablename__ = "set_monitor_level_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    severity = Column(Integer)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class SetNetWorkProfile201(Base):
    __tablename__ = "set_network_profile_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    configuration_slot = Column(Integer)
    ocpp_version = Column(String)
    ocpp_transport = Column(String)
    ocpp_csms_url = Column(String)
    message_timeout = Column(Integer)
    security_profile = Column(Integer)
    ocpp_interface = Column(String)
    vpn_server = Column(String)
    vpn_user = Column(String)
    vpn_group = Column(String)
    vpn_password = Column(String)
    vpn_key = Column(String)
    vpn_type = Column(String)
    apn = Column(String)
    apn_user_name = Column(String)
    apn_password = Column(String)
    sim_pin = Column(Integer)
    preffered_network = Column(String)
    use_only_preffered_network = Column(Boolean)
    apn_authentication = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class SetVariableMonitoring201(Base):
    __tablename__ = "set_variable_monitoring_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    set_monitoring_id = Column(Integer)
    transaction = Column(Boolean)
    monitoring_value = Column(Integer)
    monitoring_type = Column(String)
    monitoring_result_id = Column(String)
    monitoring_result_status = Column(String)
    monitoring_result_type = Column(String)
    severity = Column(Integer)
    component_name = Column(String)
    component_instance = Column(String)
    evse_id = Column(Integer)
    connector_id = Column(Integer)
    variable_name = Column(String)
    variable_instance = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class SetVariables201(Base):
    __tablename__ = "set_variables_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    attribute_value = Column(String)
    attribute_type = Column(String)
    attribute_status = Column(String)
    component_name = Column(String)
    component_instance = Column(String)
    evse_id = Column(Integer)
    connector_id = Column(Integer)
    variable_name = Column(String)
    variable_instance = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class CancelReservation201(Base):
    __tablename__ = "cancel_reservation_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    reservation_id = Column(Integer)
    reason_code = Column(String)
    additional_info = Column(String)

class CertificateSigned201(Base):
    __tablename__ = "certificate_signed_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    certificate_chain = Column(String)
    certificate_type = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class Availability201(Base):
    __tablename__ = "availability_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    operational_status = Column(String)
    evse_id = Column(Integer)
    connector_id = Column(Integer)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class ClearCache201(Base):
    __tablename__ = "clear_cache_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class ClearChargingProfile201(Base):
    __tablename__ = "clear_charging_profile_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    charging_profile_id = Column(Integer)
    evse_id = Column(Integer)
    charging_profile_purpose = Column(String)
    stack_level = Column(Integer)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class ClearMessageDisplay201(Base):
    __tablename__ = "clear_message_display_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    message_id = Column(Integer)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class GetVariable201(Base):
    __tablename__ = "get_variable_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    attribute_status = Column(String)
    attribute_type = Column(String)
    attribute_value = Column(String)
    component_name = Column(String)
    component_instance = Column(String)
    evse_id = Column(Integer)
    connector_id = Column(Integer)
    variable_name = Column(String)
    variable_instance = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class InstallCertificate201(Base):
    __tablename__ = "install_certificate_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    certificate_type = Column(String)
    certificate = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class PublishFirmware201(Base):
    __tablename__ = "publish_firmware_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    location = Column(String)
    retries = Column(Integer)
    retry_interval = Column(Integer)
    checksum = Column(String)
    request_id = Column(Integer)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class RequestStartTransaction201(Base):
    __tablename__ = "request_start_transaction_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    evse_id = Column(Integer)
    remote_start_id = Column(Integer)
    id_token_id = Column(String)
    id_token_type = Column(String)
    charging_profile_id = Column(Integer)
    stack_level = Column(Integer)
    charging_profile_purpose = Column(String)
    charging_profile_kind = Column(String)
    recurrency_kind = Column(String)
    valid_from = Column(DateTime)
    valid_to = Column(DateTime)
    transaction_id = Column(String)
    charging_schedule_id = Column(Integer)
    start_schedule = Column(DateTime)
    duration = Column(Integer)
    charging_rate_unit = Column(String)
    min_charging_rate = Column(Integer)
    start_period = Column(Integer)
    limit = Column(Integer)
    number_phases = Column(Integer)
    phases_to_use = Column(Integer)
    sales_tariff_id = Column(Integer)
    sales_tariff_description = Column(String)
    num_e_price_levels = Column(Integer)
    e_price_level = Column(Integer)
    relative_time_interval_start = Column(Integer)
    relative_time_interval_duration = Column(Integer)
    consumption_start_value = Column(Integer)
    cost_kind = Column(String)
    amount = Column(Integer)
    amount_multiplier = Column(Integer)
    group_id_token = Column(String)
    group_id_token_type = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class RequestStopTransaction201(Base):
    __tablename__ = "request_stop_transaction_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    transaction_id = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class GetLocalListVersion201(Base):
    __tablename__ = "get_local_list_version_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    version_number = Column(Integer)

class GetLog201(Base):
    __tablename__ = "get_log_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    log_type = Column(String)
    request_id = Column(Integer)
    retries = Column(Integer)
    retry_interval = Column(Integer)
    remote_location = Column(String)
    oldest_timestamp = Column(DateTime)
    latest_timestamp = Column(DateTime)
    filename = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)


class GetMonitoringReport201(Base):
    __tablename__ = "get_monitoring_report_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    request_id = Column(Integer)
    monitoring_criteria = Column(String)
    component_name = Column(String)
    component_instance = Column(String)
    evse_id = Column(Integer)
    connector_id = Column(Integer)
    variable_name = Column(String)
    variable_instance = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class GetReport201(Base):
    __tablename__ = "get_report_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    request_id = Column(Integer)
    component_criteria = Column(String)
    component_name = Column(String)
    component_instance = Column(String)
    evse_id = Column(Integer)
    connector_id = Column(Integer)
    variable_name = Column(String)
    variable_instance = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class GetTransactionStatus201(Base):
    __tablename__ = "get_transaction_status_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    transaction_id = Column(String)
    ongoing_indicator = Column(Boolean)
    messages_in_queue = Column(Boolean)

class UnlockConnector201(Base):
    __tablename__ = "unlock_connector_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    evse_id = Column(Integer)
    connector_id = Column(Integer)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class UnpublishFirmware201(Base):
    __tablename__ = "unpublish_firmware_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    checksum = Column(String)
    status = Column(String)

class UpdateFirmware201(Base):
    __tablename__ = "update_firmware_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    retries = Column(Integer)
    retry_interval = Column(Integer)
    request_id = Column(Integer)
    location = Column(String)
    retrieve_datetime = Column(DateTime)
    install_datetime = Column(DateTime)
    signing_certificate = Column(String)
    signature = Column(String)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class TriggerMessage201(Base):
    __tablename__ = "trigger_message_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    requested_message = Column(String)
    evse_id = Column(Integer)
    connector_id = Column(Integer)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)

class SetDisplayMessage201(Base):
    __tablename__ = "set_display_message_201"
    id = Column(Integer, primary_key = True, index = True)
    charge_point_id = Column(String)
    timestamp = Column(DateTime)
    message_id = Column(Integer)
    priority = Column(String)
    state = Column(String)
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    transaction_id = Column(String)
    message_format = Column(String)
    message_language = Column(String)
    message_content = Column(String)
    display_name = Column(String)
    display_instance = Column(String)
    evse_id = Column(Integer)
    connector_id = Column(Integer)
    status = Column(String)
    reason_code = Column(String)
    additional_info = Column(String)
