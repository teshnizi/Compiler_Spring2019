

class ActivationRecord:

    def __init__(self, params, control_link, access_link, return_address, temps):
        self.result = 0
        self.params = params #list
        self.access_link = access_link #address of activation record
        self.control_link = control_link
        self.return_address = return_address
        self.temps = temps  #tuples of (name, type,
