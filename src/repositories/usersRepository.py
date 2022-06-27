
from Cheese.cheeseRepository import CheeseRepository

#@repository users;
#@dbscheme (id, email, enabled);
#@dbmodel User;
class UsersRepository(CheeseRepository):
    
    #@query "select case when exists
    #       (select * from users u where u.email = :email)
    #       then cast(1 as bit)
    #       else cast(0 as bit) end;";
    #@return bool;
    @staticmethod
    def validateEmail(email):
        return CheeseRepository.query(email=email)