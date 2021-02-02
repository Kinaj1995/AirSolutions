# Python3 code to generate the 
# random id using uuid1() 
  
import uuid 
  
# Printing random id using uuid1() 
print ("The random id using uuid1() is : ",end="") 
print (uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org')) 

uuid.uuid5()