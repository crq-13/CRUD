import uuid

class ClientModel:
    def __init__(self, name, company, email, position, uid=None):
        self.name = name
        self.email = email
        self.position = position
        self.company = company
        self.uid = uid or uuid.uuid4()

    def to_dict(self):
        return vars(self)

    @staticmethod
    def schema():
        return['name', 'company', 'email', 'position', 'uid']