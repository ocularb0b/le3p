#le3p-v0.1.3 Shapes functions

# Le3p - A larger envelope t-slot extrusion based H-Gantry 3D printer.
#
# Copyright (c) 2013 Scott Maher scott.a.maher@gmail.com
#
# This file is part of Le3p

# Le3p is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Le3p is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Le3p.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
import sys

import FreeCAD, Part, math
from FreeCAD import Base
from FreeCAD import Vector
from math import pi, cos, sin

def regPolygon(sides, radius=0, type="inner", edgeLength=0, \
  X_offset=0, Y_offset=0, Z_offset=0, \
	vX=0,vY=0,vZ=0, \
	rotation=0, extrude=0, makeFace= 1):
	
	if sides < 3:
		raise ValueError("Sides must be >=3")
	if radius == 0 and edgeLength == 0:
		raise ValueError("Either radius or edgeLength must be assigined a non-zero value")
	
	r = {'inner': 0, 'outer': 0}
	i = 'innner' ## Allows shorthand r[i] instead of r["inner"]
	o = 'outer'  ## Bad form, but useful
		
	if type == "inner":
		r[i] = radius 
		r[o] = radius / cos(pi/sides)
		radius = r[o]	
	elif type == "edgeLength":
		radius = (edgeLength / (2*sin(pi/sides)))
		r[o] = radius
		r[i] = (edgeLength / (2*tan(pi/sides)))
	else:
		r[i] = cos(pi/sides) * radius 
		r[o] = radius
	
	# Define the starting point for our calculations
	# regardless of the final orientation, we will start working in the X & Y
	x = radius
	y = 0
	z = Z_offset
	
	# Set initial point if rotation was specified and save it for the end point	
	startx = round((x*cos((0))) - (y*sin((0))), 4)
	starty = round((x*sin((0))) + (y*cos((0))), 4)
	
	x = startx
	y = starty	
	
	# create the points list and define the first point, off set in X,Y, and Z as needed
	points = [(Base.Vector(x + X_offset,y  + Y_offset, z))]
	
	# Calculate the remaining points	
	# These calculations assume the circle is centered at 0,0, so 
	# the offset is applied after the calculations are applied
	for step in range (1, sides):
		# http://en.wikipedia.org/wiki/Cartesian_coordinate_system#Rotation
		newx = round((x*cos((2*pi/sides))) - (y*sin((2*pi/sides))), 4)
		newy = round((x*sin((2*pi/sides))) + (y*cos((2*pi/sides))), 4)
		x = newx
		y = newy	
		points.append((Base.Vector(x + X_offset,y  + Y_offset,z)))
	
	points.append((startx + X_offset, starty + Y_offset,z))
	polygon = Part.makePolygon(points)
	
	if makeFace != 0:
		polygon = Part.Face(polygon)

	if extrude != 0:
		polygon = polygon.extrude(Base.Vector(0,0,extrude))
	
	#polygon.rotate(vX, vY, vZ)

	return polygon
	
def BeltCorner(id=1,od=2,w=2,a=90):
	bc = Part.makeCylinder(od/2,w)
	idc = Part.makeCylinder(id/2,w)
	bc=bc.cut(idc)
	
	ct = Part.makeBox(od,od,w)
	ct.translate(Vector(-od/2,-od,0))
	bc=bc.cut(ct)
	if a == 90:
		ct.rotate(Vector(0,0,0),Vector(0,0,1),-90)
		bc=bc.cut(ct)
	
	return bc
	
	
def TSlot(topthick=2.5,topwide = 5.5,inthick=2.5,indeep=1.65,length=10):
	top=Part.makeBox(topwide,topthick,length)
	top.translate(Vector(-topwide/2,indeep,0))
	tee=Part.makeBox(inthick,indeep,length)
	tee.translate(Vector(-inthick/2,0,0))
	
	ts = top.fuse(tee)
	return ts

def RodClampSlice(size = 20,wide = 10,thick = 2, rad = 4):
	bb = Part.makeBox(size,wide,size)
	bb = bb.makeFillet(rad,[bb.Edges[3]])
	bc = Part.makeBox(size,wide,size)
	if rad-thick > 0:
		bc = bc.makeFillet(rad-thick,[bc.Edges[3]])
	bc.translate(Vector(thick,0,thick))
	rcs = bb.cut(bc)
	#rcs = rcs.makeFillet(thick/2-0.01,[rcs.Edges[2],rcs.Edges[14],rcs.Edges[20],rcs.Edges[21]])
	return rcs
	
def ThinSlice(size=20,wide = 10, thick = 2):
	ts = Part.makeBox(size,wide,thick)
	ts = ts.makeFillet(thick/2-0.01,[ts.Edges[1],ts.Edges[3],ts.Edges[5],ts.Edges[7]])
	return ts
	
def USlice(wide=20,tall=20,deep=20,thick=2,rad=4):
	bb = Part.makeBox(wide,deep,tall)
	bb = bb.makeFillet(rad,[bb.Edges[8],bb.Edges[9]])
	bc = Part.makeBox(wide,deep-thick,tall-thick*2)
	bc = bc.makeFillet(rad,[bc.Edges[8],bc.Edges[9]])
	bc.translate(Vector(0,thick,thick))
	us=bb.cut(bc)
	return us
	

def FilletFlange(innerdia = 10,filletdia = 5,filletthick=10):
	ff = Part.makeCylinder(innerdia/2 + filletdia/2,filletthick)
	fi = Part.makeCylinder(innerdia/2,filletthick+filletdia)
	fi.translate(Vector(0,0,-filletdia/2))
	ff=ff.fuse(fi)
	ff=ff.fuse(ff.makeFillet(filletdia/2-0.01,[ff.Edges[3],ff.Edges[5]]))
	return ff

def LE3Plogolong(size=20,deep=10):
	L = Part.makeBox(size*0.5,deep,size)
	lc = Part.makeBox(size*0.8,deep,size)
	lc.translate(Vector(size/4,0,size/4))
	L = L.cut(lc)
	E = Part.makeBox(size*0.5,deep,size)
	ec1 = Part.makeBox(size*0.8,deep,size/5)
	ec1.translate(Vector(size/4,0,size/4))
	ec2 = Part.makeBox(size*0.8,deep,size/5)
	ec2.translate(Vector(size/4,0,size - size/4 - size/5))
	E = E.cut(ec1.fuse(ec2))
	E.translate(Vector(size*0.6,0,0))
	Three = E.mirror(Vector(size*1.15,0,0),Vector(1,0,0))
	P = Part.makeBox(size*0.5,deep,size)
	pc1 = Part.makeBox(size*0.8,deep,size)
	pc1.translate(Vector(size/4,0,-size*0.75))
	pc2 = Part.makeBox(size*0.2,deep,size*0.3)
	pc2.translate(Vector(size*0.15,0,size*0.5))
	P = P.cut(pc1.fuse(pc2))
	P.translate(Vector(size*1.8,0,0))
	LE3P=L.fuse(E.fuse(Three.fuse(P)))
	return LE3P

	
