import matplotlib.pyplot as plt
import numpy as np

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
  #tuples = [[0.0,0.0],[0.0,0.0],[0.0,0.0]]
  tuples = []
  for i in range(0, numflows):
    tuples.append([0.0,0.0])
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
    if source == 4 and flow == 0 and event == "-":
      tuples[flow][0] += 1
#    if source == 1 and flow == 0 and event == "-":
#      tuples[flow][0] += 1
    if event == "d":
      tuples[flow][1] += 1
  retval = []
  for i in range(0, numflows):
    if tuples[i][0] == 0:
      retval.append(0.0)
    else:
      retval.append(100.0 * tuples[i][1] / tuples[i][0])
  return retval    
  return [100.0 * tuples[0][1]/tuples[0][0],100.0 * tuples[1][1]/tuples[1][0],100.0 * tuples[2][1]/tuples[2][0]]
  return tuples


def main():
  #code 
  numflows = 2
  files = ["Reno.DropTail.out", "Reno.RED.out", "Sack1.DropTail.out", "Sack1.RED.out"]
  labels = []
  for file in files:
    spl = file.split('.')
    labels.append(spl[0] + "/" + spl[1])
  cbr = [2,4,6,8,10]
  loss = []
  bw = []
  for i in range(0, numflows):
    loss.append([])
    bw.append([])
  for file in files:
    l = parsePacketLoss(file, numflows=2)
    for i in range(0, len(l)):
      loss[i].append(l[i])
    b = parseBandwidth(file, numflows=2)
    for i in range(0, len(b)):
      bw[i].append(b[i])

  N = 4
  width = .35
  ind = np.arange(N)
  fig, ax = plt.subplots()
  rects1 = ax.bar(ind, bw[0], width, color='r')

  rects2 = ax.bar(ind + width, bw[1], width, color='y')
  ax.set_ylabel('Bandwidth (Mb)')
  ax.set_title('Influence of Queueing')
  ax.set_xticks(ind + width)
  ax.set_xticklabels(labels)
  ax.legend((rects1[0], rects2[0]), ('CBR', 'TCP'))
  plt.show()
  fig, ax = plt.subplots()
  rects1 = ax.bar(ind, loss[0], width, color='r')
  rects2 = ax.bar(ind + width, loss[1], width, color='y')
  ax.set_ylabel('Loss Percentage (%)')
  ax.set_xticks(ind + width)
  ax.set_xticklabels(labels)
  ax.legend((rects1[0], rects2[0]), ('CBR', 'TCP'))
  plt.show()
  return
  

  plt.subplot(2,1,1)
  plt.title('NewReno/Reno')
  plt.ylabel('Loss Percentage (%)')
  for i in range(0,numflows):
    plt.plot(cbr,loss[i])
  plt.legend(['CBR', 'NewReno', 'Reno'], loc='upper left')
  plt.subplot(2,1,2)
  plt.ylabel('Bandwidth (Mb)')
  for i in range(0,numflows):
    plt.plot(cbr,bw[i])
  plt.legend(['CBR', 'NewReno', 'Reno'], loc='upper left')
  plt.show()
  #plt.savefig('NRxR.png')
  return

if __name__=="__main__":
  main()
