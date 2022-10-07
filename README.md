# Multi-Robot Coverage with Interval Analysis-based Obstacle Avoidance

Supervised by: Vivek Yogi and [Leena Vachhani](https://www.sc.iitb.ac.in/~leena/), [Systems and Control Group](https://www.sc.iitb.ac.in/), IIT Bombay.

## Abstract
The goal of a Coverage Path Planning (CPP) Problem is to find an optimal path which covers an Area Of Interest (AOI) while ensuring collision avoidance with obstacles in the area. The use of multiple agents for this task leads to increase in robustness and scalability of the coverage. This work studies the multi-agent coverage problem for an enclosed environment with numerous static obstacles. Interval Analysis (IA) is used for the parallel collision avoidance between the agents as well as with the obstacles within the dynamic environment. This technique would enable the use of hardware and sensor-efficient low-end robots with only local sensing capabilities. Random Walks (RW) would lead to the decentralized solution without the use of localization and mapping.We compare the results of systematic coverage with the random walk coverage with IA-based Collision Avoidance.

## Installation

Install the required libraries:

```
pip install numpy
pip install matplotlib
pip install opencv-python
```

Install the CGAL library by 
```
sudo apt-get install libcgal-dev
```

Clone the reposity by 
```
git clone https://github.com/KshitijBhat/IA-coverage
```

## Compiling

To compile the ``Interval.cpp`` file into a shared library run the following:

```
g++ -c -fPIC Interval.cpp -o Interval.o -std=c++14 -lmpfr -lgmp -lCGAL
g++ -shared -Wl,-soname,libInterval.so -o libInterval.so Interval.o -std=c++14 -lmpfr -lgmp
```


## References
1. Vyas, P., Vachhani, L. & Sridharan, K. Interval Analysis Technique for Versatile and Parallel Multi-Agent Collision Detection and Avoidance. J Intell Robot Syst 98, 705–720 (2020). https://doi.org/10.1007/s10846-019-01091-1
2. Pranjal Vyas, Leena Vachhani, K Sridharan, Hardware-efficient interval analysis based collision detection and avoidance for mobile robots, Mechatronics, Volume 62, 2019, 102258, ISSN 0957-4158, https://doi.org/10.1016/j.mechatronics.2019.102258
