# -*- coding:gb2312

import urllib
import urllib2
import httplib
import os

def GB2UTF(gb_str):
        return unicode(gb_str, "GB2312").encode("utf-8")

class TicketOrder(object):
    cookie = {}
    header ={}
    order_post = {}
    login_form = {}
    url = ""
    username = ""
    password = ""

    #pass in the username and password of the user and register the cookies to the server
    def login(self, username, password):
        conn = httplib.HTTPConnection("dynamic.12306.cn:80")
        rcode = self.get_randcode(r"/otsweb/passCodeAction.do?rand=lrand",
                                  r"login.png")
        self.login_form["randCode"] = rcode
        self.login_form["loginUser.user_name"] = username
        self.login_form["user.password"] = password
        conn.request("POST", r"/otsweb/loginAction.do?method=login",
                     urllib.urlencode(self.login_form), self.header)
        response = conn.getresponse()
        conn.close()
        print "[+] Get response from login!"
        print response.getheaders()
        print response.read()

    #post the ticket order params to the server
    def post_order(self, url, order_body, header):
        conn = httplib.HTTPConnection("dynamic.12306.cn:80")
        rcode = self.get_randcode(r"/otsweb/passCodeAction.do?rand=randp", r"order.png")
        self.order_post["randCode"] = rcode
        conn.request("POST", url, urllib.urlencode(order_body), header)
        response = conn.getresponse()
        conn.close()
        print "[+] Get response from post order!"
        print response.getheaders()
        print response.read()

    #retrieve the randcode pic to the local file, send specific cookies
    def get_randcode(self, url, filepath):
        conn = httplib.HTTPConnection("dynamic.12306.cn:80")
        conn.request("GET", url, headers=self.header)
        response = conn.getresponse()
        if os.path.exists(filepath):
            os.remove(filepath)
        fcode = open(filepath, "wb+")
        fcode.writelines(response.read())
        fcode.close()
        conn.close()
        os.startfile(filepath)
        return raw_input("Random Code:")

    def __init__(self):
        self.url = "/otsweb/order/confirmPassengerAction.do?%s" % \
                   urllib.urlencode({"method": "confirmPassengerInfoSingle"})
        self.header = {"Host":"dynamic.12306.cn", "Connection":"keep-alive", "Cache-Control":"max-age=0",
                       "Origin":r"http://dynamic.12306.cn",
                       "User-Agent":r"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2",
                       "Content-Type":r"application/x-www-form-urlencoded",
                       "Accept":r"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                       "Referer":r"htt p://dynamic.12306.cn/otsweb/order/confirmPassengerAction.do?method=init",
                       "Accept-Encoding":"gzip,deflate,sdch", "Accept-Language":"en-US,zh-CN;q=0.8,zh;q=0.6",
                       "Accept-Charset":"GBK,utf-8;q=0.7,*;q=0.3"}
        self.order_post = {"org.apache.struts.taglib.html.TOKEN":"bee25e7e253045759500561387540994",
                           "textfield":GB2UTF("中文或拼音首字母"),
                           "checkbox0":"0",
                           "orderRequest.train_date":"2011-12-15",
                           "orderRequest.train_no":"24000000T10E",
                           "orderRequest.station_train_code":"T1",
                           "orderRequest.from_station_telecode":"BXP",
                           "orderRequest.to_station_telecode":"CSQ",
                           "orderRequest.seat_type_code":"",
                           "orderRequest.ticket_type_order_num":"",
                           "orderRequest.bed_level_order_num":"000000000000000000000000000000",
                           "orderRequest.start_time":"16:04",
                           "orderRequest.end_time":"07:38",
                           "orderRequest.from_station_name":GB2UTF("北京西"),
                           "orderRequest.to_station_name":GB2UTF("长沙"),
                           "orderRequest.cancel_flag":"1",
                           "orderRequest.id_mode":"Y",
                           "passengerTickets":GB2UTF("3,3,罗成,1,430481198804250037,15010292867,N"),
                           "oldPassengers":GB2UTF("罗成,1,430481198804250037"),
                           "passenger_1_seat":"3",
                           "passenger_1_ticket":"3",
                           "randCode":"ENBF",
                           "orderRequest.reserve_flag":"A"}
        self.cookie = {"Cookie":"JSESSIONID=58400DA0EE1247AA61CC3CA1C1E4D6BB; T0egrhEC8V=MDAwM2IyODZkZjgwMDAwMDAwMDYweCQjaxUxMzIzNzkyNTQx"}
        self.header.update(self.cookie)
        self.login_form = {"loginUser.user_name":"starmate",
                           "nameErrorFocus":"",
                           "user.password":"52408812",
                           "passwordErrorFocus":"",
                           "randCode":"",
                           "randErrorFocus":""}

def main():
    ticket_order = TicketOrder()

    ticket_order.username = raw_input("Username:")
    ticket_order.password = raw_input("Password:")
    #ticket_order.login(ticket_order.username, ticket_order.password)
    
    post_url = r"/otsweb/order/confirmPassengerAction.do?" + \
               urllib.urlencode({"method":"confirmPassengerInfoSingle"})
    ticket_order.post_order(post_url, ticket_order.order_post,
                            ticket_order.header)
    print "[+] Post order finished, check the website!"
    
if __name__ == "__main__":
    main()