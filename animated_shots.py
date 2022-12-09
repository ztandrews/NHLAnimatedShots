from matplotlib import pyplot as plt
import random
import pandas as pd
from hockey_rink import NHLRink
import numpy as np
from datetime import datetime
import glob
from PIL import Image


game = pd.read_csv('single_game_shots.csv')

game['xCordAdjusted2'] = np.where(game['isHomeTeam']==1,(game['xCordAdjusted']),(game['xCordAdjusted']*-1))
game['yCordAdjusted2'] = np.where(game['isHomeTeam']==1,(game['yCordAdjusted']),(game['yCordAdjusted']*-1))

x_cords = game['xCordAdjusted2'].tolist()
y_cords = game['yCordAdjusted2'].tolist()
goal = game['goal'].tolist()
xgs = game['xG'].tolist()
period = game['period'].tolist()
home_goals_for = game['homeTeamGoals'].tolist()
away_goals_for = game['awayTeamGoals'].tolist()
is_home_team = game['isHomeTeam'].tolist()

adj_xgs = []
for x in xgs:
    adj = x*300
    adj_xgs.append(adj)
x = []
y = []
gx = []
gy = []
xg = []
gxg = []
plt.xlim([-100,100])
plt.ylim([-42.5, 42.5])
home_xg = 0
away_xg = 0
rink = NHLRink()
ax = rink.draw()
name = 'a'
for i in range(0, len(goal)):
    if is_home_team[i] == 1:
        home_xg = home_xg + xgs[i]
    else:
        away_xg = away_xg + xgs[i]
    plt.title("Vancouver Canucks @ New York Islanders\n2022-03-03\nPeriod " + str(period[i]) + "\nScore\nVAN " + str(away_goals_for[i]) + " - " + str(home_goals_for[i])+ " NYI " + "\nExpected Goals\nVAN "+ str(round(away_xg,3)) + ' - ' + str(round(home_xg,3)) +' NYI',size=7)
    plt.text(47,47,"NYI Shot Attempts",size=7)
    plt.text(-83, 47, "VAN Shot Attempts",size=7)
    if goal[i] == 1:
        gx.append(x_cords[i])
        gy.append(y_cords[i])
        gxg.append(adj_xgs[i])
    else:
        x.append(x_cords[i])
        y.append(y_cords[i])
        xg.append(adj_xgs[i])
    plt.scatter(x, y, xg, color="orange",zorder=10)
    plt.scatter(gx, gy, gxg, color="green",zorder=10)
    t=datetime.now()
    plt.savefig('game/'+name+'.png',dpi=300)
    name = name+'a'
    plt.pause(0.001)

def make_gif(frame_folder):
    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*")]
    frame_one = frames[0]
    frame_one.save("game_shots2.gif", format="GIF", append_images=frames,
               save_all=True, duration=200, loop=0)

make_gif("game")
