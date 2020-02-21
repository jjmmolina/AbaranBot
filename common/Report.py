import json

class Report:
    """ Clase que representa un Report"""
    def __init__(self, thumbnail, type, hazard, address, status, organization, values):

        self.thumbnail = thumbnail
        self.type = type
        self.hazard = hazard
        self.address = address
        self.status = status
        self.organization = organization
        self.values = values


    def toString(self):
        report = json.dumps({"thumbnail": self.thumbnail,
                             "type": self.type, "hazard": self.hazard,
                             "status": self.status,
                             "address": self.address,"organization": self.organization,
                             })
        return (report)