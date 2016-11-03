
def parseBandwidth(filename,time=10):
  bws = [0.0,0.0,0.0]
  with open(filename) as f:
    lines = f.readlines()
  for line in lines:
    words = line.split()
    if words[2] == "*":
      continue
    event = words[0]
    source = int(words[4])
    dest = int(words[6])
    protocol = words[8]
    size = int(words[10])
    flow = int(words[12])
    if source == 1 and dest == 2 and flow == 1 and event == "-":
      bws[flow] += size
    if source == 1 and dest == 2 and flow == 2 and event == "-":
      bws[flow] += size
    if source == 1 and dest == 2 and flow == 0 and event == "-":
      bws[flow] += size
  return [bws[0]/time,bws[1]/time,bws[2]/time]
  return bws

def parsePacketLoss(filename):
  tuples = [[0.0,0.0],[0.0,0.0],[0.0,0.0]]
  with open(filename) as f:
    lines = f.readlines()
  for line in lines:
    words = line.split()
    if words[2] == "*":
      continue
    event = words[0]
    source = int(words[4])
    dest = int(words[6])
    protocol = words[8]
    size = int(words[10])
    flow = int(words[12])
    if source == 0 and flow == 1 and event == "-":
      tuples[flow][0] += 1
    if source == 4 and flow == 2 and event == "-":
      tuples[flow][0] += 1
    if source == 1 and flow == 0 and event == "-":
      tuples[flow][0] += 1
    if event == "d":
      tuples[flow][1] += 1
    continue
    index = 0
    while index < len(words):
      flow = -1
      if words[index] == "-c":
        index += 1
        flow = int(words[index])
        if words[0] == "d":
          dropped[flow] += 1
      #  elif words[0] == "-":
      #index += 1
      
  return [tuples[0][0]/tuples[0][1],tuples[1][0]/tuples[1][1],tuples[2][0]/tuples[2][1]]
  return tuples


def main():
  #code
  print parsePacketLoss("out.nam")
  print parseBandwidth("out.nam")
  pass

if __name__=="__main__":
  main()
