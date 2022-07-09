# import the module
import ctypes
from telnetlib import IAC
import _ctypes
import numpy as np
from matplotlib.patches import Arc as Arc_patch
import matplotlib.pyplot as plt
from matplotlib import collections  as mc
import time


# compiling instructions
# g++ -c -fPIC Interval.cpp -o Interval.o -std=c++11 -lmpfr -lgmp -lCGAL
# g++ -shared -Wl,-soname,libInterval.so -o libInterval.so Interval.o -std=c++11 -lmpfr -lgmp -lCGAL

# load the library
IA = ctypes.cdll.LoadLibrary('./libInterval.so')

class interval_struct(ctypes.Structure):
    _fields_ = [('radius1', ctypes.c_double),
                ('radius2', ctypes.c_double),
                ('theta1', ctypes.c_double),
                ('theta2', ctypes.c_double),
                ('origin1', ctypes.c_double),
                ('origin2', ctypes.c_double)]

IA.interval_analysis.argtypes = [interval_struct,interval_struct]
IA.interval_analysis.restype = ctypes.c_void_p
IA.Interval_new.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]

def normalize(theta):
    return np.arctan2(np.sin(theta), np.cos(theta))

class Interval:
    """Interval in the local frame"""

    def __init__(self,r1,r2,t1,t2,pt):
        t = t2 - t1
        t1 = normalize(t1)
        t2 = t1 + t
        self.obj = IA.Interval_new(r1,r2,t1,t2,pt[0],pt[1])
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

    def __repr__(self):
        return f"Interval({self.radius1},{self.radius2},{self.theta1},{self.theta2},{self.origin})"    

    def from_struct(self,IS):
        return Interval(IS.radius1,IS.radius2,IS.theta1,IS.theta2,np.array([IS.origin1,IS.origin2]))

    def interval_analysis(self,I2):
        interval_analysis = IA.interval_analysis
        if self.theta2>np.pi:
            I1 = self
            II1 = I1.rotate_interval((self.theta2+self.theta1)/2,self.origin)
            II2 = I1.transform_interval(I2,(self.theta2+self.theta1)/2)
            
            result = interval_struct.from_address(interval_analysis(II1.IS,II2.IS))
            J = self.from_struct(result)
            J = J.rotate_interval(-(self.theta2+self.theta1)/2,origin=self.origin)


        else:    
            
            result = interval_struct.from_address(interval_analysis(self.IS,I2.IS))
            J = self.from_struct(result)

        
        return J 

    def transform_interval(self,I,theta):
        R = np.array([[np.cos(theta),np.sin(theta)],[-np.sin(theta),np.cos(theta)]])
        new_origin = np.matmul(R,(I.origin-self.origin).T).T + self.origin
        return Interval(I.radius1,I.radius2,I.theta1-theta,I.theta2-theta,new_origin)    

    def rotate_interval(self,theta,origin) :
        return Interval(self.radius1,self.radius2,self.theta1-theta,self.theta2-theta,origin)  

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
    
            


if __name__ == "__main__":

    # Tests
    I2 = Interval(1,2,2,3.5,np.array([5+3,5+2]))
    I1 = Interval(1,2,0.5,1.7,np.array([5+0,5+0]))

    # I2 = Interval(1,2,3,4.5,np.array([2,3]))
    # I1 = Interval(1,2,0.5,1.7,np.array([0,0]))

    # I2 = Interval(1,2,2,3.5,np.array([1,0]))
    # I1 = Interval(1,2,0.5,1.7,np.array([0,0]))

    # I2 = Interval(1,2,-0.5,1.5,np.array([3.5,7]))
    # I1 = Interval(1,2,1.57+2*np.pi,3.5+2*np.pi,np.array([7,7]))

    # I2 = Interval(9,0.0+1e-6,1e-6,1e-6,np.array([-1.5,1.5]))
    # I1 = Interval(1,2,0.5,2.5,np.array([0,0]))


    # I2 = Interval(1e-6,2,np.pi/2-1e-6,np.pi/2,np.array([19,18]))
    # I1 = Interval(1,2,0.5,1.7,np.array([18,18]))

    # I2 = Interval(0.2,1.3,1,3.5,np.array([22,20]))
    # I1 = Interval(0,3,0.5,1.7,np.array([20,20]))

    # I2 = Interval(0,9,0,1.57,np.array([30,-4]))
    # I1 = Interval(1,4,-1.5,0.5,np.array([0,0]))
     
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
    II1 = I1.rotate_interval((I1.theta2+I1.theta1)/2,I1.origin)

    II2 = II1.transform_interval(I2,(I1.theta2+I1.theta1)/2)
    t_t = time.time()
    JJ = II1.interval_analysis(II2)
    print(JJ)
    #print(II2)
    print(f"Python: {t_t-s_t} C++: {time.time()-t_t}")

    II1.draw(ax1,'blue')
    II2.draw(ax1,'red')
    JJ.draw(ax1,'green')
    plt.axis('equal')
    plt.grid()
    plt.show()