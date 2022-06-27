
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

