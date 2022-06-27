# import the module
import ctypes
import numpy as np
from matplotlib.patches import Arc as Arc_patch
import matplotlib.pyplot as plt
from matplotlib import collections  as mc
# compiling instructions
# g++ -c -fPIC Intersections.cpp -o Intersections.o -std=c++11 -lmpfr -lgmp -lCGAL
# g++ -shared -Wl,-soname,libIntersections.so -o libIntersections.so Intersections.o -std=c++11 -lmpfr -lgmp -lCGAL

# load the library
lib = ctypes.cdll.LoadLibrary('./libIntersections.so')

#lib.interval_analysis.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,
                                  #ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]  
# function calling
# lib.interval_analysis(1.00,2.00,0.500,1.700,  0.00,0.00,   
#                       1.00,2.00,2.00,3.5,     3.00,2.00)

# create a Geek class
class Interval:
    """Interval in the local frame"""
    # constructor
    def __init__(self,r1,r2,t1,t2,pt):
  
        # attribute
        lib.Interval_new.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
        self.obj = lib.Interval_new(r1,r2,t1,t2,pt[0],pt[1])
        self.radius1 = r1
        self.radius2 = r2
        self.theta1 = t1
        self.theta2 = t2
        self.origin = pt




  
    # define method
    def interval_analysis(self,I2):
        lib.interval_analysis(self.obj,I2.obj)

    def transform_interval(self,I,theta):
        R = np.array([[np.cos(theta),np.sin(theta)],[-np.sin(theta),np.cos(theta)]])
        new_origin = np.matmul(R,(I.origin-self.origin).T).T

        return Interval(I.radius1,I.radius2,I.theta1-theta,I.theta2-theta,new_origin)    

    def rotate_interval(self,theta) :
        return Interval(self.radius1,self.radius2,self.theta1-theta,self.theta2-theta,np.array([0,0]))  

    def draw(self,ax,color):
        x,y = self.origin
        theta1, theta2 = self.theta1,self.theta2
        r1, r2 = self.radius1, self.radius2
        ax.add_patch(Arc_patch((self.origin[0], self.origin[1]), 2*self.radius1,2*self.radius1, theta1=np.rad2deg(self.theta1), theta2=np.rad2deg(self.theta2), linewidth=1, color=color))
        ax.add_patch(Arc_patch((self.origin[0], self.origin[1]), 2*self.radius2,2*self.radius2, theta1=np.rad2deg(self.theta1), theta2=np.rad2deg(self.theta2), linewidth=1, color=color))
        l11, l12 = tuple((x+r1*np.cos(theta1),y+r1*np.sin(theta1))),tuple((x+r2*np.cos(theta1),y+r2*np.sin(theta1)))
        l21, l22 = tuple((x+r1*np.cos(theta2),y+r1*np.sin(theta2))),tuple((x+r2*np.cos(theta2),y+r2*np.sin(theta2)))
        lc = mc.LineCollection([[l11,l12],[l21,l22]], colors = color, linewidths=1)
        ax.add_collection(lc)
    
            




# create a Geek class object
I2 = Interval(1,2,2,3.5,np.array([5+3,5+2]))
I1 = Interval(1,2,0.5,1.7,np.array([5+0,5+0]))

# object method calling
I1.interval_analysis(I2)

fig= plt.figure(figsize = (16,8))
ax = fig.add_subplot(1,2,1)
I2.draw(ax,'red')
I1.draw(ax,'blue')

# I1.draw(ax,'blue')
plt.axis('equal')
plt.grid()
ax1 = fig.add_subplot(1,2,2)
# I2.draw(ax1,'red')
I1.rotate_interval(1.5708).draw(ax1,'blue')
I1.transform_interval(I2,1.5708).draw(ax1,'red')
plt.axis('equal')
plt.grid()
plt.show()