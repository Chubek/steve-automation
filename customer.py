import pandas as pd

class Customer:

    def __init__(self, email, date, retailer_group, segment, address):

        self.email = email
        self.date = date
        self.retailer_group = retailer_group
        self.segment = segment
        self.address = address


    def return_info(self):
        return (self.address.name, self.address.address, self.address.zip, self.address.soc, self.email, self.date, self.retailer_group, self.segment)


