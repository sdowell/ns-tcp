import matplotlib.pyplot as plt

def parseBandwidth(filename,time=10, numflows=3):
  bws = [0.0,0.0,0.0]
  bws = []
  for i in range(0, numflows):
    bws.append(0.0)
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
    if source == 1 and dest == 2 and event == "-":
      bws[flow] += size
#    if source == 1 and dest == 2 and flow == 1 and event == "-":
#      bws[flow] += size
#    if source == 1 and dest == 2 and flow == 2 and event == "-":
#      bws[flow] += size
#    if source == 1 and dest == 2 and flow == 0 and event == "-":
#      bws[flow] += size
  for i in range(0, numflows):
    bws[i] /= time
    bws[i] *= 8
    bws[i] /= 1000000
  return bws
  return [bws[0]/time,bws[1]/time,bws[2]/time]
  return [(bws[0] * 8.0)/(time * 1000000),(bws[1] * 8.0)/(time * 1000000),(bws[2] * 8.0)/(time * 1000000)]
  #return bws

def parsePacketLoss(filename, numflows=3):
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
      
  return [100.0 * tuples[0][1]/tuples[0][0],100.0 * tuples[1][1]/tuples[1][0],100.0 * tuples[2][1]/tuples[2][0]]
  return tuples


def main():
  #code 
  numflows = 3
  files = ["2.out", "4.out", "6.out", "8.out", "10.out"]
  cbr = [2,4,6,8,10]
  loss = []
  bw = []
  for i in range(0, numflows):
    loss.append([])
    bw.append([])
  for file in files:
    l = parsePacketLoss(file)
    for i in range(0, len(l)):
      loss[i].append(l[i])
    b = parseBandwidth(file)
    for i in range(0, len(b)):
      bw[i].append(b[i])
  plt.subplot(2,1,1)
  plt.title('Reno/Reno')
  plt.ylabel('Loss Percentage (%)')
  for i in range(0,numflows):
    plt.plot(cbr,loss[i])
  plt.legend(['CBR', 'Reno', 'Reno'], loc='upper left')
  plt.subplot(2,1,2)
  plt.ylabel('Bandwidth (Mb)')
  for i in range(0,numflows):
    plt.plot(cbr,bw[i])
  plt.legend(['CBR', 'Reno', 'Reno'], loc='upper left')
  #plt.show()
  plt.savefig('RxR.png')
  return

if __name__=="__main__":
  main()
