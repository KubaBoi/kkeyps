
from Cheese.cheeseRepository import CheeseRepository

#@repository machines;
#@dbscheme (id, ip, user_id, verified, origin_date, last_connection, name, user_agent, platform);
#@dbmodel Machine;
class MachinesRepository(CheeseRepository):
    
    #@query "select * from machines where user_id=:userId and ip=:ip";
    #@return one;
    @staticmethod
    def findMachineByUserIdAndIp(userId, ip):
        return CheeseRepository.query(userId=userId, ip=ip)