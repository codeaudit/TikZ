# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 23:56:41 2014
@author: Edward
"""
import numpy as np
from numpy.core.umath_tests import inner1d
from utilities import showImage


blurKernelSize = 7


def blurredDistance(a,b, show = False):
    import cv2
    kernelSize = blurKernelSize
    
    a = cv2.GaussianBlur(a,(kernelSize,kernelSize),sigmaX = 0)
    b = cv2.GaussianBlur(b,(kernelSize,kernelSize),sigmaX = 0)
    
    if show:
        showImage(a)
        showImage(b)
    return -np.sum(np.abs(a - b))



def asymmetricBlurredDistance(a,b, show = False):
    # a = target
    # b = current
    # if you see a pixel in current that isn't in target, that's really bad
    # if you see a pixel and target that isn't an current, that's not so bad
    import cv2
    kernelSize = blurKernelSize

    # threshold the images
    a = np.copy(a*2)
    a[a > 0.35] = 1.0
    a[a <= 0.35] = 0.0
#    showImage(a)

    b = np.copy(b)
    b[b > 0.5] = 1.0
    b[b <= 0.5] = 0.0
#    showImage(b)
    
    a = cv2.GaussianBlur(a,(kernelSize,kernelSize),sigmaX = 0)
    b = cv2.GaussianBlur(b,(kernelSize,kernelSize),sigmaX = 0)
    
    if show:
        showImage(a)
        showImage(b)

    d = a - b
    positives = d > 0
    targetBigger = np.sum(np.abs(d[d > 0]))
    currentBigger = np.sum(np.abs(d[d < 0]))
    return currentBigger*2 + targetBigger

def analyzeAsymmetric(a,b):
    # a = target
    # b = current
    # if you see a pixel in current that isn't in target, that's really bad
    # if you see a pixel and target that isn't an current, that's not so bad
    import cv2
    kernelSize = blurKernelSize

   
    a = cv2.GaussianBlur(a,(kernelSize,kernelSize),sigmaX = 0)
    b = cv2.GaussianBlur(b,(kernelSize,kernelSize),sigmaX = 0)

    showImage(a + b)
    
    d = a - b
    targetBigger = np.sum(d[d > 0]*d[d > 0])
    currentBigger = np.sum(d[d < 0]*d[d < 0])
    print "targetBigger = %f"%targetBigger
    print "currentBigger = %f"%currentBigger

#    showImage(b)

    return currentBigger*2 + targetBigger


# Hausdorff Distance
def HausdorffDist(A,B):
    # Hausdorf Distance: Compute the Hausdorff distance between two point
    # clouds.
    # Let A and B be subsets of metric space (Z,dZ),
    # The Hausdorff distance between A and B, denoted by dH(A,B),
    # is defined by:
    # dH(A,B) = max(h(A,B),h(B,A)),
    # where h(A,B) = max(min(d(a,b))
    # and d(a,b) is a L2 norm
    # dist_H = hausdorff(A,B)
    # A: First point sets (MxN, with M observations in N dimension)
    # B: Second point sets (MxN, with M observations in N dimension)
    # ** A and B may have different number of rows, but must have the same
    # number of columns.
    #
    # Edward DongBo Cui; Stanford University; 06/17/2014

    # Find pairwise distance
    D_mat = np.sqrt(inner1d(A,A)[np.newaxis].T + inner1d(B,B)-2*(np.dot(A,B.T)))
    # Find DH
    dH = np.max(np.array([np.max(np.min(D_mat,axis=0)),np.max(np.min(D_mat,axis=1))]))
    return(dH)

def ModHausdorffDist(A,B):
    #This function computes the Modified Hausdorff Distance (MHD) which is
    #proven to function better than the directed HD as per Dubuisson et al.
    #in the following work:
    #
    #M. P. Dubuisson and A. K. Jain. A Modified Hausdorff distance for object
    #matching. In ICPR94, pages A:566-568, Jerusalem, Israel, 1994.
    #http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=576361
    #
    #The function computed the forward and reverse distances and outputs the
    #maximum/minimum of both.
    #Optionally, the function can return forward and reverse distance.
    #
    #Format for calling function:
    #
    #[MHD,FHD,RHD] = ModHausdorffDist(A,B);
    #
    #where
    #MHD = Modified Hausdorff Distance.
    #FHD = Forward Hausdorff Distance: minimum distance from all points of B
    #      to a point in A, averaged for all A
    #RHD = Reverse Hausdorff Distance: minimum distance from all points of A
    #      to a point in B, averaged for all B
    #A -> Point set 1, [row as observations, and col as dimensions]
    #B -> Point set 2, [row as observations, and col as dimensions]
    #
    #No. of samples of each point set may be different but the dimension of
    #the points must be the same.
    #
    #Edward DongBo Cui Stanford University; 06/17/2014

    # Find pairwise distance
    D_mat = np.sqrt(inner1d(A,A)[np.newaxis].T + inner1d(B,B)-2*(np.dot(A,B.T)))
    # Calculating the forward HD: mean(min(each col))
    FHD = np.mean(np.min(D_mat,axis=1))
    # Calculating the reverse HD: mean(min(each row))
    RHD = np.mean(np.min(D_mat,axis=0))
    # Calculating mhd
    MHD = np.max(np.array([FHD, RHD]))
    return(MHD, FHD, RHD)
