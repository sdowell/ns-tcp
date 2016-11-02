
def parseBandwidth():
  pass

def parsePacketLoss(filename):
  with open(filename) as f:
    lines = f.readlines()
  for line in lines:
     print line
  return


def main():
  #code
  parsePacketLoss("out.nam")
  pass

if __name__=="__main__":
  main()
