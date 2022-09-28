import matplotlib.pyplot as plt
from Interval import *
import numpy as np
import matplotlib.pyplot as plt
from Interval import *
import cv2
import json
from Robot import Robot

if __name__ == "__main__":
    fig,ax = plt.subplots(figsize=(8,8))
    with open('room.json') as f:   
        data = json.load(f)
    obstacles = []
    for obstacle in data['obstacles']:
        params,center = obstacle['params'],obstacle['center']
        obstacles.append(Interval(*params,center))
    arena = cv2.imread("arena1.png")
    arena = (1-cv2.cvtColor(arena,cv2.COLOR_RGB2GRAY)/255).astype('int')
    
    for obstacle in obstacles:
        obstacle.draw(ax,'red')
    # plt.show()

    robot1 = Robot(200,200,np.pi/2,35,1.13)
    # robot2 = Robot(800,400, 0,35,1.13)
    # robot3 = Robot(400,400, 0.5,35,1.13)
    # robot4 = Robot(200,800, np.pi/2,35,1.13)

    # robot1.fellows = [robot2,robot3,robot4]
    # robot2.fellows = [robot1,robot3,robot4]
    # robot3.fellows = [robot1,robot2,robot4]
    # robot4.fellows = [robot1,robot2,robot3]
    robot1.set_environment(obstacles)
    
    

    for i in range(5000):
        plt.cla()
        ax.imshow(arena,cmap = plt.cm.gray_r,origin = 'lower')
        # ax. set_aspect('equal')
        ax.set_xlim([0, 1024])
        ax.set_ylim([0, 1024])
        # ax.imshow(arena,cmap = plt.cm.gray_r,origin = 'lower')
        # for obstacle in obstacles:
        #     obstacle.draw(ax,'red')
        for obstacle in obstacles:
            obstacle.draw(ax,'red')
        robot1.draw(ax)
        robot1.interval_hull.draw(ax,'blue')
        robot1.interval.draw(ax,'blue')
        # robot2.draw(ax)
        # robot2.interval_hull.draw(ax,'red')
        # robot2.interval.draw(ax,'red')
        # robot3.draw(ax)
        # robot3.interval_hull.draw(ax,'magenta')
        # robot3.interval.draw(ax,'magenta')
        # robot4.draw(ax)
        # robot4.interval_hull.draw(ax,'black')
        # robot4.interval.draw(ax,'black')
        # print(i, " ")
        v1,w1 = robot1.collision_free_command(ax)
            

            # v2,w2 = robot2.collision_free_command(ax)

            # v3,w3 = robot3.collision_free_command(ax)

            # v4,w4 = robot4.collision_free_command(ax)
        robot1.move(v1,w1)
        # if i%(robot1.Δt//robot1.dt) == 0:
        #     v1,w1 = robot1.collision_free_command(ax)
            

        #     # v2,w2 = robot2.collision_free_command(ax)

        #     # v3,w3 = robot3.collision_free_command(ax)

        #     # v4,w4 = robot4.collision_free_command(ax)
        #     robot1.move(v1,w1)
        #     # robot2.move(v2,w2)
        #     # robot3.move(v3,w3)
        #     # robot4.move(v4,w4)    
        # plt.savefig(f'captures/fig{i}.png',bbox_inches='tight',dpi=133)

        #robot1.move2(v1,w1)
        # robot2.move2(v2,w2)
        # robot3.move2(v3,w3)
        # robot4.move2(v4,w4)
    
        # plt.axis("off")
        # plt.savefig(f'captures/fig{i}.png',bbox_inches='tight',dpi=133)
        # plt.show()
        plt.pause(0.0000001)
    