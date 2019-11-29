from Component.Helper.JsonHandler import JsonHandler
from Component.Handler.eventHook import EventHook
from Component.Helper.Priority import Priority
import datetime
import re

# this class is in charge of the priority object and sending
#the flood data request to bluetooth
class P2PManager (object) :

    _P2PHandler = EventHook()
    _P2PHandlerRxOff = EventHook()

    def setUp(self):
        self.jsonHandler = JsonHandler()
        self.NodePortList=self.Priority.getNodePortList()

    def __init__ (self,CurrentBatteryPower) :
        self.CurrentBatteryPower = CurrentBatteryPower
        self.Priority=Priority()
        self.setUp()

    def __del__ (self):
        self.Priority.__del__()

    #floods the surrounding nodes in the priority table with current battery data
    def floodData(self,CurrentBatteryPower):
        self.CurrentBatteryPower = CurrentBatteryPower
        #fires event to bluetooth to flood the priority table sensors with new battery data
        self._P2PHandler.fire(batteryData=CurrentBatteryPower,NodePortList=self.NodePortList,sensorName=self.Priority.SensorDeviceName)
        # updtaes the current priority list
        self.Priority.priorityUpdate(self.Priority.SensorDeviceName,CurrentBatteryPower)
        self.Priority.prioritySort()
    # this receives the sent data from other nodes and parses it
    # it then passes it into the update table method and jif the result
    # comes back true and the current top node is the sensor then stay
    # active as it is the chosen peer node
    def updatePriorityTable(self,**kwargs):
        data=kwargs.get('PriorityTableData')
        processedBatteryData=re.findall("\d+\.\d+", data )
        nodeName = re.search(': (.+?) :', data).group(1)
        #check if this sensor is top of priority list
        # and stop listening for its own sent data
        if  self.Priority.SensorDeviceName not in nodeName:
            #parse data for updating PriorityTable
            #send it to the table
            PriorityTableUpdated=self.Priority.priorityUpdate(nodeName,processedBatteryData[0])
            self.Priority.prioritySort()
            #check if this sensor is top of priority list
            if(PriorityTableUpdated):
                if self.Priority.SensorDeviceName in self.Priority.getCurrentPriorityPort():
                    return
                else: #not top priority node and turn Turn Off
                    self._P2PHandlerRxOff.fire()
