# import the module
import ctypes

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
  
    # constructor
    def __init__(self,r1,r2,t1,t2,pt):
  
        # attribute
        lib.Interval_new.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
        self.obj = lib.Interval_new(r1,r2,t1,t2,pt[0],pt[1])
  
    # define method
    def interval_analysis(self,I2):
        lib.interval_analysis(self.obj,I2.obj)

    
            




# create a Geek class object
I2 = Interval(1,2,2,3.5,(3,2))
I1 = Interval(1,2,0.5,1.7,(0,0))

# object method calling
I1.interval_analysis(I2)

