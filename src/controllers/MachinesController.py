
from datetime import datetime
import requests
import json

from Cheese.cheeseController import CheeseController as cc
from Cheese.appSettings import Settings
from Cheese.Logger import Logger
from Cheese.httpClientErrors import *

from src.repositories.usersRepository import UsersRepository as ur
from src.repositories.machinesRepository import MachinesRepository as mr

#@controller /machines;
class MachinesController(cc):

    #@get /getMy;
    @staticmethod
    def getMy(server, path, auth):
        userModel = ur.findOneBy("email", auth["login"]["login"])
        
        machines = mr.findBy("user_id", userModel.id)
        newMachines = []
        for machine in machines:
            reqText = f"https://geo.ipify.org/api/v2/country,city,vpn?apiKey={Settings.geoApiKey}&ipAddress={machine.ip}"
            Logger.info(f"Sending GET request: {reqText}")
            req = requests.get(reqText)

            if (req.status_code != 200):
                Logger.fail("Fail while getting info about machine")
                machine.setAttrs(
                    city = "",
                    region = "",
                    country = "",
                    lat = "",
                    lng = "",
                    proxy = "",
                    vpn = "",
                    tor = "",
                )
            else:
                Logger.info(req.text)
                jsn = json.loads(req.text)
                machine.setAttrs(
                    city = jsn["location"]["city"],
                    region = jsn["location"]["region"],
                    country = jsn["location"]["country"],
                    lat = jsn["location"]["lat"],
                    lng = jsn["location"]["lng"],
                    proxy = jsn["proxy"]["proxy"],
                    vpn = jsn["proxy"]["vpn"],
                    tor = jsn["proxy"]["tor"],
                )
            newMachines.append(machine)

        return cc.createResponse({"MACHINES": cc.modulesToJsonArray(newMachines)})

    #@post /logMachine;
    @staticmethod
    def logMachine(server, path, auth):
        args = cc.readArgs(server)
        cc.checkJson(["ip", "login"], args)

        ip = args["ip"]
        login = args["login"].replace("'", "")

        userModel = ur.findOneBy("email", login)
        machineModel = mr.findMachineByUserIdAndIp(userModel.id, ip)

        if (machineModel == None):
            raise NotFound("Machine was not found")

        machineModel.last_connection = datetime.now()
        mr.update(machineModel)

        return cc.createResponse({"STATUS": "OK"})

