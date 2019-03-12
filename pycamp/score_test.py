import os
import sys
import subprocess
import multiprocessing as mp
from server_api import Server
from time import sleep
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-y', dest='year', default='2018')
parser.add_argument('-p', dest='port', default='50052')
args = parser.parse_args()

test_agents = os.listdir(f'thegame-agent/{args.year}')

def run_client(agent):
  subprocess.run(['python', f'thegame-agent/{args.year}/{agent}', f'localhost:{args.port}'], stdout=subprocess.DEVNULL, stderr=sys.stdout)

for agent in test_agents:
  for i in range(10):
    svr = Server(server='../thegame-server', port=int(args.port))
    svr.start()
    sleep(0.5)
    cp = mp.Process(target=run_client, args=(agent,))
    cp.start()
    sleep(0.5)
    for step in range(15000):
      sleep(0.001)
      svr.sync()
    sys.stdout.flush()
    sleep(0.5)
    cp.terminate()
    sleep(0.5)
    svr.terminate()
    sleep(0.5)
    print('agent', agent)
    print('****************************\n') #, file=sys.stder)
