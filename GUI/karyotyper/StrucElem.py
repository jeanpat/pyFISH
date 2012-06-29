# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 14:56:20 2011

@author: Jean-Patrick Pommier
"""

import numpy as np

'''
The different structuring elements to detect branched-points
o:no pixel
x:a pixel
*: a pixel or no pixel

*x* x*x x*x x*x *x* x** *** **x *x* x*x
xxx *x* *x* *x* xx* *x* xxx *x* *xx *x*
*** x*x x** x** *x* x*x *x* x*x *x* **x
'''

branch1=np.array([[2, 1, 2], [1, 1, 1], [2, 2, 2]])
branch2=np.array([[1, 2, 1], [2, 1, 2], [1, 2, 1]])
branch3=np.array([[1, 2, 1], [2, 1, 2], [1, 2, 2]])
branch4=np.array([[2, 1, 2], [1, 1, 2], [2, 1, 2]])
branch5=np.array([[1, 2, 2], [2, 1, 2], [1, 2, 1]])
branch6=np.array([[2, 2, 2], [1, 1, 1], [2, 1, 2]])
branch7=np.array([[2, 2, 1], [2, 1, 2], [1, 2, 1]])
branch8=np.array([[2, 1, 2], [2, 1, 1], [2, 1, 2]])
branch9=np.array([[1, 2, 1], [2, 1, 2], [2, 2, 1]])
'''
The different structuring elements to detect end-points
o:no pixel
x:a pixel
*: a pixel or no pixel
ooo  ooo oo* o*x *x* x*o *oo ooo
oxo  ox* oxx ox* oxo *xo xxo *xo
*x*  o*x oo* ooo ooo ooo *oo x*o
'''
endpoint1=np.array([[0, 0, 0], 
                    [0, 1, 0], 
                    [2, 1, 2]])
                    
endpoint2=np.array([[0, 0, 0], 
                    [0, 1, 2], 
                    [0, 2, 1]])
                    
endpoint3=np.array([[0, 0, 2], 
                    [0, 1, 1], 
                    [0, 0, 2]])
                    
endpoint4=np.array([[0, 2, 1], 
                    [0, 1, 2], 
                    [0, 0, 0]])
                    
endpoint5=np.array([[2, 1, 2], 
                    [0, 1, 0], 
                    [0, 0, 0]])
                    
endpoint6=np.array([[1, 2, 0], 
                    [2, 1, 0], 
                    [0, 0, 0]])
                    
endpoint7=np.array([[2, 0, 0], 
                    [1, 1, 0], 
                    [2, 0, 0]])
                    
endpoint8=np.array([[0, 0, 0], 
                    [2, 1, 0], 
                    [1, 2, 0]])

'''

'''
cornerS=np.array([[2, 2, 2],
                   [2, 0 ,2],
                   [1, 1, 1]])
                   
cornerSE=np.array([[2, 2, 2],
                   [2, 0 ,1],
                   [2, 1, 1]])
                   
cornerE=np.array([[2,2,1],
                   [2,0,1],
                   [2,2,1]])

cornerNE=np.array([[2,1,1],
                   [2,0,1],
                   [2,2,2]])
                   
cornerN=np.array([[1,1,1],
                   [2,0,2],
                   [2,2,2]])
                   
cornerNW=np.array([[1,1,2],
                   [1,0,2],
                   [2,2,2]])

cornerW=np.array([[1,2,2],
                   [1,0,2],
                   [1,2,2]])              

cornerSW=np.array([[2,2,2],
                   [1,0,2],
                   [1,1,2]]) 
'''
corner se
*** *xx xx* ***
*ox *ox xo* xo*
*xx *** *** xx*
'''
pureSE=np.array([[0, 0, 2],
                   [0, 0 ,1],
                   [2, 1, 1]]) 
                   
pureNE=np.array([[2,1,1],
                   [0,0,1],
                   [0,0,2]]) 
                   
pureNW=np.array([[1,1,2],
                   [1,0,0],
                   [2,0,0]])
                   
pureSW=np.array([[2,0,0],
                   [1,0,0],
                   [1,1,2]]) 