'''
Created on Aug 31, 2010

@author: Chris Glass (tribaal@gmail.com)
'''

from optparse import OptionParser
from suds.client import Client
from suds.transport.https import WindowsHttpAuthenticated
import re
from painters import default_painter

class WindowsHttpAuthenticatedWithoutCarriageReturns(WindowsHttpAuthenticated):
    """This class is needed to talk to microsoft webservices, since they expect messages without any linefeeds and
    other gimmicks :("""
    
    def send(self, request):
        """Overrides HttpTransport.send() to strip the message of linefeeds and non-printing characters."""
        request.message = request.message.replace('\n', '').replace('\r', '').replace('\t','')
        # Remove all whitespaces between '>' and '<'
        request.message = re.sub(r'> *<', '><', request.message)
        return  WindowsHttpAuthenticated.send(self, request)


class Cartographer():
    
    client = None
    transport = None
    
    def __init__(self, transport=None, painter=default_painter()):
        self.transport = transport
        self.painter = painter
        
    def create_client(self, wsdl_url):
        client = None
        if self.transport:
            client = Client(wsdl_url, transport=self.transport)
        else:
            client = Client(wsdl_url)
            
        self.client = client
        return client
        
    def print_map(self, wsdl_url):
        """
            Prints the map for the webservice
        """
        self.painter.paint_map_header(wsdl_url)
        self.create_client(wsdl_url)
        self.print_methods(self.client)
        self.print_types(self.client)
        
        
    def print_types(self,client):
        for service_def in client.sd :
        # For each service definition (There can be several)
            self.painter.paint_types_header()
            for type in service_def.types:
                self.painter.paint_type(type, service_def, client)
            
            
    def print_methods(self,client):
        
        for service_def in client.sd :
            # For each service definition (There can be several)
            
            self.painter.paint_methods_header()
            """
            This piece of shit is so complex to read it hurts my brain. WTF did they use single char variable names
            in a modern programming language is beyond me
            """
            for port in service_def.ports:
                for method in port[1]: # Suds source is full of magic numbers. Theses guys are C engineers!!!
                    self.painter.paint_method(method, service_def)
    

    
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-u", "--url", action="store_const", const=0, dest="url")
    parser.add_option("-n", "--username", action="store_const", const=2, dest="username")
    parser.add_option("-p", "--password", action="store_const", const=0, dest="password")
    
    options, args = parser.parse_args()
    
    
    url = '' # Put a nice URL here
    user='' # Your username, if any
    passw='' # Your passowrd if any
    
    if options['url']:
        url = options['url']
        
    if options['password']:
        passw = options['password']
    
    if options['username']:
        user = options['username']
        
    ntlm = WindowsHttpAuthenticatedWithoutCarriageReturns(username=user, password=passw)
    c = Cartographer(ntlm)
    c.print_map(url)
    
    
