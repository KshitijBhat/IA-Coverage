import numpy as np
import matplotlib.pyplot as plt
from Interval import *

np.random.seed(5)

class Robot:
    radius = 20
    bot_color = 'b'
    color = 'blue'
    Δt = 1
    dt = 0.1
    obstacles = []
    max_v = 30
    max_w = 1.47
    num_samples = 65
    r = 1.5 # Scaling factor

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
        r = self.r
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
        collide1 = False
        v = self.max_v*np.ones(self.num_samples)
        w = np.array([(2*i*self.max_w/(self.num_samples-1)-self.max_w) for i in range(self.num_samples)])

        for other_robot in self.fellows:
            J = self.interval_hull.interval_analysis(other_robot.interval)
            if ax is not None:
                J.draw(ax,"green")

            w1 = (J.theta1+self.yaw)/self.Δt
            w2 = (J.theta2+self.yaw)/self.Δt
            r = self.r
            vj = (J.radius1-self.interval_hull.radius1-2*r*self.radius)/self.Δt

            if not J.radius1==0.0:
                collide1 = True

            for i in range(self.num_samples):
                if w[i]>= 2*w1 and w[i]<= 2*w2:
                    v[i] = max(min(v[i],vj),0)
        
        for obstacle in self.obstacles:
            J = self.interval_hull.interval_analysis(obstacle)
            if ax is not None:
                J.draw(ax,"green")

            w1 = (J.theta1-self.yaw)/self.Δt
            w2 = (J.theta2-self.yaw)/self.Δt
            r = self.r
            vj = (J.radius1-self.interval_hull.radius1-2*r*self.radius)/self.Δt
            
            if not J.radius1==0.0:
                collide = True
                if ax is not None:
                    obstacle.draw(ax, "magenta")

            for i in range(self.num_samples):
                if w[i]>= 2*w1 and w[i]<= 2*w2:
                    v[i] = max(min(v[i],vj),0)

        # if collide and not collide1:
        #     print("Collision")
        #     if np.sum(v[:len(v)//2])>np.sum(v[len(v)//2:]):
        #         vex,wex = v[0],w[0]
        #     else:
        #         vex,wex = v[-1],w[-1]
        #     return vex,wex 
        # if collide1:
        #     if np.sum(v[:len(v)//2])>np.sum(v[len(v)//2:]):
        #         vex,wex = v[0],w[0]
        #     else:
        #         vex,wex = v[-1],w[-1]
        #     return vex,wex
        if collide:
            rand_choice = np.random.choice(range(self.num_samples))
            vex,wex = v[rand_choice],w[rand_choice]
            return vex,wex 
        print("No collision")    
        return self.max_v,w[len(v)//2]   

    def collision_free_command2(self,ax=None):
        collide_robot = False
        collide_obstacle = False
        v = self.max_v*np.ones(self.num_samples)
        w = np.array([(2*i*self.max_w/(self.num_samples-1)-self.max_w) for i in range(self.num_samples)])

        for other_robot in self.fellows:
            J = self.interval.interval_analysis(other_robot.interval_hull)
            if ax is not None:
                J.draw(ax,"green")

            w1 = (J.theta1-self.yaw)/self.Δt
            w2 = (J.theta2-self.yaw)/self.Δt
            r = self.r
            vj = J.radius1/self.Δt #(J.radius1-self.interval_hull.radius1-2*r*self.radius)/self.Δt

            if not J.radius1==0.0:
                collide_robot = True

            for i in range(self.num_samples):
                if w[i]>= 2*w1 and w[i]<= 2*w2:
                    v[i] = max(min(v[i],vj),0)
        
        for obstacle in self.obstacles:
            J = self.interval_hull.interval_analysis(obstacle)
            if ax is not None:
                J.draw(ax,"green")

            w1 = (J.theta1-self.yaw)/self.Δt
            w2 = (J.theta2-self.yaw)/self.Δt
            r = self.r
            vj = (J.radius1-self.interval_hull.radius1-2*r*self.radius)/self.Δt
            
            if not J.radius1==0.0:
                collide_obstacle = True
                if ax is not None:
                    obstacle.draw(ax, "magenta")

            for i in range(self.num_samples):
                if w[i]>= 2*w1 and w[i]<= 2*w2:
                    v[i] = max(min(v[i],vj),0)

        # if collide and not collide1:
        #     print("Collision")
        #     if np.sum(v[:len(v)//2])>np.sum(v[len(v)//2:]):
        #         vex,wex = v[0],w[0]
        #     else:
        #         vex,wex = v[-1],w[-1]
        #     return vex,wex 
        # if collide1:
        #     if np.sum(v[:len(v)//2])>np.sum(v[len(v)//2:]):
        #         vex,wex = v[0],w[0]
        #     else:
        #         vex,wex = v[-1],w[-1]
        #     return vex,wex
        if collide_robot:
            rand_choice = np.random.choice(range(self.num_samples))
            vex,wex = v[rand_choice],w[rand_choice]
            return vex,wex   
        if collide_obstacle:
            if np.sum(v[:len(v)//2])>np.sum(v[len(v)//2:]):
                vex,wex = v[0],w[0]
            else:
                vex,wex = v[-1],w[-1]
            return vex,wex        

        print("No collision")    
        return self.max_v,w[len(v)//2]   



    def move(self,v,w,ax=None):
        """Moves by Δt"""
        w = w*np.ones(int(self.Δt//self.dt))
        yaw = self.yaw + np.cumsum(w) * self.dt
        x = self.x_bot + np.cumsum(v * np.cos(yaw)) * self.dt
        y = self.y_bot + np.cumsum(v * np.sin(yaw)) * self.dt
        
        self.yaw = yaw[-1]
        self.x_bot = x[-1]
        self.y_bot = y[-1]
        #return x[-1],y[-1],yaw[-1]
        
    def move2(self,v,w,ax=None):
        """Moves only by dt"""
        yaw = self.yaw + w * self.dt
        x = self.x_bot + v * np.cos(yaw) * self.dt
        y = self.y_bot + v * np.sin(yaw) * self.dt
        
        self.yaw = yaw
        self.x_bot = x
        self.y_bot = y

    def draw(self,ax):
        bot_circle = plt.Circle( (self.x_bot, self.y_bot),self.radius,color=self.bot_color)
        arrow = ax.arrow(self.x_bot,self.y_bot,self.radius*np.cos(self.yaw),self.radius*np.sin(self.yaw))
        ax.add_patch(bot_circle)
        ax.add_patch(arrow)
        
    @classmethod
    def set_environment(cls,obstacles):
        cls.obstacles = obstacles



    
        