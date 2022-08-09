
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
        for machine in machines:
            reqText = f"https://geo.ipify.org/api/v2/country,city,vpn?apiKey={Settings.geoApiKey}&ipAddress={machine.ip}"
            Logger.info(f"Sending GET request: {reqText}")
            req = requests.get(reqText)

            if (req.status_code != 200):
                Logger.fail("Fail while getting info about machine")
            else:
                jsn = json.loads(req.text)
                Logger.info(json.dumps(jsn, indent=4, sort_keys=True))
                setattr(machine, "city", jsn["location"]["city"])
                setattr(machine, "region", jsn["location"]["region"])
                setattr(machine, "country", jsn["location"]["country"])
                setattr(machine, "lat", jsn["location"]["lat"])
                setattr(machine, "lng", jsn["location"]["lng"])
                setattr(machine, "proxy", jsn["proxy"]["proxy"])
                setattr(machine, "vpn", jsn["proxy"]["vpn"])
                setattr(machine, "tor", jsn["proxy"]["tor"])

        return cc.createResponse({"MACHINES": cc.modulesToJsonArray(machines)})

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

