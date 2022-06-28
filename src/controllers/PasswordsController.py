
from Cheese.cheeseController import CheeseController as cc
from Cheese.httpClientErrors import *

from src.tools.GateKeeper import GateKeeper

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
            psw.password = u"\u2022"*10

        return cc.createResponse({"PASSWORDS": cc.modulesToJsonArray(passwords)})

    #@post /create;
    @staticmethod
    def create(server, path, auth):
        args = cc.readArgs(server)
        cc.checkJson(["USER_NAME", "WEB", "PASSWORD"], args)

        userName = args["USER_NAME"]
        web = args["WEB"]
        psw = GateKeeper.encode(args["PASSWORD"])
        
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

        psw = GateKeeper.decode(pswModel.password)

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

    #@get /getByWeb;
    @staticmethod
    def getByWeb(server, path, auth):
        args = cc.getArgs(path)
        cc.checkJson(["web"], args)

        userModel = ur.findOneBy("email", auth["login"]["login"])
        passwords = pr.findByUserIdAndWeb(userModel.id, args["web"])

        for psw in passwords:
            psw.password = "HIDDEN"

        return cc.createResponse({"PASSWORDS": cc.modulesToJsonArray(passwords)})

    #@post /updateKey;
    @staticmethod
    def updateKey(server, path, auth):
        args = cc.readArgs(server)
        cc.checkJson(["NK", "OK"], args)

        GateKeeper.sendConfirmation(args["NK"], args["OK"], cc.getClientAddress(server))

        return cc.createResponse({"STATUS": "OK"})

    #@get /confirmKeyUpdate;
    @staticmethod
    def confirmKeyUpdate(server, path, auth):
        args = cc.getArgs(path)
        cc.checkJson(["hash"], args)

        GateKeeper.updateKey(args["hash"], cc.getClientAddress(server))

        return cc.createResponse({"STATUS": "OK"})
