# le3p-v0.1.3 Part Sizes

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

class partSizes:
  
	#Nuts and Bolts
	# Tolerances for nuts and bolts is done here
	# [dia,headdia,headthick]
	m2c = [2.1,4.1,2]
	m3l = [3.1, 6.1, 2.2] #m3 lowhead cap
	m3c = [3.1,6.1,3.2] #m3 std cap
	m3i = [4.1,6] #m3 threaded insert
	m4l = [4.1, 8.1, 3.2]  #m4 lowhead cap
	m8b = [8.1,12.25,5.2] #m8 bolt
	
	m3n = [3,5.55,2] #M3 Nut
	m5n = [5,8,3.8]
	m8n = [8,12.25,5.2]  #M8 Nut
	m8tn = [8,12.25,3.2] #M8 Thin Nut
	
	m10n = [10,17.25,9]  #M10 Nut
	m10tn = [10,17.25,5] #M10 Thin Nut
	
	#All Bearings And Bushings are [id, od, len]
	#RadialBearings
	z608 = [8,22,7]
	z624 = [4,13,5]
	z623 = [3,10,4]
	z688 = [8,16,5]
	z689 = [9,17,5]
	z6700 = [10,15,4]
	z6800 = [10,19,5]
	z6000 = [10,26,8]
	
	#LinearBearings
	lm10uu = [10,19,22]
	lm10luu = [10,19,55]
	
	igusMSM101650 = [10,16,50]
	
	printed = [10,19,55]

	#Nema Stepper Motors
	#[size,length,shaftdia,shaftlen,boltspacing,facedia,screwdia]
	nema17x48 = [42,48,5,25,31,26,3]
	nema17x42 = [42,42,5,25,31,26,3]
	nema17x35 = [42,35,5,25,31,26,3]
