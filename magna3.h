#pragma once

#include "esphome/core/component.h"
#include "esphome/components/ble_client/ble_client.h"
#include "esphome/components/esp32_ble_tracker/esp32_ble_tracker.h"
#include "esphome/components/sensor/sensor.h"

#ifdef USE_ESP32

#include <esp_gattc_api.h>

namespace esphome {
namespace magna3 {

namespace espbt = esphome::esp32_ble_tracker;

// Same BLE service/characteristic as Alpha2/Alpha3 — all Grundfos GENIBus BLE pumps
static const espbt::ESPBTUUID MAGNA3_GENI_SERVICE_UUID = espbt::ESPBTUUID::from_uint16(0xfe5d);
static const espbt::ESPBTUUID MAGNA3_GENI_CHARACTERISTIC_UUID =
    espbt::ESPBTUUID::from_raw({static_cast<char>(0xa9), 0x7b, static_cast<char>(0xb8), static_cast<char>(0x85), 0x0,
                                0x1a, 0x28, static_cast<char>(0xaa), 0x2a, 0x43, 0x6e, 0x3, static_cast<char>(0xd1),
                                static_cast<char>(0xff), static_cast<char>(0x9c), static_cast<char>(0x85)});

// Expected combined reply length: SD(1)+LEN(1)+payload(24)+CRC(2) = 28 bytes
static const size_t MAGNA3_RESPONSE_MAX_LENGTH = 64;
// Minimum reply to contain all five sensors
static const size_t MAGNA3_RESPONSE_MIN_LENGTH = 28;

class Magna3 : public esphome::ble_client::BLEClientNode, public PollingComponent {
 public:
  void setup() override;
  void update() override;
  void gattc_event_handler(esp_gattc_cb_event_t event, esp_gatt_if_t gattc_if,
                           esp_ble_gattc_cb_param_t *param) override;
  void dump_config() override;

  void set_flow_sensor(sensor::Sensor *sensor) { this->flow_sensor_ = sensor; }
  void set_head_sensor(sensor::Sensor *sensor) { this->head_sensor_ = sensor; }
  void set_power_sensor(sensor::Sensor *sensor) { this->power_sensor_ = sensor; }
  void set_speed_sensor(sensor::Sensor *sensor) { this->speed_sensor_ = sensor; }
  void set_temperature_sensor(sensor::Sensor *sensor) { this->temperature_sensor_ = sensor; }

 protected:
  sensor::Sensor *flow_sensor_{nullptr};
  sensor::Sensor *head_sensor_{nullptr};
  sensor::Sensor *power_sensor_{nullptr};
  sensor::Sensor *speed_sensor_{nullptr};
  sensor::Sensor *temperature_sensor_{nullptr};

  uint16_t geni_handle_{0};
  uint8_t response_buf_[MAGNA3_RESPONSE_MAX_LENGTH];
  uint16_t response_offset_{0};
  uint16_t response_expected_{0};

  void handle_notification_(const uint8_t *data, uint16_t length);
  void parse_response_();
  void send_request_(uint8_t *request, size_t len);
  void publish_disconnect_();
};

}  // namespace magna3
}  // namespace esphome

#endif
