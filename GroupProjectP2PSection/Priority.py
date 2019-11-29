from Component.Helper.JsonHandler import JsonHandler
import datetime
import operator
import random


class Priority (object) :

    PriorityTablePath = "Characteristics/PriorityTable.json"
    logPath = "Characteristics/PriorityLog.json"

    def __init__ (self) :
        self.jsonHandlerPriority = JsonHandler()
        self.CurrentPriorityList =  self.jsonHandlerPriority.LoadJson(self.PriorityTablePath)
        self.PriorityLog = self.jsonHandlerPriority.LoadJson(self.logPath)
        self._logsPrioirity = self.PriorityLog['PriorityLog']
        self.PriorityCallsAmount=len(self.CurrentPriorityList["Priority"])
        self.PriorityCalls = 0
        print("the length is: "+str(len(self.CurrentPriorityList["Priority"])))

    def __del__ (self):
        self.PriorityLog['PriorityLog'] = self._logsPrioirity
        print(self._logsPrioirity)
        self.jsonHandlerPriority.WriteJson(self.logPath,self.PriorityLog)

    #this sorts the list into order to place longest battery at top
    def prioritySort(self):#currentPriorityList
        #self.CurrentPriorityList=currentPriorityList
        nodeList={}
        for key, value in self.CurrentPriorityList["Priority"].items():
            print(value)
            nodeList[key]=value["battery"]
        sortedNodeList=sorted(nodeList, key=operator.itemgetter(1), reverse=True)
        for key in sortedNodeList:
            print("here inside ordering")
            print(self.CurrentPriorityList)
            value=self.CurrentPriorityList["Priority"][key].pop()
            self.CurrentPriorityList["Priority"][key]=value
            print(self.CurrentPriorityList)
            count=0
            randomVar=random.randint(10000,100000)
        for key in sortedNodeList:
            count+=1
            log = { "DeviceID":key,
                    "DatapointID":randomVar,
                    "RankOrder":count,
                    "battery":self.CurrentPriorityList["Priority"][key]["battery"],
                    "portNumber":self.CurrentPriorityList["Priority"][key]["portNumber"],
                   'TimeStamp' : (datetime.datetime.now()).strftime('%m/%d/%Y %I:%M:%S %p') }
            self._logsPrioirity.append(log)

        #self._logsPrioirity.append(log)
        
        #self.jsonHandlerPriority.WriteJson(self.logPath,self._logsPrioirity)


    #this method removes old data and updates it with newest data
    def priorityUpdate(self,node,data):
        #changes order of priority list round robbin orderin
            nodeList={}
            for key, value in self.CurrentPriorityList["Priority"].items():
                if node in key:
                    self.CurrentPriorityList["Priority"][node]["battery"]=float(data)
            #self.prioritySort(self.CurrentPriorityList)
            self.PriorityCalls+=1
            #if all calls made
            if self.PriorityCalls == self.PriorityCallsAmount:
                self.PriorityCalls=0
                return True
            else:
                return False

    def getCurrentPriority(self):
        return self.CurrentPriorityList

    def getCurrentPriorityPort(self):
        FirstKeyIndex=next(iter(self.CurrentPriorityList['Priority']))
        value=self.CurrentPriorityList['Priority'][FirstKeyIndex]
        return value

    #returns a list with the current node ports for contacting
    def getNodePortList(self):
        nodeList=[]
        for key, value in self.CurrentPriorityList["Priority"].items():
            #home sensor a parameter to signal this sensors data (1 or 0)
            if 1 != value["HomeSensor"]:
                print(value["portNumber"])
                nodeList.append(value["portNumber"])
            else:
                print("Here "+key)
                self.SensorDeviceName = key
        return nodeList
