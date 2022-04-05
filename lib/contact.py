class Contact:
    '''
    Contact class to simplify contact info passing
    '''
    name = 'default name'
    email = 'default email'

    def __init__(self, name:str='', email:str='') -> None:
        self.name = name
        self.email = email


    def set_name(self, name:str):
        '''
        Name setter
        '''
        self.name = name


    def get_name(self):
        '''
        Name getter
        '''
        return self.name


    def set_email(self, email:str):
        '''
        Email setter
        '''
        self.email = email


    def get_email(self):
        '''
        Email getter
        '''
        return self.email
