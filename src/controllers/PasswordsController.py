
from Cheese.metadata import Metadata
from Cheese.appSettings import Settings
from Cheese.cheeseController import CheeseController as cc
from Cheese.httpClientErrors import *

from src.repositories.usersRepository import UsersRepository as ur
from src.repositories.passwordsRepository import PasswordsRepository as pr

#@controller /passwords;
class PasswordsController(cc):

    #@get /getMy;
    @staticmethod
    def getMy(server, path, auth):
        userModel = ur.findOneBy("email", auth["login"]["login"])
        
        passwords = pr.findBy("user_id", userModel.id)
        for psw in passwords:
            psw.password = "HIDDEN"

        return cc.createResponse({"PASSWORDS": cc.modulesToJsonArray(passwords)})

    #@post /create;
    @staticmethod
    def create(server, path, auth):
        args = cc.readArgs(server)
        cc.checkJson(["USER_NAME", "WEB", "PASSWORD"], args)

        userName = args["USER_NAME"]
        web = args["WEB"]
        psw = Metadata.encode(args["PASSWORD"], Settings.passKey)
        
        userModel = ur.findOneBy("email", auth["login"]["login"])

        passModel = pr.model()
        passModel.setAttrs(
            user_id=userModel.id,
            user_name=userName,
            web=web,
            password=psw
        )
        pr.save(passModel)

        return cc.createResponse({"STATUS": "Password has been created"})

    #@get /show;
    @staticmethod
    def show(server, path, auth):
        args = cc.getArgs(path)
        cc.checkJson(["web", "userName"], args)

        userModel = ur.findOneBy("email", auth["login"]["login"])
        pswModel = pr.findByUserIdAndWebAndUserName(userModel.id, args["web"], args["userName"])

        psw = Metadata.decode(pswModel.password, Settings.passKey)

        return cc.createResponse({"PASSWORD": psw})

    #@get /remove;
    @staticmethod
    def remove(server, path, auth):
        args = cc.getArgs(path)
        cc.checkJson(["web", "userName"], args)

        userModel = ur.findOneBy("email", auth["login"]["login"])
        pswModel = pr.findByUserIdAndWebAndUserName(userModel.id, args["web"], args["userName"])

        pr.delete(pswModel)

        return cc.createResponse({"STATUS": "Removed"})
