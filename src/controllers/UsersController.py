
from datetime import datetime

from Cheese.metadata import Metadata
from Cheese.appSettings import Settings
from Cheese.cheeseController import CheeseController as cc
from Cheese.httpClientErrors import *

from src.repositories.usersRepository import UsersRepository as ur
from src.repositories.accPassRepository import AccPassRepository as apr
from src.repositories.machinesRepository import MachinesRepository as mr

#@controller /users;
class UsersController(cc):

    #@post /register;
    @staticmethod
    def register(server, path, auth):
        args = cc.readArgs(server)
        cc.checkJson(["MAIL", "PASSWORD"], args)

        mail = args["MAIL"]
        password = Metadata.encode(args["PASSWORD"], Settings.passKey)

        cc.getHeadersDict(server)

        if (ur.validateEmail(mail)):
            raise Conflict("Email is already registered")

        userModel = ur.model()
        userModel.setAttrs(email=mail, enabled=True)
        ur.save(userModel)

        passModel = apr.model()
        passModel.setAttrs(user_id=userModel.id, password=password)
        apr.save(passModel)

        UsersController.registerMachine(server, userModel)

        return cc.createResponse({"STATUS": "OK"})

    #@get /login;
    @staticmethod
    def login(server, path, auth):
        return cc.createResponse({"STATUS": "OK"})


    # METHODS

    @staticmethod
    def registerMachineWithHeaders(headers, ip, userModel):
        userAgent = ""
        platform = ""
        if ("User-Agent" in headers.keys()):
            userAgent = headers["User-Agent"]
        if ("sec-ch-ua-platform" in headers.keys()):
            platform = headers["sec-ch-ua-platform"]

        machineModel = mr.model()
        machineModel.setAttrs(
            ip = ip,
            user_id = userModel.id,
            user_agent = userAgent,
            platform = platform,
            origin_date = datetime.now(),
            last_connection = datetime.now(),
            verified = False,
            name = "Unknown"
        )
        mr.save(machineModel)

    @staticmethod
    def registerMachine(server, userModel):
        ip = cc.getClientAddress(server)
        headers = cc.getHeadersDict(server)

        UsersController.registerMachineWithHeaders(headers, ip, userModel)


