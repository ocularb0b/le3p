# le3p-v0.1.3 mBed.py 

# le3p - A larger envelope, t-slot extrusion based, H-Gantry 3D printer.
#
# Copyright (c) 2013 Scott Maher scott.a.maher@gmail.com
#
# This file is part of le3p

# le3p is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# le3p is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with le3p.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
import sys
import FreeCAD, Part, math
from FreeCAD import Vector

from include.parts import BoxExtrusion

from config import basicConfig
from config import displayConfig
from config import advancedConfig

bc = basicConfig.basicConfig()
dc = displayConfig.displayConfig()
ac = advancedConfig.advancedConfig()

def Kapton():
  t = Part.makeBox(ac.envelopeX+ac.hotEndDia+ac.hotEndSpacing,ac.envelopeY,0.1)
	t.translate(Vector(-(ac.envelopeX+ac.hotEndDia+ac.hotEndSpacing)/2,-ac.envelopeY/2,0)) 
	t.translate(Vector(0,0,ac.mZpos))
	return t 

def GlassPlate():
	p = Part.makeBox(bc.bedSizeX,bc.bedSizeY,bc.glassPlateThick)
	p.translate(Vector(-bc.bedSizeX/2,-bc.bedSizeY/2,-bc.glassPlateThick)) 
	p = p.makeFillet(ac.minthick*2,[p.Edges[0],p.Edges[2],p.Edges[4],p.Edges[6]])
	p.translate(Vector(0,0,ac.mZpos))
	return p 

def HeatPlate():
	p = Part.makeBox(bc.bedSizeX,bc.bedSizeY+20,bc.heatPlateThick)
	p.translate(Vector(-bc.bedSizeX/2,-bc.bedSizeY/2-10,-bc.glassPlateThick - bc.heatPlateThick)) 
	p = p.makeFillet(ac.minthick,[p.Edges[0],p.Edges[2],p.Edges[4],p.Edges[6]])
	p.translate(Vector(0,0,ac.mZpos))
	return p 
	
def BasePlate():
	p = Part.makeBox(bc.bedSizeX,bc.bedSizeY+20,bc.basePlateThick)
	p.translate(Vector(-bc.bedSizeX/2,-bc.bedSizeY/2-10,-bc.glassPlateThick - bc.heatPlateThick -bc.heaterOffset - bc.basePlateThick)) 
	p = p.makeFillet(ac.minthick/2,[p.Edges[0],p.Edges[2],p.Edges[4],p.Edges[6]])
	p.translate(Vector(0,0,ac.mZpos))
	return p 

def BedFrame():
	size = ac.bedXBeamLen
	bf = BoxExtrusion(size=ac.beamSize,length=size)
	bf.translate(Vector(-size/2,-ac.zrodspacing/4,-bc.glassPlateThick - bc.heatPlateThick -bc.heaterOffset - bc.basePlateThick - ac.beamSize/2))
	bf = bf.fuse(bf.mirror(Vector(0,0,0),Vector(0,1,0)))
	bf.translate(Vector(0,0,ac.mZpos))
	return bf




