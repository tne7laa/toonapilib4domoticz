import Domoticz
from devices.device import Device
from devices.device import DeviceCommandException
from devices.device import DeviceCreateException
from devices.device import DeviceUpdateException


class DeviceThermostatState(Device):
    def __init__(self, name, unit, devices, toon, debug):
        super().__init__(name, unit, devices, toon, debug)

    def create(self):
        if not self.exists:
            try:
                Domoticz.Log("Creating thermostat state device " + self.name)

                options = {
                    "LevelNames": "Unknown|Away|Sleep|Home|Comfort|Holiday",
                    "LevelOffHidden": "true", "SelectorStyle": "0"}
                Domoticz.Device(Name=self.name, Unit=self.unit,
                                TypeName="Selector Switch", Options=options).Create()

            except DeviceCreateException as ex:
                Domoticz.Log("An error occurred creating " + self.name)
                Domoticz.Log("Exception: " + str(ex))
        elif self.debug:
            Domoticz.Log("Unit " + str(self.unit) + " exists - nothing to do")
        return self

    def on_command(self, Unit, Command, Level, Hue):
        try:
            str_scene = self.get_scene_name(Level)
            self.toon.thermostat_state = str_scene

            if self.debug:
                Domoticz.Log("set scene " + str(Level) + " - " + str_scene)
            self.devices[self.unit].Update(2, str(Level))

        except DeviceCommandException as ex:
            Domoticz.Log("An error occurred setting " + self.name)
            Domoticz.Log("Exception: " + str(ex))

    def update(self):
        super().update()
        str_value = ""

        try:
            if not self.toon.thermostat_state:
                str_value = "Unknown"
            else:
                str_value = str(self.toon.thermostat_state.name)

            if str_value != "" and str_value != self.previous_value:
                if self.debug:
                    Domoticz.Log("Update thermostat state: " + str_value)
                self.devices[self.unit].Update(2, str(self.get_scene_value(str_value)))

        except DeviceUpdateException as ex:
            Domoticz.Log("An error occurred updating " + self.name)
            Domoticz.Log("Exception: " + str(ex))

        self.set_previous_value(str_value)

    @staticmethod
    def get_scene_value(x):
        return {
            'Unknown': 0,
            'Away': 10,
            'Sleep': 20,
            'Home': 30,
            'Comfort': 40,
            'Holiday': 50
        }[x]

    @staticmethod
    def get_scene_name(i):
        str_return_string = "Unknown"

        if i == 10:
            str_return_string = "Away"
        elif i == 20:
            str_return_string = "Sleep"
        elif i == 30:
            str_return_string = "Home"
        elif i == 40:
            str_return_string = "Comfort"
        elif i == 50:
            str_return_string = "Holiday"

        return str_return_string
