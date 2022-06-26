
from Cheese.metadata import Metadata
from Cheese.appSettings import Settings
from Cheese.cheeseController import CheeseController as cc
from Cheese.httpClientErrors import *

from src.repositories.usersRepository import UsersRepository as ur
from src.repositories.accPassRepository import AccPassRepository as apr

#@controller /users;
class UsersController(cc):

    #@post /register;
    @staticmethod
    def register(server, path, auth):
        args = cc.readArgs(server)
        cc.checkJson(["MAIL", "PASSWORD"], args)

        mail = args["MAIL"]
        password = Metadata.encode(args["PASSWORD"], Settings.passKey)

        if (ur.validateEmail(mail)):
            raise Conflict("Email is already registered")

        userModel = ur.model()
        userModel.setAttrs(email=mail)
        ur.save(userModel)

        passModel = apr.model()
        passModel.setAttrs(user_id=userModel.id, password=password)
        apr.save(passModel)

        return cc.createResponse({"STATUS": "OK"})

    #@get /login;
    @staticmethod
    def login(server, path, auth):
        return cc.createResponse({"STATUS": "OK"})


