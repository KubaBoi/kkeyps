
from datetime import datetime
import json
import string
import random

from Cheese.resourceManager import ResMan
from Cheese.cheeseController import CheeseController as cc
from Cheese.httpClientErrors import *

from src.controllers.UsersController import UsersController as uc

from src.repositories.machinesRepository import MachinesRepository as mr
from src.repositories.usersRepository import UsersRepository as ur
from src.repositories.confirmationsRepository import ConfirmationsRepository as cr

from src.tools.LetterMan import LetterMan

#@controller /emails;
class EmailsController(cc):

    #@post /unknownMachine;
    @staticmethod
    def unknownMachine(server, path, auth):
        args = cc.readArgs(server)
        cc.checkJson(["headers", "ip", "login"], args)

        headers = json.loads(args["headers"])
        ip = args["ip"]
        login = args["login"].replace("'", "")

        code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))

        with open(ResMan.resources("emails", "regMail.html"), "r") as f:
            html = f.read().replace("$CODE$", code)

        userModel = ur.findOneBy("email", login)
        userModel.enabled = False
        ur.update(userModel)

        machineModel = mr.findMachineByUserIdAndIp(userModel.id, ip)
        if (machineModel == None):
            machineModel = mr.model()
            uc.registerMachineWithHeaders(headers, ip, userModel)
            machineModel = mr.find(machineModel.id)

        machineModel.last_connection = datetime.now()
        mr.update(machineModel)

        html = html.replace("$IP$", ip)
        html = html.replace("$ORIGIN_DATE$", machineModel.origin_date.strftime("%d.%m.%Y %H:%M:%S"))
        html = html.replace("$LAST_CONNECTION$", machineModel.last_connection.strftime("%d.%m.%Y %H:%M:%S"))
        html = html.replace("$USER_AGENT$", machineModel.user_agent)
        html = html.replace("$PLATFORM$", machineModel.platform)

        confModel = cr.model()
        confModel.setAttrs(
            machine_id=machineModel.id,
            code=code
        )
        cr.save(confModel)

        LetterMan.sendMail(login, html, "Machine confirmation")

        return cc.createResponse({"STATUS": "OK"})

    #@get /reg;
    @staticmethod
    def reg(server, path, auth):
        args = cc.getArgs(path)
        cc.checkJson(["code", "type"], args)

        confModel = cr.findOneBy("code", args["code"])
        machineModel = mr.find(confModel.machine_id)
        userModel = ur.find(machineModel.user_id)
        cr.delete(confModel)

        userModel.enabled = True
        ur.update(userModel)

        type = int(args["type"])
        if (type == 0):
            machineModel.verified = True
            mr.update(machineModel)
            return cc.createResponse({"STATUS": "Machine has been registered :)"})
        elif (type == 1):
            mr.delete(machineModel)
            return cc.createResponse({"STATUS": "Everything is ok :)"})
        else:
            mr.delete(machineModel)
            return cc.createResponse({"STATUS": "We have send you an email with your new password :)"})


    