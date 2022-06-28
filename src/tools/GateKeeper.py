
import string
import random

from Cheese.metadata import Metadata
from Cheese.appSettings import Settings
from Cheese.httpClientErrors import *
from Cheese.Logger import Logger

from src.tools.LetterMan import LetterMan

from src.repositories.passwordsRepository import PasswordsRepository as pr
from src.repositories.accPassRepository import AccPassRepository as apr

class GateKeeper:

    __key = ""
    __newKey = ""
    __hash = ""

    @staticmethod
    def sendConfirmation(newKey, oldKey, ip):
        if (ip != Settings.my_ip):
            raise Unauthorized("You are not me")
        if (oldKey != GateKeeper.__key and GateKeeper.__key != ""):
            raise Unauthorized("Key does not match")
        if (GateKeeper.__key == ""):
            GateKeeper.__key = oldKey

        psws = pr.findAll() + apr.findAll()
        try:
            for psw in psws:
                GateKeeper.decode(psw.password)
        except Exception as e:
            GateKeeper.__key = ""
            raise e

        GateKeeper.__newKey = newKey
        GateKeeper.__hash = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(200))

        Logger.adminInfo("Sending email for Key Update")

        LetterMan.sendMail("jakubanderle@outlook.cz",
         f"""
         <body>
         <a href='http://frogie.cz:7969/passwords/confirmKeyUpdate?hash={GateKeeper.__hash}'>{GateKeeper.__hash}</a>
         </body>"""
         , "Key Update")

    @staticmethod
    def updateKey(hash, ip):
        if (ip != Settings.my_ip):
            raise Unauthorized("You are not me")
        if (hash != GateKeeper.__hash):
            raise Unauthorized("Hash does not match")

        psws = pr.findAll()
        accPsws = apr.findAll()

        GateKeeper.updatePasswords(psws + accPsws)

    @staticmethod
    def updatePasswords(passwords):
        for psw in passwords:
            psw.password = GateKeeper.decode(psw.password)

        Settings.passKey = GateKeeper.__newKey
        GateKeeper.__key = GateKeeper.__newKey

        for psw in passwords:
            psw.password = GateKeeper.encode(psw.password)
            if (psw.modelName == "Password"):
                pr.update(psw)
            elif (psw.modelName == "AccPass"):
                apr.update(psw)

    @staticmethod
    def decode(text):
        if (GateKeeper.__key == ""):
            raise Unauthorized("GateKeeper does not allow you to enter")
        try:
            return Metadata.decode(text, GateKeeper.__key)
        except PermissionError:
            raise Unauthorized("GateKeeper does not allow you to enter")
        except Exception as e:
            raise e

    @staticmethod
    def encode(text):
        if (GateKeeper.__key == ""):
            raise Unauthorized("GateKeeper does not allow you to enter")
        return Metadata.encode(text, GateKeeper.__key)

