import subprocess as sp

def IPq(foo):
  return foo

def IPcheck(host):
  status,result = sp.getstatusoutput("ping -c1 -w2 " + str(host))
  if status == 0:
      print("System " + str(host) + " is UP !")
  else:
      print("System " + str(host) + " is DOWN !")
