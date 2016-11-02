
def parseBandwidth():
  pass

def parsePacketLoss(filename):
  tuples = [[0,0],[0,0],[0,0]]
  with open(filename) as f:
    lines = f.readlines()
  for line in lines:
    words = line.split()
    index = 0
    while index < len(words):
      event = words[0]
      source = int(words[4])
      dest = int(words[6])
      protocol = words[8]
      size = int(words[10])
      flow = int(words[12])
      if source == 0 && event == "-":
        tuples[flow][0]++
      if event == "d":
        dropped[flow][1]++
      continue
      
      flow = -1
      if words[index] == "-c":
        index++
        flow = int(words[index])
        if words[0] == "d":
          dropped[flow]++
        elif words[0] == "-"
      index++
      
      
  return tuples


def main():
  #code
  parsePacketLoss("out.nam")
  pass

if __name__=="__main__":
  main()
