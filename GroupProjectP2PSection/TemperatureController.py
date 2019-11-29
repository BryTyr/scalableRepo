from Component.MicroController import MicroController
from Component.Bluetooth import Bluetooth
from Component.Battery import Battery
from Component.TemperatureSensor import TemperatureSensor
from Component.Handler.P2PManager import P2PManager
from Component.Handler.eventHook import EventHook
from Component.Helper.JsonHandler import JsonHandler
from threading import Timer
import time
import sys

class TemperatureController (MicroController) :

    _characteristicsPath = "Characteristics/TemperatureController.json"

    def Setup(self):
        self.bt = Battery(self._ControllerChar['Battery']['CurrentState']['Power'])
        self.ble = Bluetooth(3.0,30)
        self.ts = TemperatureSensor(3.0)
        self.mgr = P2PManager(self.bt.GetCurrentCharge())

    def __init__(self):
        self.jsonHandler = JsonHandler()
        self._ControllerChar = self.jsonHandler.LoadJson(self._characteristicsPath)
        self.Setup()
        self.ConnectHandlers()
        self.floodDataTimer()
        super().__init__(3.0)

        try:
            while(True):
                self.Run()
        except KeyboardInterrupt:
            self._ControllerChar['Battery']['CurrentState']['Power'] = self.bt.GetCurrentCharge()
            self.__del__()
            exit(1)

    def __del__(self):
        self.jsonHandler.WriteJson(self._characteristicsPath,self._ControllerChar)
        self.ble.__del__()
        self.ts.__del__()
        self.bt.__del__()
        self.mgr.__del__()
        super().__del__()

    def ConnectHandlers(self):
        self.ble._p2PEvent.addHandler(self.mgr.updatePriorityTable) # to update priority table data
        self.mgr._P2PHandler.addHandler(self.ble.FloodNodes) # to turn on flooding
        self.mgr._P2PHandlerRxOff.addHandler(self.ble.ToActiveMode) #to turn off RX mode
        self.ble._batteryEvent.addHandler(self.bt.Discharging)
        self.ts._batteryEvent.addHandler(self.bt.Discharging)
        self._batteryEvent.addHandler(self.bt.Discharging)
        self.ble._uartEvent.addHandler(self.UartRx)

    def Run(self):
        time.sleep(1)
        temp = self.ReadTemperature()
        time.sleep(1)
        self.WriteBluetooth(temp)
        time.sleep(1)

    def ReadTemperature(self):
        self.I2CRead()
        return self.ts.I2CRead()

    def WriteBluetooth(self,data):
        super().I2CWrite()
        self.ble.Tx(data)

    # to start a flood timer
    def floodDataTimer(self):
        # hop device flood data every 900 seconds
        self._timer = Timer(20,self.timerHit)
        self._timer.start()

    def timerHit(self):
        self.mgr.floodData(self.bt.GetCurrentCharge())
        time.sleep(1)
        self.floodDataTimer()

    def UartRx(self,**kwargs):
        data = kwargs.get('data')
        #self.UartPowerConsumed(data)
        print('RX --->>>', str(data))
        #self.WifiPowerConsumed(data)
        #self._mqttService.Publish(data)
