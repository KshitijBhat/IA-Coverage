# import the module
import ctypes
import _ctypes
import numpy as np
from matplotlib.patches import Arc as Arc_patch
import matplotlib.pyplot as plt
from matplotlib import collections  as mc
from numpy.ctypeslib import ndpointer
import time


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

class interval_struct(ctypes.Structure):
    _fields_ = [('radius1', ctypes.c_double),
                ('radius2', ctypes.c_double),
                ('theta1', ctypes.c_double),
                ('theta2', ctypes.c_double),
                ('origin1', ctypes.c_double),
                ('origin2', ctypes.c_double)]
          

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
        self.IS = interval_struct()
        self.IS.radius1 = ctypes.c_double(r1)
        self.IS.radius2 = ctypes.c_double(r2)
        self.IS.theta1 = ctypes.c_double(t1)
        self.IS.theta2 = ctypes.c_double(t2)
        self.IS.origin1 = ctypes.c_double(pt[0])
        self.IS.origin2 = ctypes.c_double(pt[1])

    def from_struct(self,IS):
        return Interval(IS.radius1,IS.radius2,IS.theta1,IS.theta2,np.array([IS.origin1,IS.origin2]))
  
    # define method
    def interval_analysis(self,I2):
        foo = lib.interval_analysis
        foo.argtypes = [interval_struct,interval_struct]
        foo.restype = ctypes.c_void_p
        #interval_struct #ctypes.c_void_p #ctypes.POINTER(ctypes.c_double)
        # print(foo(self.IS,I2.IS).radius1)
        result = interval_struct.from_address(foo(self.IS,I2.IS))
        return self.from_struct(result)


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
# I2 = Interval(1,2,2,3.5,np.array([5+3,5+2]))
# I1 = Interval(1,2,0.5,1.7,np.array([5+0,5+0]))

# I2 = Interval(1,2,3,4.5,np.array([2,3]))
# I1 = Interval(1,2,0.5,1.7,np.array([0,0]))

# I2 = Interval(1,2,2,3.5,np.array([1,0]))
# I1 = Interval(1,2,0.5,1.7,np.array([0,0]))
I2 = Interval(1,2,-0.5,1.5,np.array([-3.5,0]))
I1 = Interval(1,2,1.57,3.15,np.array([0,0]))
# object method calling
# print("hello: ",I1.interval_analysis(I2))
st_time = time.time()
J = I1.interval_analysis(I2)
print("Time: ", time.time()-st_time)
fig= plt.figure(figsize = (16,8))
ax = fig.add_subplot(1,2,1)
I2.draw(ax,'red')
I1.draw(ax,'blue')
J.draw(ax,'green')
# I1.draw(ax,'blue')
plt.axis('equal')
plt.grid()
ax1 = fig.add_subplot(1,2,2)
# I2.draw(ax1,'red')
s_t = time.time()
II1 = I1.rotate_interval(1.5708)

II2 = I1.transform_interval(I2,1.5708)
t_t = time.time()
JJ = II1.interval_analysis(II2)
print(f"Python: {t_t-s_t} C++: {time.time()-t_t}")

II1.draw(ax1,'blue')
II2.draw(ax1,'red')
JJ.draw(ax1,'green')
plt.axis('equal')
plt.grid()
plt.show()