## Grundfos Magna 3 E for esphome

This plugin has been AI-generated from the alpha3 source code, a bluetooth HCI dump from the Grundfos Go App as well as the GENIBus register description found in the APK of the Grundfos Go App.

Use it in esphome like this:

* put this repository for example as `magna3` into your custom components folder
* add the following template to your esphome config and adjust it accordingly

```
esp32_ble_tracker:
  
external_components:
 - source:
     type: local
     path: .
   components: [magna3]

ble_client:
  - mac_address: <pump1_mac>
    id: pump1
  - mac_address: <pump2_mac>
    id: pump2

sensor:
  - platform: magna3
    ble_client_id: pump1
    flow:
      name: "Pump 1 Flow"
    head:
      name: "Pump 1 Head"
    speed:
      name: "Pump 1 Speed"
    power:
      name: "Pump 1 Power"
    temperature:
      name: "Radiator Pump Temperature"
  - platform: magna3
    ble_client_id: pump2
    flow:
      name: "Pump 2 Flow"
    head:
      name: "Pump 2 Head"
    speed:
      name: "Pump 2 Speed"
    power:
      name: "Pump 2 Power"
    temperature:
      name: "Pump 2 Temperature"
```

You have to press the pair button on the pump in the right moment - just press it often until it works.

I was too lazy to make this into a generic plugin. With the register description from the grundfos go app, it should be quite possible to write a generic component which could also be used for configuration.

Still, I provide no warranty that this doesn't destroy your pump - use at your own risk!