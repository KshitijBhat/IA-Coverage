import matplotlib.pyplot as plt
from Interval import *
import numpy as np
import matplotlib.pyplot as plt
from Interval import Interval
import cv2
import json
from Robot import Robot

def main():
    # robot = Robot(4,4,0,100,1)
    robot = Robot(4,4,3.14,100,1)
    # obstacle = Interval(0,40,1,2.5,[50,-40])
    # obstacle = Interval(0,40,-1,1,[-40,40])
    robot1 = Robot(-70,-40,0,30,1)
    robot1.bot_color = 'red'
    v = robot.max_v*np.ones(robot.num_samples)
    w = np.array([(2*i*robot.max_w/(robot.num_samples-1)-robot.max_w) for i in range(robot.num_samples)])
    fig,ax = plt.subplots(figsize=(8,8))
    ax. set_aspect('equal')
    # robot.draw(ax)
    # robot.draw(ax)
    robot.interval_hull.draw(ax,color='b')
    robot.interval.draw(ax,color='b')

    # robot1.draw(ax)
    robot1.interval.draw(ax,color='r')
    robot1.interval_hull.draw(ax,color='r')
    # obstacle.draw(ax,'red')
    J = robot.interval_hull.interval_analysis(robot1.interval)
    J.draw(ax,"green")
    #changes w's in J

   
    # w1 = (J.theta1-robot.yaw)/robot.Δt
    # w2 = (J.theta2-robot.yaw)/robot.Δt

    w1 = (J.theta1+robot.yaw)/robot.Δt
    w2 = (J.theta2+robot.yaw)/robot.Δt

    # print("robot yaw ", robot.yaw)
    # print(w1, " w ", w2)
    # print("Ws ", w)
    # #vj = J.radius1/robot.Δt
    # print(J.radius1)
    # print(robot.interval_hull.radius1, " ", robot.interval_hull.radius2)
    # print((robot.interval_hull.radius2-robot.interval_hull.radius1-4*robot.radius)/robot.Δt)
    # print((J.radius1-robot.interval_hull.radius1-4*robot.radius)/robot.Δt)
    # print(robot.interval.radius1, " ", robot.interval.radius2)
    vj = (J.radius1-robot.interval_hull.radius1-2*robot.r*robot.radius)/robot.Δt
    print("vj = ",vj)
    for i in range(robot.num_samples):
        if w[i]>=2*w1 and w[i]<=2*w2:
            v[i] = min(v[i],vj)

    for i in range(robot.num_samples):
        x,y,yaw = robot.move(v[i],w[i])
        print(f"velocity: {v[i]}")
        print(f"coordinates: ({x},{y})")
        plt.scatter(x,y,color='blue')
        

    
    plt.show()

def main2():
    # robot = Robot(4,4,0,100,1)
    robot = Robot(4,4,3.14,100,1)
    # obstacle = Interval(0,40,1,2.5,[50,-40])
    # obstacle = Interval(0,40,-1,1,[-40,40])
    robot1 = Robot(-70,-40,0,30,1)
    robot1.bot_color = 'red'
    v = robot.max_v*np.ones(robot.num_samples)
    w = np.array([(2*i*robot.max_w/(robot.num_samples-1)-robot.max_w) for i in range(robot.num_samples)])
    fig,ax = plt.subplots(figsize=(8,8))
    ax. set_aspect('equal')
    # robot.draw(ax)
    # robot.draw(ax)
    robot.interval_hull.draw(ax,color='b')
    robot.interval.draw(ax,color='b')

    # robot1.draw(ax)
    robot1.interval.draw(ax,color='r')
    robot1.interval_hull.draw(ax,color='r')
    # obstacle.draw(ax,'red')
    J = robot.interval.interval_analysis(robot1.interval_hull)
    J.draw(ax,"green")
    #changes w's in J

   
    # w1 = (J.theta1-robot.yaw)/robot.Δt
    # w2 = (J.theta2-robot.yaw)/robot.Δt

    w1 = (J.theta1-robot.yaw)/robot.Δt
    w2 = (J.theta2-robot.yaw)/robot.Δt

    # print("robot yaw ", robot.yaw)
    # print(w1, " w ", w2)
    # print("Ws ", w)
    # #vj = J.radius1/robot.Δt
    # print(J.radius1)
    # print(robot.interval_hull.radius1, " ", robot.interval_hull.radius2)
    # print((robot.interval_hull.radius2-robot.interval_hull.radius1-4*robot.radius)/robot.Δt)
    # print((J.radius1-robot.interval_hull.radius1-4*robot.radius)/robot.Δt)
    # print(robot.interval.radius1, " ", robot.interval.radius2)
    # vj = (J.radius1-robot.interval_hull.radius1-2*robot.r*robot.radius)/robot.Δt

    vj = J.radius1/robot.Δt
    print("vj = ",vj)
    for i in range(robot.num_samples):
        if w[i]>=2*w1 and w[i]<=2*w2:
            v[i] = min(v[i],vj)

    for i in range(robot.num_samples):
        x,y,yaw = robot.move(v[i],w[i])
        print(f"velocity: {v[i]}")
        print(f"coordinates: ({x},{y})")
        plt.scatter(x,y,color='blue')
        

    
    plt.show()

if __name__ == "__main__":
    
    main()

    # with open('obstacles copy.json') as f:   
    #     data = json.load(f)
    # obstacles = []
    # for obstacle in data['obstacles']:
    #     params,center = obstacle['params'],obstacle['center']
    #     obstacles.append(Interval(*params,center))
    # arena = cv2.imread("arena1.png")
    # arena = (1-cv2.cvtColor(arena,cv2.COLOR_RGB2GRAY)/255).astype('int')
    # robot = Robot(680,600,0,80,0,1.57,0)
    # robot = Robot(800,800,0.5,100,0,1,0)
    # robot = Robot(400,500,0,80,1)
    # robot = Robot(600,900,3.14,80,0,1,0)
    # robot = Robot(900,800,4.2,100,0,1,0)
    # robot = Robot(800,770,4.5,80,0,1,0)


    # robot1 = Robot(200,200,-np.pi/2,35,1.13)
    # robot2 = Robot(100,200, 0,35,1.13)
    # robot3 = Robot(250,200, 0.5,35,1.13)
    # robot4 = Robot(200,250, np.pi/2,35,1.13)

    # robot1.fellows = [robot2,robot3,robot4]
    # robot2.fellows = [robot1,robot3,robot4]
    # robot3.fellows = [robot1,robot2,robot4]
    # robot4.fellows = [robot1,robot2,robot3]
    # # robot1.set_environment(obstacles)
    
    # fig,ax = plt.subplots(figsize=(8,8))

    # for i in range(5000):
    #     plt.cla()

    #     ax. set_aspect('equal')
    #     ax.set_xlim([0, 524])
    #     ax.set_ylim([0, 524])
    #     # ax.imshow(arena,cmap = plt.cm.gray_r,origin = 'lower')
    #     # for obstacle in obstacles:
    #     #     obstacle.draw(ax,'red')
    #     robot1.draw(ax)
    #     robot1.interval_hull.draw(ax,'blue')
    #     robot1.interval.draw(ax,'blue')
    #     robot2.draw(ax)
    #     robot2.interval_hull.draw(ax,'red')
    #     robot2.interval.draw(ax,'red')
    #     robot3.draw(ax)
    #     robot3.interval_hull.draw(ax,'magenta')
    #     robot3.interval.draw(ax,'magenta')
    #     robot4.draw(ax)
    #     robot4.interval_hull.draw(ax,'black')
    #     robot4.interval.draw(ax,'black')
        
    #     if i%(robot1.Δt//robot1.dt) == 0:
    #         v1,w1 = robot1.collision_free_command(ax)
            

    #         v2,w2 = robot2.collision_free_command(ax)

    #         v3,w3 = robot3.collision_free_command(ax)

    #         v4,w4 = robot4.collision_free_command(ax)
    #         # robot1.move(v1,w1)
    #         # robot2.move(v2,w2)
    #         # robot3.move(v3,w3)
    #         # robot4.move(v4,w4)    
    #         # plt.savefig(f'captures/fig{i}.png',bbox_inches='tight',dpi=133)

    #     robot1.move2(v1,w1)
    #     robot2.move2(v2,w2)
    #     robot3.move2(v3,w3)
    #     robot4.move2(v4,w4)
    
    #     # plt.axis("off")
    #     # plt.savefig(f'captures/fig{i}.png',bbox_inches='tight',dpi=133)
    #     # plt.show()
    #     plt.pause(0.100000001)
    