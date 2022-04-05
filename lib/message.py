from lib.contact import Contact

class Message:
    '''
    Simple message class
    '''
    sender = Contact()
    receiver = Contact()
    subject = 'default subject'
    content = 'default content'


    def __init__(
        self,
        sender:Contact=Contact(),
        receiver:Contact=Contact(),
        subject:str='',
        content:str='') -> None:
        '''
        (default) Constructor
        '''
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.content = content


    def update_subject(self, subject:str):
        '''
        update subject method
        '''
        self.subject = subject


    def update_content(self, content:str):
        '''
        update content method
        '''
        self.content = content


    def update_sender(self, sender:Contact):
        '''
        update sender information
        '''
        self.sender = sender


    def update_receiver(self, receiver:Contact):
        '''
        update receiver information
        '''
        self.receiver = receiver


    def print_msg(self):
        '''
        simple print
        '''
        print(f'Sender: {self.sender.name} <{self.sender.email}>')
        print(f'Receiver: {self.receiver.name} <{self.receiver.email}>')
        print(f'Message Subject: "{self.subject}"')
        print(f'Message Content: "{self.content}"')
