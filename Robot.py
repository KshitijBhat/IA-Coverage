import numpy as np
import matplotlib.pyplot as plt
from Interval import *
import cv2
import json

class Robot:
    radius = 15
    bot_color = 'b'
    color = 'blue'
    Δt = 1
    dt = 0.01
    obstacles = None
    max_v = 30
    max_w = 1.5
    num_samples = 64

    
    def __init__(self,x_bot,y_bot,yaw,v,w):
        
        self.x_bot = x_bot
        self.y_bot = y_bot
        self.yaw = yaw
        self.v = v
        self.w = w
        self.fellows = []

    def __repr__(self):
        return f"Robot at {self.x_bot},{self.y_bot},{self.yaw}"

    @property
    def interval(self):
        theta1 = self.yaw - (self.max_w/2)*self.Δt
        theta2 = self.yaw + (self.max_w/2)*self.Δt
        origin = np.array([self.x_bot,self.y_bot])
        r = (self.max_v)*self.Δt
        return Interval(0,r,theta1,theta2,origin)

    @property
    def interval_hull(self):
        r =  2
        theta1 = self.yaw - (self.max_w/2)*self.Δt*1.2
        theta2 = self.yaw + (self.max_w/2)*self.Δt*1.2
        origin = np.array([self.x_bot+self.radius*r*(np.cos(theta1)+np.cos(theta2))/(1e-6 + np.sin(theta1-theta2)),
                       self.y_bot+self.radius*r*(np.sin(theta1)+np.sin(theta2))/(1e-6 + np.sin(theta1-theta2))])

        n = self.radius*r/np.sin(1e-6+(theta2-theta1)/2)
        nu1 = n - self.radius*r
        nu2 = n + self.radius*r + (self.max_v)*self.Δt
        return Interval(nu1,nu2,theta1,theta2,origin)
    
    def collision_free_command(self,ax=None):
        v = self.max_v*np.ones(self.num_samples)
        w = np.array([(2*i*self.max_w/(self.num_samples-1)-self.max_w) for i in range(self.num_samples)])
        for other_robot in self.fellows:

            J = self.interval.interval_analysis(other_robot.interval_hull)
            # if not J.radius2==0:
            if ax is not None:
                J.draw(ax,"green")
            # changes w's in J

            w1 = (J.theta1-self.yaw)/self.Δt
            w2 = (J.theta2-self.yaw)/self.Δt
            vj = (J.radius1/self.Δt)
            for i in range(self.num_samples):
                if w[i]>= 2*w1 and w[i]<= 2*w2:
                    v[i] = min(v[i],vj)

        # for obstacle in self.obstacles:
        #     print(obstacle)
        #     print(self.interval)
        #     J = self.interval.interval_analysis(obstacle)
        #     if not J.radius2 == 0:
        #         if ax is not None:
        #             J.draw(ax,"green")
        #         # changes w's in J
        #         w1 = (J.theta1-self.yaw)/self.Δt
        #         w2 = (J.theta2-self.yaw)/self.Δt
        #         vj = J.radius1/self.Δt
        #         for i in range(self.num_samples):
        #             if w[i]>=2*w1 and w[i]<=2*w2:
        #                 v[i] = min(v[i],vj) 
        # for i in range(self.num_samples):                           
        #     wa = w[i]*np.ones(int(self.Δt//self.dt))
        #     yaw = self.yaw + np.cumsum(wa) * self.dt
        #     x = self.x_bot + np.cumsum(v[i] * np.cos(yaw)) * self.dt
        #     y = self.y_bot + np.cumsum(v[i] * np.sin(yaw)) * self.dt
        #     if ax is not None:
        #         ax.plot(x,y)
        return np.random.choice(v),np.random.choice(w)    

    # def choose_command(v,w):
    #     return np.random.choice(v),np.random.choice(w)    

    def move(self,v,w,ax=None):
        w = w*np.ones(int(self.Δt//self.dt))
        yaw = self.yaw + np.cumsum(w) * self.dt
        x = self.x_bot + np.cumsum(v * np.cos(yaw)) * self.dt
        y = self.y_bot + np.cumsum(v * np.sin(yaw)) * self.dt
        
        if (x[-1]<=500 and x[-1]>=20 and y[-1]<=500 and y[-1]>=20):
            self.yaw = yaw[-1]
            self.x_bot = x[-1]
            self.y_bot = y[-1]
        else:
            self.yaw = yaw[-1]

        return x,y,yaw
        
    def draw(self,ax):
        bot_circle = plt.Circle( (self.x_bot, self.y_bot),self.radius,color=self.bot_color)
        arrow = ax.arrow(self.x_bot,self.y_bot,self.radius*np.cos(self.yaw),self.radius*np.sin(self.yaw))
        ax.add_patch(bot_circle)
        ax.add_patch(arrow)
        
    
    @classmethod
    def set_environment(cls,obstacles):
        cls.obstacles = obstacles


if __name__ == "__main__":
    # # robot = Robot(4,4,0,100,1)
    # robot = Robot(4,4,3.14,100,1)
    # # obstacle = Interval(0,40,1,2.5,[50,-40])
    # obstacle = Interval(0,40,-1,1,[-40,40])
    # v = robot.max_v*np.ones(robot.num_samples)
    # w = np.array([(2*i*robot.max_w/(robot.num_samples-1)-robot.max_w) for i in range(robot.num_samples)])
    # fig,ax = plt.subplots(figsize=(8,8))
    # ax. set_aspect('equal')
    # # robot.draw(ax)
    # robot.interval.draw(ax,color='b')
    # obstacle.draw(ax,'red')
    # J = robot.interval.interval_analysis(obstacle)
    # J.draw(ax,"green")
    # # changes w's in J
    # w1 = (J.theta1-0)/robot.Δt
    # w2 = (J.theta2-0)/robot.Δt
    # vj = J.radius1/robot.Δt
    # for i in range(robot.num_samples):
    #     if w[i]>=2*w1 and w[i]<=2*w2:
    #         v[i] = min(v[i],vj)

    # for i in range(robot.num_samples):
    #     x,y,yaw = robot.move(v[i],w[i])
    #     plt.plot(x,y)
    # plt.show()


    # with open('obstacles copy.json') as f:   
    #     data = json.load(f)
    # obstacles = []
    # for obstacle in data['obstacles']:
    #     params,center = obstacle['params'],obstacle['center']
    #     obstacles.append(Interval(*params,center))
    # arena = cv2.imread("arena1.png")
    # arena = (1-cv2.cvtColor(arena,cv2.COLOR_RGB2GRAY)/255).astype('int')
    #robot = Robot(680,600,0,80,0,1.57,0)
    #robot = Robot(800,800,0.5,100,0,1,0)
    # robot = Robot(400,500,0,80,1)
    #robot = Robot(600,900,3.14,80,0,1,0)
    #robot = Robot(900,800,4.2,100,0,1,0)
    #robot = Robot(800,770,4.5,80,0,1,0)

    robot1 = Robot(200,200,-np.pi/2,35,1.13)
    robot2 = Robot(100,200, 0,35,1.13)
    robot3 = Robot(250,200, 0.5,35,1.13)
    robot4 = Robot(200,250, np.pi/2,35,1.13)

    robot1.fellows = [robot2,robot3,robot4]
    robot2.fellows = [robot1,robot3,robot4]
    robot3.fellows = [robot1,robot2,robot4]
    robot4.fellows = [robot1,robot2,robot3]
    # robot.set_environment(obstacles)
    
    fig,ax = plt.subplots(figsize=(8,8))
    
    for i in range(500):
        plt.cla()
   
        ax. set_aspect('equal')
        ax.set_xlim([0, 524])
        ax.set_ylim([0, 524])
        # ax.imshow(arena,cmap = plt.cm.gray_r,origin = 'lower')
        # for obstacle in obstacles:
        #     obstacle.draw(ax,'red')
        robot1.draw(ax)
        robot1.interval_hull.draw(ax,'blue')
        robot1.interval.draw(ax,'blue')
        robot2.draw(ax)
        robot2.interval_hull.draw(ax,'red')
        robot2.interval.draw(ax,'red')
        robot3.draw(ax)
        robot3.interval_hull.draw(ax,'magenta')
        robot3.interval.draw(ax,'magenta')
        robot4.draw(ax)
        robot4.interval_hull.draw(ax,'black')
        robot4.interval.draw(ax,'black')
        

        v1,w1 = robot1.collision_free_command(ax)
        

        v2,w2 = robot2.collision_free_command(ax)

        v3,w3 = robot3.collision_free_command(ax)

        v4,w4 = robot4.collision_free_command(ax)

        robot1.move(v1,w1)
        robot2.move(v2,w2)
        robot3.move(v3,w3)
        robot4.move(v4,w4)
        
        plt.axis("off")
        plt.savefig(f'captures/fig{i}.png',bbox_inches='tight',dpi=133)

        plt.pause(0.0001)
    
    
    