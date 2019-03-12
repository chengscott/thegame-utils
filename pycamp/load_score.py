from argparse import ArgumentParser
from collections import defaultdict
import pygal

parser = ArgumentParser()
parser.add_argument('-f', dest='fileName', default='log')
parser.add_argument('-t', dest='title', default='title')
args = parser.parse_args()

scoreList = []

def loadFile(filename):
  global scoreList
  with open(filename) as f:
    agent, score = '', 0
    for line in f:
      if line.strip():
        key, *values = line.split()
        if key == '****************************':
          scoreList.append((agent, score))
          agent, score = '', 0
        elif key == 'agent':
          agent = values[0][:-3]
        elif key == 'score':
          score = int(values[0])

loadFile('log_2017')
loadFile('log_2018')

scoreDict = defaultdict(list)
for agent, score in scoreList:
  scoreDict[agent].append(score)
for agent, score in scoreDict.items():
  scoreDict[agent] = sorted(score)[1:-1]

scoreList = [(agent, score, sum(score) / len(score)) for agent, score in scoreDict.items() if sum(score) != 0]
sorted_score_list = sorted(scoreList, key=lambda x: x[2])
print(sorted_score_list)

chart = pygal.Box(title=args.title, y_title='score', legend_at_bottom=True)

for a, s, _ in sorted_score_list:
  chart.add(a, s)

chart.render_to_file('{}.svg'.format(args.title.lower().replace(' ', '_')))
#chart.render_in_browser()
