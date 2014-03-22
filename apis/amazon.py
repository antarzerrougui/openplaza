import re,os
from boto.mws.connection import MWSConnection



class Amazon(object):
    def __init__(self):
        #self.mws = MWSConnection()
        self.mws = MWSConnection(host = 'mws.amazonservices.co.uk',Merchant='A3O0SQBUO1R6E',aws_access_key_id='AKIAJLZYYCFQSDPV2CSA',SellerId = '1903-0173-6891',aws_secret_access_key='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', debug=1)
    def get_product_info(self):
        pass

    def create_product(self):
        pass

    def update_product(self):
        pass

    def get_order_list(self):
        pass

    def get_order_info(self):
        pass

    def confirm_shipment(self):
        pass

    def add_tracking_info(self):
        pass

    def refund_order(self):
        pass


if __name__=="__main__":
    amazon = Amazon()
    orders = amazon.mws.list_orders(MarketplaceId = 'A1PA6795UKMFR9',CreatedAfter = '2014-02-15')
    print(orders)

