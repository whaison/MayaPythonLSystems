#------------------------------------------------------------------------------
#Creates tree-like shapes made from cylinders
#Uses an L-system derived recursive function
#
#For use with 3dprint.
#
#Nobolu Ootsuka whaison
#2020/02/28
#------------------------------------------------------------------------------

from pymel.all import *
import maya.cmds as cmds
import random
#import math
from maya.OpenMaya import MVector
#import pymel.core as pm 
#Initialize
branches=""
angle=""
angleVariance=""
lengthFactor=""
lengthVariance=""
radiusFactor=""
radiusVariance=""
circleReffArr=[]
#Draws a tree using an L-system derived algorithm
#First sets the globals from user specifications
#Sets the starting length and radius
#Calls the recursive function to build the branches
def drawTree(bran, ang, angleVar, lengthFac, lengthVar, radiusFac, radiusVar):
	global branches
	global angle
	global angleVariance
	global lengthFactor
	global lengthVariance
	global radiusFactor
	global radiusVariance
	branches = bran
	angle = ang
	angleVariance = angleVar
	lengthFactor = lengthFac/100.0
	lengthVariance = lengthVar/100.0
	radiusFactor = radiusFac/100.0
	radiusVariance = radiusVar/100.0
	
	startingLength = 8
	#startingRadius = 1
	startingRadius = 4
	circle( nr=(0, 1,0), c=(0, 0, 0), r=startingRadius)
	shape = cmds.ls(sl=True)[0]
	circleReffArr.append(shape)
	drawBranch(0, 0, 0, 0, 0, 1, 0, startingRadius, startingLength,shape,False)
	#cmds.delete("pSphere1")
	for c in circleReffArr:
		cmds.delete(c)

#Recursive function for creating branches. 
#Creates a circle with radius
#Extrudes circle out
#Calculates new attributes based on user input plus random logic
def drawBranch(iteration, cX, cY, cZ, nrX, nrY, nrZ, radius, length,old_circle,ShereBool):
	if(iteration < branches):
		iteration = iteration + 1
		print("iteration= "+str(iteration))
		#Draw circle and extrude based on parameters
		R=radius*math.fabs(math.sin(iteration))
		R=radius+iteration-math.fabs(iteration)
		R=10-iteration
		circle( nr=(nrX, nrY, nrZ), c=(cX, cY, cZ), r=radius)
		shape = cmds.ls(sl=True)[0]
		circleReffArr.append(shape)
		cmds.select( clear=True )
		cmds.select( old_circle, add=True )
		cmds.select( shape, add=True )
		cmds.loft( c=0, ch=1, d=3, ss=1, rsn=True, ar=1, u=1, rn=0, po=0)
		extrudedSurface = cmds.ls(sl=True)[0]
		print("nrX= "+str(nrX)+" nrY= "+str(nrY)+" nrZ= "+str(nrZ))
		if(0==True):
			cmds.polySphere(createUVs=2, sy=20, ch=1, sx=20, r=radius*10)
			SpherePoly = cmds.ls(sl=True)[0]
			cmds.move( cX, cY, cZ, SpherePoly, absolute=True )
		#extrudedSurface=extrude (shape, et=0, d= (nrX, nrY, nrZ), l= length)
		#extrudedSurface=extrude (shape, extrudeType=0, d= (nrX, nrY, nrZ), l= length,polygon=1)
		#extrudedSurface=extrude (shape, extrudeType=0, d= (nrX, nrY, nrZ), l= length)
		
		cmds.nurbsToPoly(extrudedSurface, uss=1, ch=1, ft=0.01, d=0.1, pt=0, f=0, mrt=0, mel=0.001, ntr=0, vn=3, pc=1000, chr=0.9, un=3, vt=1, ut=1, ucr=0, cht=0.01, mnd=1, es=0, uch=0)
		delete(extrudedSurface)
		#print("extrudedSurface= "+str(extrudedSurface))
		extrudedPoly = cmds.ls(sl=True)[0]
		print("extrudedPoly= "+str(extrudedPoly))
		cmds.polyCloseBorder(extrudedPoly, ch=1)# Close Holl
		hollface = cmds.ls(sl=True)[0]
		print("hollface= "+str(hollface))
		cmds.polyTriangulate(hollface, ch=1)
		cmds.select(extrudedPoly)
		#cmds.polyClean(extrudedPoly)
		#cmds.eval('polyCleanupArgList 4 { "0","1","1","1","1","1","1","1","0","1e-05","0","1e-05","0","1e-05","0","1","1","0" };')
		#Delete the base circle, keep the cylinder
		#delete(shape)
		
		#Define direction vector and normalize
		vector = MVector(nrX, nrY, nrZ)
		vector.normalize()
		
		cX = cX + (length*vector.x)
		cY = cY + (length*vector.y)
		cZ = cZ + (length*vector.z)
		
		randX = random.randint(0, 1)*2 -1
		randY = random.randint(0, 1)*2 -1
		randZ = random.randint(0, 1)*2 -1
		
		#Random direction vector
		#For X, Y, Z, ( -1 or 1 )*angle + (randint from -angleVariance to +angleVariance)
		nrX = nrX + ((angle*randX) + random.randint(0, angleVariance*2) - angleVariance)/100.0
		nrY = nrY + ((angle*randY) + random.randint(0, angleVariance*2) - angleVariance)/100.0
		nrZ = nrZ + ((angle*randZ) + random.randint(0, angleVariance*2) - angleVariance)/100.0
		
		#Length and Radius based on factor + (randint from -variance to +variance)
		length = length * (lengthFactor + (random.randint(0, lengthVariance*2*100)/100.0) - lengthVariance)
		radius = radius * (radiusFactor + (random.randint(0, radiusVariance*2*100)/100.0) - radiusVariance)
		
		#Draw first branch
		drawBranch(iteration, cX, cY, cZ, nrX, nrY, nrZ, radius, length,shape,False)
		#drawBranch(iteration, cX, cY, cZ, 0, 1, 0, radius, length,shape,False)
		#--------------------
		#Use opposite base angle from previous branch
		nrX = nrX + ((angle*randX*-1) + random.randint(0, angleVariance*2) - angleVariance)/100.0
		nrY = nrY + ((angle*randY*-1) + random.randint(0, angleVariance*2) - angleVariance)/100.0
		nrZ = nrZ + ((angle*randZ*-1) + random.randint(0, angleVariance*2) - angleVariance)/100.0

		length = length * (lengthFactor + (random.randint(0, lengthVariance*2*100)/100.0) - lengthVariance)
		radius = radius * (radiusFactor + (random.randint(0, radiusVariance*2*100)/100.0) - radiusVariance)
		
		#Draw second branch
		drawBranch(iteration, cX, cY, cZ, nrX, nrY, nrZ, radius, length,shape,True)
	    


""" Create simple Maya interface window. """
myWindow = cmds.window(title="Parameters", wh=(180,400))
cmds.columnLayout()

cmds.text(label="Number of branches (2-15): ")
branchesText= cmds.intField( minValue=2, value=9, maxValue=15 )

cmds.text(label="Branch Base Angle (0-90): ")
angleText= cmds.intField( minValue=0, value=2, maxValue=90 )

cmds.text(label="Angle Variance (0-50)")
angleVarianceText= cmds.intField( minValue=0, value=35, maxValue=50 )

cmds.text(label="Length Factor Percent (0-200): ")
lengthFactorText= cmds.intField( minValue=0, value=95, maxValue=200 )

cmds.text(label="Length Variance Percent (0-100): ")
lengthVarianceText= cmds.intField( minValue=0, value=15, maxValue=100 )

cmds.text(label="Radius Wide Percent (0-200): ")
radiusFactorText= cmds.intField( minValue=0, value=82, maxValue=200 )

cmds.text(label="Radius Variance Percent (0-100): ")
radiusVarianceText= cmds.intField( minValue=0, value=2, maxValue=100 )

commandString = ("drawTree(cmds.intField(branchesText, query=True, value=True),"
		"cmds.intField(angleText, query=True, value=True),"
		"cmds.intField(angleVarianceText, query=True, value=True),"
		"cmds.intField(lengthFactorText, query=True, value=True),"
		"cmds.intField(lengthVarianceText, query=True, value=True),"
		"cmds.intField(radiusFactorText, query=True, value=True),"
		"cmds.intField(radiusVarianceText, query=True, value=True))")
waitCommand = 'cmds.evalDeferred('+commandString+')'
def DrawInit():
	#--------------------
    #cmds.file(new=1, f=1)
    #--------------------
	cmds.eval(waitCommand)
cmds.button(label="Draw", command=commandString)
#cmds.button(label="Draw", command=waitCommand)
#cmds.button(label="Draw", command="DrawInit()")
cmds.showWindow(myWindow)

#--------------------
cmds.file(new=1, f=1)
#--------------------
