import numpy as np
import matplotlib.pyplot as plt
from Interval import *

np.random.seed(3)

class Robot:
    radius = 15
    bot_color = 'b'
    color = 'blue'
    Δt = 1
    dt = 0.1
    obstacles = []
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
        r = 2
        theta1 = self.yaw - (self.max_w/2)*self.Δt
        theta2 = self.yaw + (self.max_w/2)*self.Δt
        origin = np.array([self.x_bot+r*self.radius*(np.cos(theta1)+np.cos(theta2))/(1e-6 + np.sin(theta1-theta2)),
                       self.y_bot+r*self.radius*(np.sin(theta1)+np.sin(theta2))/(1e-6 + np.sin(theta1-theta2))])

        n = self.radius*r/np.sin(1e-6+(theta2-theta1)/2)
        nu1 = n - self.radius*r
        nu2 = n + self.radius*r + (self.max_v)*self.Δt
        return Interval(nu1,nu2,theta1,theta2,origin)
    
    def collision_free_command(self,ax=None):
        collide = False
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
            # vj = ((J.radius2-J.radius1)-2*self.radius)/self.Δt
            for i in range(self.num_samples):
                if w[i]>= 2*w1 and w[i]<= 2*w2:
                    v[i] = min(v[i],vj)/2
                    collide = True
                    
        for obstacle in self.obstacles:

            J = self.interval.interval_analysis(obstacle)
            # if not J.radius2==0:
            if ax is not None:
                J.draw(ax,"green")
            # changes w's in J

            w1 = (J.theta1-self.yaw)/self.Δt
            w2 = (J.theta2-self.yaw)/self.Δt
            vj = (J.radius1/self.Δt)
            # vj = ((J.radius2-J.radius1)-2*self.radius)/self.Δt
            for i in range(self.num_samples):
                if w[i]>= 2*w1 and w[i]<= 2*w2:
                    v[i] = min(v[i],vj)
                    collide = True            

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
        # if collide:
        #     return v[-1],w[-1] 
        return np.random.choice(v),np.random.choice(w)    

    # def choose_command(v,w):
    #     return np.random.choice(v),np.random.choice(w)    

    def move(self,v,w,ax=None):
        """Moves by Δt"""
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


    def move2(self,v,w,ax=None):
        """Moves only by dt"""
        yaw = self.yaw + w * self.dt
        x = self.x_bot + v * np.cos(yaw) * self.dt
        y = self.y_bot + v * np.sin(yaw) * self.dt
        
        if (x<=500 and x>=20 and y<=500 and y>=20):
            self.yaw = yaw
            self.x_bot = x
            self.y_bot = y
        else:
            self.yaw = yaw

        return x,y,yaw

    def draw(self,ax):
        bot_circle = plt.Circle( (self.x_bot, self.y_bot),self.radius,color=self.bot_color)
        arrow = ax.arrow(self.x_bot,self.y_bot,self.radius*np.cos(self.yaw),self.radius*np.sin(self.yaw))
        ax.add_patch(bot_circle)
        ax.add_patch(arrow)
        
    
    @classmethod
    def set_environment(cls,obstacles):
        cls.obstacles = obstacles



    
        