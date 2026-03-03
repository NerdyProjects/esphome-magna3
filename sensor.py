import esphome.codegen as cg
from esphome.components import ble_client, sensor
import esphome.config_validation as cv
from esphome.const import (
    CONF_FLOW,
    CONF_HEAD,
    CONF_ID,
    CONF_POWER,
    CONF_SPEED,
    CONF_TEMPERATURE,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_TEMPERATURE,
    STATE_CLASS_MEASUREMENT,
    UNIT_CELSIUS,
    UNIT_CUBIC_METER_PER_HOUR,
    UNIT_METER,
    UNIT_REVOLUTIONS_PER_MINUTE,
    UNIT_WATT,
)

magna3_ns = cg.esphome_ns.namespace("magna3")
Magna3 = magna3_ns.class_("Magna3", ble_client.BLEClientNode, cg.PollingComponent)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(Magna3),
            cv.Optional(CONF_FLOW): sensor.sensor_schema(
                unit_of_measurement=UNIT_CUBIC_METER_PER_HOUR,
                accuracy_decimals=2,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_HEAD): sensor.sensor_schema(
                unit_of_measurement=UNIT_METER,
                accuracy_decimals=2,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_POWER): sensor.sensor_schema(
                unit_of_measurement=UNIT_WATT,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_SPEED): sensor.sensor_schema(
                unit_of_measurement=UNIT_REVOLUTIONS_PER_MINUTE,
                accuracy_decimals=0,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
        }
    )
    .extend(ble_client.BLE_CLIENT_SCHEMA)
    .extend(cv.polling_component_schema("15s"))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await ble_client.register_ble_node(var, config)

    if flow_config := config.get(CONF_FLOW):
        sens = await sensor.new_sensor(flow_config)
        cg.add(var.set_flow_sensor(sens))

    if head_config := config.get(CONF_HEAD):
        sens = await sensor.new_sensor(head_config)
        cg.add(var.set_head_sensor(sens))

    if power_config := config.get(CONF_POWER):
        sens = await sensor.new_sensor(power_config)
        cg.add(var.set_power_sensor(sens))

    if speed_config := config.get(CONF_SPEED):
        sens = await sensor.new_sensor(speed_config)
        cg.add(var.set_speed_sensor(sens))

    if temperature_config := config.get(CONF_TEMPERATURE):
        sens = await sensor.new_sensor(temperature_config)
        cg.add(var.set_temperature_sensor(sens))
