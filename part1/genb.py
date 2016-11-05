import sys
import os
def main(args):
  for i in range(0, 11):
    cmd = "ns ../part1b.tcl " + str(i) + " " + args[0]
    os.system(cmd)

if __name__=="__main__":
  main(sys.argv[1:])
