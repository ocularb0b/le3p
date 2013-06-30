#le3p-v0.1.3 Parts functions

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

def BoxExtrusion(size=5, length=40):
  
	blank=Part.makeBox(length, size, size)
	blank.translate(Vector(0, -size, -size))
	
	slota=Part.makeBox(length, size/6, size/3)
	slota.translate(Vector(0, -size/2 - (size/12), -size))
	cut1 = blank.cut(slota)
	
	slotb=Part.makeBox(length, size/6, size/3)
	slotb.translate(Vector(0, -size/2 - (size/12), -size/3))
	cut2 = cut1.cut(slotb)
	
	slotc=Part.makeBox(length, size/3, size/6)
	slotc.translate(Vector(0, -size/3, -size/12 -size/2))
	cut3 = cut2.cut(slotc)
		
	slotd=Part.makeBox(length, size/3, size/6)
	slotd.translate(Vector(0, -size, -size/12 -size/2))
	cut4 = cut3.cut(slotd)
	cut4.translate(Vector(0, size/2, size/2))
		
	return cut4

def CapHeadScrew(l=10,d=3,hd=6,hh=3,cut=0):
	s = Part.makeCylinder(d/2,l)
	s.translate(Vector(0,0,-l))
	if cut == 0:
		h = Part.makeCylinder(hd/2,hh)
		
	if cut == 1:
		h = Part.makeCylinder(hd/2,hh+hd+l)
		h = h.makeFillet(hd/2-0.01,[h.Edges[0]])
	
	screw=s.fuse(h)	
	return screw

def NemaMotor(motor=[]):
	bodyblank = Part.makeBox(motor[0], motor[0], motor[1])
	body = bodyblank.makeChamfer(motor[0]/12, [bodyblank.Edges[0], bodyblank.Edges[2], bodyblank.Edges[4],  bodyblank.Edges[6]])
	body.translate(Vector(-motor[0]/2, -motor[0]/2, -motor[1]))
	face = Part.makeCylinder(motor[5]/2, 2)
	shaft = Part.makeCylinder(motor[2]/2, motor[3])
	fuse1 = face.fuse(shaft)
	motor = body.fuse(fuse1)
	return motor

def TimingGear(pitchdia=25, gearwidth=12, boredia=5,hubdia = 20, hubheight = 6):
	g = Part.makeCylinder(pitchdia/2, gearwidth)
	hb = Part.makeCylinder(hubdia/2, hubheight)
	hb.translate(Vector(0, 0, -hubheight))
	f1 = g.fuse(hb)
	b = Part.makeCylinder(boredia/2, gearwidth + hubheight)
	b.translate(Vector(0, 0, -hubheight))
	c1 = f1.cut(b)
	c1.translate(Vector(0,0,-gearwidth/2))
	tg = c1
	return tg

def StraightBushing(dim=[10,20,20]):
	bo = Part.makeCylinder(dim[1]/2,dim[2])
	bi = Part.makeCylinder(dim[0]/2,dim[2])
	b = bo.cut(bi)
	return b

def Bearing(dim=[4,13,5]):
	bo = Part.makeCylinder(dim[1]/2,dim[2])
	bi = Part.makeCylinder(dim[0]/2,dim[2])
	b = bo.cut(bi)
	return b


def E3Dv4():
	blockx = 14
	blocky = 20
	blockz = 10
	fin=2.1
	findia=25
	b1t=4.7
	b2t=4.6
	b3t=3
	b4t=fin*8
	b11t=fin*6
	b16t=5
	#built top up (upside down)
	b1 = Part.makeCylinder(8,b1t)
	b2 = Part.makeCylinder(6,b1t+b2t)
	b3 = Part.makeCylinder(8,b3t)
	b3.translate(Vector(0,0,b1t+b2t))
	b4 = Part.makeCylinder(8.93/2,b4t)
	b4.translate(Vector(0,0,b1t+b2t+b3t))
	b5 = Part.makeCylinder(findia/2,fin)
	b5.translate(Vector(0,0,b1t+b2t+b3t+fin))
	b6 = Part.makeCylinder(findia/2,fin)
	b6.translate(Vector(0,0,b1t+b2t+b3t+fin*3))
	b7 = Part.makeCylinder(findia/2,fin)
	b7.translate(Vector(0,0,b1t+b2t+b3t+fin*5))
	b8 = Part.makeCylinder(findia/2,fin)
	b8.translate(Vector(0,0,b1t+b2t+b3t+fin*7))
	b9 = Part.makeCylinder(13/2,fin)
	b9.translate(Vector(0,0,b1t+b2t+b3t+fin*8))
	b10 = Part.makeCylinder(findia/2,fin)
	b10.translate(Vector(0,0,b1t+b2t+b3t+fin*9))
	b11 = Part.makeCylinder(15/2,b11t)
	b11.translate(Vector(0,0,b1t+b2t+b3t+fin*10))
	b12 = Part.makeCylinder(findia/2,fin)
	b12.translate(Vector(0,0,b1t+b2t+b3t+fin*11))
	b13 = Part.makeCylinder(findia/2,fin)
	b13.translate(Vector(0,0,b1t+b2t+b3t+fin*13))
	b14 = Part.makeCylinder(findia/2,fin)
	b14.translate(Vector(0,0,b1t+b2t+b3t+fin*15))
	b15 = Part.makeCylinder(2.8/2,fin)
	b15.translate(Vector(0,0,b1t+b2t+b3t+fin*16))
	b16 = Part.makeCylinder(3,b16t)
	b16.translate(Vector(0,0,b1t+b2t+b3t+fin*17))
	blk=Part.makeBox(blockx,blocky,blockz)
	blk.translate(Vector(-blockx/2,-blocky+blockx/2,b1t+b2t+b3t+fin*17))
	noz = Part.makeCone(6,0.5,6)
	noz.translate(Vector(0,0,b1t+b2t+b3t+fin*17+blockz))
	
	he = b1.fuse(b2.fuse(b3.fuse(b4.fuse(b5.fuse(b6.fuse(b7.fuse(b8.fuse(b9.fuse(b10.fuse(b11.fuse(b12.fuse(b13.fuse(b14.fuse(b15.fuse(b16.fuse(blk.fuse(noz)))))))))))))))))
	he.rotate(Vector(0,0,0),Vector(1,0,0),180)
	return he
	
