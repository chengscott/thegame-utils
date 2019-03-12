import pygal
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-f', dest='fileName', default='log.txt')
parser.add_argument('-t', dest='title', default='reward')
args = parser.parse_args()

f = open(args.fileName)
trainList = []
last_timestep = 0
total_reward = 0
episode = []

for line in f:
  parse = line.split()
  if parse[0] == "timestep":
    timestep, reward = int(parse[1]), int(parse[3])
    if last_timestep > timestep:
      trainList.append(episode)
      episode = []
      total_reward = 0
    total_reward += reward
    episode.append((timestep, total_reward))
    last_timestep = timestep

trainList.append(episode)
f.close()

line_chart = pygal.XY(
    title=args.title,
    x_title='episode',
    y_title='score',
    show_legend=False,
)

#for i, episode in enumerate(trainList):
#  line_chart.add(str(i), episode)
r = [(i + 1, x[-1][1]) for i, x in enumerate(trainList)]
line_chart.add('r', [(0, 0), *r])

#line_chart.render_in_browser()
line_chart.render_to_file('{}.svg'.format(args.title.lower().replace(' ', '_')))
