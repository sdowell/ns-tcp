import matplotlib.pyplot as plt
import numpy as np

def parseBandwidth(filename,time=5, numflows=3):
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
    if float(words[2]) > 5.5:
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
    if source == 0 and flow == 0 and event == "-":
      tuples[flow][0] += 1
    if source == 4 and flow == 1 and event == "-":
      tuples[flow][0] += 1
    if source == 6 and flow == 2 and event == "-":
      tuples[flow][0] += 1
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

def parseLatency(filename, numflows=3):
  latency = []
  sendtime = []
  for flow in range(0, numflows):
    sendtime.append({})
    latency.append([])
  with open(filename) as f:
    lines = f.readlines()
  for line in lines:
    words = line.split()
    if words[2] == "*":
      continue
    if float(words[2]) > 5.5:
      continue
    event = words[0]
    time = float(words[2])
    source = int(words[4])
    dest = int(words[6])
    protocol = words[8]
    size = int(words[10])
    flow = int(words[12])
    index = int(words[14])
    if source == 0 and flow == 0 and event == "-":
      sendtime[flow][index] = time
    if source == 4 and flow == 1 and event == "-":
      sendtime[flow][index] = time
    if source == 6 and flow == 2 and event == "-":
      sendtime[flow][index] = time
    if dest == 3 and event == "r":
      latency[flow].append(time - sendtime[flow][index])
    if dest == 5 and event == "r":
      latency[flow].append(time - sendtime[flow][index])
    if dest == 7 and event == "r":
      latency[flow].append(time - sendtime[flow][index])
  retvals = []
  for i in range(0, numflows):
    retvals.append(np.mean(latency[i]) * 1000)
  return retvals
def main():
  #code 
  nflows = 3
  files = ["DropTail.out", "RED.out"]
  labels = []
  for file in files:
    spl = file.split('.')
    labels.append(spl[0])
  cbr = [2,4,6,8,10]
  loss = []
  bw = []
  latency = []
  for i in range(0, nflows):
    loss.append([])
    bw.append([])
    latency.append([])
  for file in files:
    l = parsePacketLoss(file, numflows=nflows)
    for i in range(0, len(l)):
      loss[i].append(l[i])
    b = parseBandwidth(file, numflows=nflows)
    for i in range(0, len(b)):
      bw[i].append(b[i])
    lat = parseLatency(file, numflows=nflows)
    for i in range(0, len(lat)):
      latency[i].append(lat[i])
  print latency
  print bw
  N = 2
  width = .35
  ind = np.arange(N)
  ind = ind * 1.5
  fig, ax = plt.subplots()
  rects1 = ax.bar(ind, bw[0], width, color='r')
  rects2 = ax.bar(ind + width, bw[1], width, color='y')
  rects3 = ax.bar(ind + 2 * width, bw[2], width, color='g')
  ax.set_ylabel('Throughput (Mb)')
  ax.set_title('CBR Throughput for DropTail/RED')
  ax.set_xticks(ind + width * 1.5)
  ax.set_xticklabels(labels)
  ax.legend((rects1[0], rects2[0], rects3[0]), ('1 KB @ 1 Mbps', '1 KB @ 1 Mbps', '.5 KB @ .6 Mbps'))
  #plt.show()
  plt.savefig("Throughput22.png")
  fig, ax = plt.subplots()
  rects1 = ax.bar(ind, latency[0], width, color='r')
  rects2 = ax.bar(ind + width, latency[1], width, color='y')
  rects3 = ax.bar(ind + 2 * width, latency[2], width, color='g')
  ax.set_ylabel('Latency (ms)')
  ax.set_title('CBR Latency for DropTail/RED')
  ax.set_xticks(ind + width * 1.5)
  ax.set_xticklabels(labels)
  ax.legend((rects1[0], rects2[0], rects3[0]), ('1 KB @ 1 Mbps', '1 KB @ 1 Mbps', '.5 KB @ .6 Mbps'))
  #plt.show()
  plt.savefig("Latency22.png")
  return
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
