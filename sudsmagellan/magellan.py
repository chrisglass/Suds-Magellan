'''
Created on Aug 31, 2010

@author: Chris Glass (tribaal@gmail.com)
'''

from optparse import OptionParser
from suds.client import Client
from suds.transport.https import WindowsHttpAuthenticated
import re

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
    
    def __init__(self, transport=None):
        self.transport = transport
        
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
        print '*' * 20
        print "MAGELLAN MAP FOR %s" % wsdl_url
        print '*' * 20
        print '*' * 20
        self.create_client(wsdl_url)
        self.print_methods(self.client)
        self.print_types(self.client)
        
        
    def print_types(self,client):
        for service_def in client.sd :
        # For each service definition (There can be several)
            xlate = service_def.xlate

            print 'TYPES:'
            print '*' * 20
            for type in service_def.types:
                webservice_object = client.factory.create(xlate(type[0]))
                print webservice_object  
            
            
    def print_methods(self,client):
        
        for service_def in client.sd :
            # For each service definition (There can be several)
            xlate = service_def.xlate
            
            print 'METHODS:'
            print '*' * 20
            """
            This piece of shit is so complex to read it hurts my brain. WTF did they use single char variable names
            in a modern programming language is beyond me
            """
            for port in service_def.ports:
                for method in port[1]: # Suds source is full of magic numbers. Theses guys are C engineers!!!
                    method_name = method[0]
                    signature = []
                    signature.append('(')
                    for signature_elt in method[1]:
                        signature.append(xlate(signature_elt[1]))
                        signature.append(' ')
                        signature.append(signature_elt[0])
                        signature.append(', ')
                    signature.append(')')
                    string_signature = ''.join(signature)
                    print "%s %s" % (method_name, string_signature)
    

    
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
    
    