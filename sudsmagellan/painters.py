'''
Created on Sep 15, 2010

@author: Chris Glass (chirstopher.glass@divio.ch)
'''

class default_painter():
    
    def paint_method(self, method, service_def):
        method_name = method[0]
        signature = []
        signature.append('(')
        for signature_elt in method[1]:
            signature.append(service_def.xlate(signature_elt[1]))
            signature.append(' ')
            signature.append(signature_elt[0])
            signature.append(', ')
        signature.append(')')
        string_signature = ''.join(signature)
        print "%s %s" % (method_name, string_signature)
    
    def paint_type(self, type ,service_def, client):
        
        webservice_object = client.factory.create(service_def.xlate(type[0]))
        print webservice_object  


    def paint_methods_header(self):
        print '*' * 20
        print 'METHODS:'
        print '*' * 20
    
    def paint_types_header(self):
        print '*' * 20
        print 'Types:'
        print '*' * 20
        
    def paint_map_header(self, a_string=''):
        print '#' * 20
        print "MAGELLAN LISTING FOR %s" % a_string
        print '#' * 20
        print ''
        