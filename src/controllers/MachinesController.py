
from datetime import datetime
from Cheese.cheeseController import CheeseController as cc
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

