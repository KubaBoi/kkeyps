
from Cheese.cheeseRepository import CheeseRepository

#@repository passwords;
#@dbscheme (id, user_id, user_name, web, password);
#@dbmodel Password;
class PasswordsRepository(CheeseRepository):
    
    #@query "select * from passwords where user_id=:userId and web=:web and user_name=:userName;";
    #@return one;
    @staticmethod
    def findByUserIdAndWebAndUserName(userId, web, userName):
        return CheeseRepository.query(userId=userId, web=web, userName=userName)

    #@query "select * from passwords where user_id=:userId and web=:web;";
    #@return array;
    @staticmethod
    def findByUserIdAndWeb(userId, web):
        return CheeseRepository.query(userId=userId, web=web)