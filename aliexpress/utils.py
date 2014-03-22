import json
import httplib2,urllib
import hmac,hashlib
from urlparse import urlparse,parse_qs,urljoin,urlunparse
from BeautifulSoup import BeautifulSoup



class Aliexpress(object):

    def __init__(self,client_id,client_secret):
        self.http = httplib2.Http()
        self.client_id =client_id
        self.client_secret = client_secret

    def post_product(self,product_data):
        api_url = "http://gw.api.alibaba.com:80/openapi/param2/1/aliexpress.open/api.postAeProduct/%s"%self.client_id
        product_data = {
            'detail' : 'description',
            'deliveryTime' : 3,
            'promiseTemplateId':1,
            'categoryId' : 1,
            'subject' : 'title',
            'keyword' : 'keywords',
            'productMoreKeywords1':'keywords',
            'productMoreKeywords2':'keywords',
            'productPrice': 'price',
            'freightTemplateId' : 1,
            'isImageWatermark' : 'false',
            'imageURLs':'0;sfd;',
            'productUnit':'100000015',
            'packageType' : "false",
            'packageLength' : 100,
            'packageWidth':100,
            'packageHeight' : 100,
            'grossWeight' : 0.2,

        }

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

        salt = url_path + parsed_query_string

        h = hmac.new(str(self.client_secret), salt, hashlib.sha1)
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

    def auth(self,account,password,redirect_url):

        auth_url = 'http://gw.api.alibaba.com/auth/authorize.htm?client_id=%s&site=aliexpress&redirect_uri=%s'%(self.client_id,redirect_url)
        signature_url = self.get_aop_signature(auth_url, is_auth=True)
        headers,content = self.http.request(signature_url,"GET")
        if headers['status'] == '200':
            fields = {}
            main_wrap = BeautifulSoup(content).find('form')
            for field in main_wrap.findAll('input',attrs={'type':lambda x: x in ['hidden','text','checkbox','password']}):
                fields[field['name']] = field['value']

            fields['account'] = account
            fields['password'] = password
            _headers = {'Content-type': 'application/x-www-form-urlencoded'}
            _headers['Cookie']= headers['set-cookie']
            headers,content = self.http.request(signature_url, "POST",urllib.urlencode(fields),headers=_headers)

            if headers['status'] == '302':
                headers,content = self.http.request(headers['location'], "GET")
                return content





    def get_token(self,code,redirect_url = "",is_refresh = False):

        if is_refresh:
            token_url = "https://gw.api.alibaba.com/openapi/param2/1/system.oauth2/getToken/%s?grant_type=refresh_token&client_id=%s&client_secret=%s&refresh_token=%s"%(self.client_id,self.client_id,self.client_secret,code)
        else:
            token_url = "https://gw.api.alibaba.com/openapi/http/1/system.oauth2/getToken/%s?grant_type=authorization_code&need_refresh_token=true&client_id=%s&client_secret=%s&redirect_uri=%s&code=%s"%(self.client_id,self.client_id,self.client_secret,redirect_url,code)

        #print(token_url)
        _headers = {'Content-type': 'application/x-www-form-urlencoded'}

        headers,content = self.http.request(token_url, "POST", headers=_headers)

        if headers['status'] == '200':
            response = json.loads(content)
            return response


