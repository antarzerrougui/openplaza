import re,os,json,time,datetime
import httplib2,urllib
from BeautifulSoup import BeautifulSoup
import hmac,hashlib

from urlparse import urlparse,parse_qs,urljoin,urlunparse


class Aliexpress(object):
    def __init__(self):

        content = '{"refresh_token_timeout":"20140906211035000-0700","aliId":"17301527096","resource_owner":"cn1002489173","expires_in":"36000","refresh_token":"953274e8-68a0-41d3-881f-92c1d70a5bf5","access_token":"1ecdfbb7-fa54-4c40-bb55-9bd164209acb"}'
        response = json.loads(content)
        print(datetime.datetime.utcnow())
        refresh_token_timeout = response['refresh_token_timeout'][:14]
        print(time.time())
        #print(time.strptime(response['refresh_token_timeout']))
        print( time.localtime(1410009035))
        #1410009035.0

        exit()
        #self.mws = MWSConnection()
        self.http = httplib2.Http()
        auth_url = 'http://gw.api.alibaba.com/auth/authorize.htm?client_id=6456454&site=aliexpress&redirect_uri=http://localhost:8118'
        #self.http.request()
        signature_url = self.get_aop_signature(auth_url, is_auth=True)
        #print(signature_url)

        headers,content = self.http.request(signature_url,"GET")
        if headers['status'] == '200':
            #print(headers)
            fields = {}
            main_wrap = BeautifulSoup(content).find('form')
            for field in main_wrap.findAll('input',attrs={'type':lambda x: x in ['hidden','text','checkbox','password']}):
                #print(field['name'])
                fields[field['name']] = field['value']
                #print(field)

            fields['account'] = "ketu.lai@gmail.com"
            fields['password'] = "L150457l"
            #print(fields)
            _headers = {'Content-type': 'application/x-www-form-urlencoded'}
            _headers['Cookie']= headers['set-cookie']

            headers,content = self.http.request(signature_url, "POST",urllib.urlencode(fields),headers=_headers)
            print(headers)
            if headers['status'] == '302':
                print(headers['location'])


                headers,content = self.http.request(headers['location'], "GET")
                print(headers)
                auth_code = headers['content-location'][headers['content-location'].index("=")+1:]
                print(auth_code)
                self.get_token(auth_code)

        #print(headers)
        """ key : 1kQ00Y3wgg"""


    def get_token(self,code,is_refresh = False):
        token_url = "https://gw.api.alibaba.com/openapi/http/1/system.oauth2/getToken/6456454?grant_type=authorization_code&need_refresh_token=true&client_id=6456454&client_secret=1kQ00Y3wgg&redirect_uri=http://localhost:8118&code=%s"%code
        print(token_url)

        #signature_url = self.get_aop_signature(token_url,True)
        _headers = {}
        _headers = {'Content-type': 'application/x-www-form-urlencoded'}
        headers,content = self.http.request(token_url, "POST",headers=_headers)
        print(content)

        #print(aop_signature)

    def get_aop_signature(self,url,is_auth = False):

        """_aop_signature"""

        parsed_url = urlparse(url)
        parsed_query = parse_qs(parsed_url.query)
        parsed_query_string = ""
        for k in sorted(parsed_query):
            parsed_query_string += k+ parsed_query[k][0]
        url_path = ""
        if not is_auth :
            url_path = parsed_url.path.replace("/openapi/","")
            print(url_path)

            #url_path = urlunparse((parsed_url.scheme,parsed_url.netloc,parsed_url.path,None,None,None))
            #print(url_path)

        salt = url_path + parsed_query_string
        #print(salt)
        h = hmac.new("1kQ00Y3wgg", salt, hashlib.sha1)
        s = h.digest().encode('hex')
        aop_signature = s.upper()

        parsed_query['_aop_signature'] = [aop_signature,]

        _parsed_query = {}
        for q in parsed_query:
            _parsed_query[q] = parsed_query[q][0]

        _query = urllib.urlencode(_parsed_query)
        _query = urllib.unquote(_query)
        _url_path = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path,None, _query, None))
        return _url_path



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
    ali = Aliexpress()

    #orders = amazon.mws.list_orders(MarketplaceId = 'A1PA6795UKMFR9',CreatedAfter = '2014-02-15')
    #print(orders)

