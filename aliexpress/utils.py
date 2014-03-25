import json,time,sys
import StringIO
import httplib2,urllib,requests
import hmac,hashlib
from urlparse import urlparse,parse_qs,urljoin,urlunparse
from BeautifulSoup import BeautifulSoup



class Aliexpress(object):
    def __init__(self,client_id,client_secret):
        self.http = httplib2.Http()
        self.client_id =client_id
        self.client_secret = client_secret
        self.post_headers = {'Content-type': 'application/x-www-form-urlencoded'}
        self.upload_headers = {'Content-type': 'multipart/form-data'}


    def get_shipping_templates(self,access_token):
        timestamp = time.time()*1000.0
        api_url = "https://gw.api.alibaba.com:443/openapi/param2/1/aliexpress.open/api.listFreightTemplate/%s?access_token=%s&_aop_timestamp=%d"%(self.client_id,access_token,timestamp)
        signature_url = self.get_aop_signature(api_url)
        r = requests.post(api_url)
        if r.status_code == 200:
            response = json.loads(r.text)
            if "success" in response:
                templates = response['aeopFreightTemplateDTOList']
                return templates
            #print(r.text)


    def upload_product(self,access_token,product_data):
        timestamp = time.time()*1000.0

        #access_token = '002f9182-2931-4769-9633-cab2237c0c3a'
        api_url = "https://gw.api.alibaba.com:443/openapi/param2/1/aliexpress.open/api.postAeProduct/%s?access_token=%s&_aop_timestamp=%d"%(self.client_id,access_token,timestamp)


        image = self.upload_temp_image(access_token,'http://www.digimotor.com/media/catalog/product/d/a/davina_product.jpg','davina.jpg')

        shipping_templates = self.get_shipping_templates(access_token)
        product_data = {
            'detail' : '<a href="">description</a>',
            'deliveryTime' : 3,
            'promiseTemplateId':1,
            'categoryId' : 200000377,
            'subject' : 'long wave wig',
            'keyword' : 'long wave wig',
            'productMoreKeywords1':'long wave wig',
            'productMoreKeywords2':'long wave wig',
            'productPrice': '199.99',
            'freightTemplateId' : shipping_templates[2]['templateId'],
            'isImageWatermark' : 'false',
            'imageURLs':image,
            'aeopAeProductSKUs':[],
            'productUnit':'100000015',
            'packageType' : "false",
            'packageLength' : 35,
            'packageWidth':54,
            'packageHeight' : 50,
            'grossWeight' : 0.2,
            'wsValidNum':30

        }
        signature_url = self.get_aop_signature(api_url,data=product_data)

        r = requests.post(signature_url,headers=self.post_headers)
        content = json.loads(r.text)


        print(content)


    def upload_temp_image(self,access_token,src_file,filename):
        timestamp = time.time()*1000.0
        api_url = "https://gw.api.alibaba.com:443/openapi/param2/1/aliexpress.open/api.uploadTempImage/%s?access_token=%s&_aop_timestamp=%d"%(self.client_id,access_token,timestamp)
        signature_url = self.get_aop_signature(api_url,data={'srcFileName':filename})
        if src_file:
            r = requests.get(src_file,stream=True)
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()

        r = requests.post(signature_url,data=open(filename,'rb'))
        if r.status_code == 200:
            response = json.loads(r.text)
            if "success" in response and response['success'] == True:
                return response['url']


    def get_category_by_id(self,access_token,id):
        timestamp = time.time()*1000.0
        api_url = "https://gw.api.alibaba.com:443/openapi/param2/1/aliexpress.open/api.getPostCategoryById/%s?access_token=%s&_aop_timestamp=%d"%(self.client_id,access_token,timestamp)
        signature_url = self.get_aop_signature(api_url,data={'cateId':id})

        r = requests.post(signature_url,headers=self.post_headers)
        print(r.text)

    def get_recommend_category_by_keyword(self,access_token,keyword):
        timestamp = time.time()*1000.0
        api_url = "https://gw.api.alibaba.com:443/openapi/param2/1/aliexpress.open/api.recommendCategoryByKeyword/%s?access_token=%s&_aop_timestamp=%d"%(self.client_id,access_token,timestamp)

        signature_url = self.get_aop_signature(api_url,data={'keyword':keyword})
        #print(signature_url)

        r = requests.post(signature_url, headers=self.post_headers)


        content = json.loads(r.text)
        if "success" in content and content['success'] == True:
            for c in content['cateogryIds']:
                self.get_category_by_id(access_token,c)


    def get_aop_signature(self,url,is_auth = False,data = None):
        """_aop_signature"""
        parsed_url = urlparse(url)
        parsed_query = parse_qs(parsed_url.query)

        if data and isinstance(data,dict):
            for k,v in data.iteritems():
                parsed_query.update({k:[str(v)]})

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

        r = requests.get(signature_url)

        #headers,content = self.http.request(signature_url,"GET")
        if r.status_code == 200:
            fields = {}
            main_wrap = BeautifulSoup(r.text).find('form')
            for field in main_wrap.findAll('input',attrs={'type':lambda x: x in ['hidden','text','checkbox','password']}):
                fields[field['name']] = field['value']

            fields['account'] = account
            fields['password'] = password
            r = requests.post(signature_url,data = fields,headers=self.post_headers,cookies=r.cookies)
            if r.status_code == 200:
                return r.text



    def get_token(self,code,redirect_url = "",is_refresh = False):
        if is_refresh:
            token_url = "https://gw.api.alibaba.com/openapi/param2/1/system.oauth2/getToken/%s?grant_type=refresh_token&client_id=%s&client_secret=%s&refresh_token=%s"%(self.client_id,self.client_id,self.client_secret,code)
        else:
            token_url = "https://gw.api.alibaba.com/openapi/http/1/system.oauth2/getToken/%s?grant_type=authorization_code&need_refresh_token=true&client_id=%s&client_secret=%s&redirect_uri=%s&code=%s"%(self.client_id,self.client_id,self.client_secret,redirect_url,code)

        r = requests.post(token_url,headers=self.post_headers)
        if r.status_code == 200:
            response = json.loads(r.text)
            if "access_token" in response:
                return response






if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')
    ali = Aliexpress('6456454','1kQ00Y3wgg')
    access_token = ali.get_token('953274e8-68a0-41d3-881f-92c1d70a5bf5',is_refresh= True)

    access_token = access_token['access_token']
    print(access_token)

    #ali.upload_temp_image(access_token,"",'/home/age/Workspaces/Python/plaza/aliexpress/banner.jpg')
    ali.get_recommend_category_by_keyword(access_token,'car cables')
    ali.upload_product(access_token ,{})
