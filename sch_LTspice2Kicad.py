#! usr/bin/python
# -*- coding: ISO-8859-1 -*-

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

#  Written by : Laurent CHARRIER
#  last change: 2017, Oct 30.
#
#  To be done : - position of the name and reference
#               - hierarchical design
#               - pins of hierarchical design
#

import sys,re,os,time

# function to find locaion of each space character in each line
def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

in_file = sys.argv[1]
indir = in_file.split("\\")
out_file = "LTspice_" + indir[len(indir)-1]

indir = os.getcwd().split("\\")
LTspice_lib = ["LTspice_"+indir[len(indir)-1],"LTspice_sym","LTspice_Comparators","LTSpice_devices","LTspice_Digital","LTspice_FilterProducts","LTspice_Misc","LTspice_Opamps","LTspice_Optos","LTspice_PowerProducts","LTspice_References","LTspice_SpecialFunctions"]
Kicad_lib = ["power","device","switches","relays","motors","transistors","conn","linear","regul","74xx","cmos4000","adc-dac","memory","xilinx","microcontrollers","dsp","microchip","analog_switches","motorola","texas","intel","audio","interface","digital-audio","philips","display","cypress","siliconi","opto","atmel","contrib","valves"]

#  .pro  export file
out_file1 = out_file.replace(".asc",".pro")
outfl = open(out_file1,"w");
outfl.write("update="+time.strftime('%d/%m/%y %H:%M',time.localtime())+"\n")
outfl.write("version=1\nlast_client=eeschema\n[general]\nversion=1\nRootSch=\nBoardNm=\n[pcbnew]\nversion=1\nLastNetListRead=\nUseCmpFile=1\nPadDrill=0.60\nPadDrillOvalY=0.60\nPadSizeH=1.50\nPadSizeV=1.50\nPcbTextSizeV=1.50\nPcbTextSizeH=1.50\nPcbTextThickness=0.30\nModuleTextSizeV=1.00\nModuleTextSizeH=1.00\nModuleTextSizeThickness=0.15\nSolderMaskClearance=0.00\nSolderMaskMinWidth=0.00\nDrawSegmentWidth=0.20\nBoardOutlineThickness=0.10\nModuleOutlineThickness=0.15\n[cvpcb]\nversion=1\nNetIExt=net\n[eeschema]\nversion=1\nLibDir=\n[eeschema/libraries]\n")
for i in range(0,len(LTspice_lib)):
	outfl.write("LibName"+str(i+1)+"="+LTspice_lib[i]+"\n")
for j in range(0,len(Kicad_lib)):
	outfl.write("LibName"+str(j+i+2)+"="+Kicad_lib[j]+"\n")
outfl.write("\n")
outfl.close()

#  .sch  export file
out_file = out_file.replace(".asc",".sch")
outfl = open(out_file,"w");
outfl.write("EESchema Schematic File Version 2\n")
for i in range(0,len(LTspice_lib)):
	outfl.write("LIBS:"+LTspice_lib[i]+"\n")
for i in range(0,len(Kicad_lib)):
	outfl.write("LIBS:"+Kicad_lib[i]+"\n")
outfl.write("EELAYER 25 0\nEELAYER END\n")

infl = open(in_file,"r");
lines = infl.readlines()
infl.close()

wireX1 = []
wireY1 = []
wireX2 = []
wireY2 = []
conn_X = []
conn_Y = []
flag_text = []
flag_X = []
flag_Y = []
text_text = []
text_X = []
text_Y = []
sym_sym = []
sym_X = []
sym_Y = []
sym_orient = []
sym_name = []
sym_value = []
sym_spice = []
sym_i = 0
sname = 0
svalue = 0
sspice = 0

lnn = 0
# read the LTspice library line by line :
for line1 in lines:
	lnn = lnn + 1
	line1 = line1.rstrip('\n')	
	line1 = line1.rstrip('\r')
	# print(line1)
	spc = list(find_all(line1," "))  # find all space locations to split the variables of the line
	
	if re.match(r"^WIRE *", line1) is not None:
		wireX1.append(int(3.125*int(line1[spc[0]:spc[1]])))
		wireY1.append(int(3.125*int(line1[spc[1]:spc[2]])))
		wireX2.append(int(3.125*int(line1[spc[2]:spc[3]])))
		wireY2.append(int(3.125*int(line1[spc[3]:])))
	
	if re.match(r"^FLAG *", line1) is not None:
		flag_text.append(line1[spc[2]+1:])
		flag_X.append(int(3.125*int(line1[spc[0]:spc[1]])))
		flag_Y.append(int(3.125*int(line1[spc[1]:spc[2]])))
	
	if re.match(r"^TEXT *", line1) is not None:
		text_text.append(line1[spc[4]+2:])
		text_X.append(int(3.125*int(line1[spc[0]:spc[1]])))
		text_Y.append(int(3.125*int(line1[spc[1]:spc[2]])))

	if re.match(r"^SYMBOL *", line1) is not None:
		if sname < sym_i :
			sym_name.append(sym_sym[sym_i-1])
			sname = sname+1
			print("add sname")
		if svalue < sym_i :
			sym_value.append(sym_sym[sym_i-1])
			svalue = svalue+1
		if sspice < sym_i :
			sym_spice.append(" ")
			sspice = sspice+1
		sym_i = sym_i + 1
		sym_sym.append(line1[spc[0]+1:spc[1]])
		sym_X.append(int(3.125*int(line1[spc[1]:spc[2]])))
		sym_Y.append(int(3.125*int(line1[spc[2]:spc[3]])))
		sym_orient.append(line1[spc[3]+1:])
	if re.match(r"^SYMATTR InstName *", line1) is not None:
		sname = sname + 1
		sym_name.append(line1[spc[1]+1:])
		print(str(lnn) + " : sym_name : "+sym_name[sname-1])
	if re.match(r"^SYMATTR Value *", line1) is not None:
		svalue = svalue + 1
		sym_value.append(line1[spc[1]+1:])
	if re.match(r"^SYMATTR SpiceLine *", line1) is not None:
		sspice = sspice + 1
		sym_spice.append(line1[spc[1]+1:])
		
if sname < sym_i :
	sym_name.append(sym_sym[sym_i-1])
	sname = sname+1
	print("add sname")
if svalue < sym_i :
	sym_value.append(sym_sym[sym_i-1])
	svalue = svalue+1
if sspice < sym_i :
	sym_spice.append(" ")
	sspice = sspice+1

# calcul of min and max of X and Y to choose the page size : A4, A3, A2 A1 or A0
X_max = max(max(sym_X),max(wireX1),max(wireX2),max(text_X))
X_min = min(min(sym_X),min(wireX1),min(wireX2),min(text_X))
Y_max = max(max(sym_Y),max(wireY1),max(wireY2),max(text_Y))
Y_min = min(min(sym_Y),min(wireY1),min(wireY2),min(text_Y))
outfl.write("$Descr A4 11693 8268\n")
offX = 50 * int((11693/2 - (X_max-X_min)/2)/50) #  grid step assumed = 50
offY = 50 * int(( (8268-1250)/2 - (Y_max-Y_min)/2)/50) #  grid step assumed = 50 & 1250 is the heigh of the cartridge
if (X_max-X_min) > 10000  or  (Y_max-Y_min) > 7500 :
	outfl.write("$Descr A3 16535 11693\n")
	offX = 50 * int((16535/2 - (X_max-X_min)/2)/50) #  grid step assumed = 50
	offY = 50 * int(((11693-1250)/2 - (Y_max-Y_min)/2)/50) #  grid step assumed = 50
if (X_max-X_min) > 15000  or  (Y_max-Y_min) > 10000 :
	outfl.write("$Descr A2 23386 16535\n")
	offX = 50 * int((23386/2 - (X_max-X_min)/2)/50) #  grid step assumed = 50
	offY = 50 * int(((16535-1250)/2 - (Y_max-Y_min)/2)/50) #  grid step assumed = 50
if (X_max-X_min) > 20000  or  (Y_max-Y_min) > 15000 :
	outfl.write("$Descr A1 33110 23386\n")
	offX = 50 * int((33110/2 - (X_max-X_min)/2)/50) #  grid step assumed = 50
	offY = 50 * int(((23386-1250)/2 - (Y_max-Y_min)/2)/50) #  grid step assumed = 50
if (X_max-X_min) > 30000  or  (Y_max-Y_min) > 20000 :
	outfl.write("$Descr A0 46811 33110\n")
	offX = 50 * int((46811/2 - (X_max-X_min)/2)/50) #  grid step assumed = 50
	offY = 50 * int(((33110-1250)/2 - (Y_max-Y_min)/2)/50) #  grid step assumed = 50
outfl.write("encoding utf-8\nSheet 1 1\nTitle \""+out_file.replace(".sch","")+"\"\nDate \""+time.strftime('%d/%m/%y %H:%M',time.localtime())+"\"\nRev \"1.0\"\nComp \"\"\nComment1 \"Converted from LTspice\"\nComment2 \"\"\nComment3 \"\"\nComment4 \"\"\n$EndDescr\n")

# export each components
for i in range(0,len(sym_sym)):
	outfl.write("$Comp\nL "+sym_sym[i]+" "+sym_name[i]+"\n")
	outfl.write("U 1 1 59E9ACCC\n")
	outfl.write("P "+str(sym_X[i]+offX)+" "+str(sym_Y[i]+offY)+"\n")
	outfl.write("F 0 \""+sym_name[i]+"\" H "+str(sym_X[i]+offX+100)+" "+str(sym_Y[i]+offY-100)+" 50  0000 L CNN\n")
	outfl.write("F 1 \""+sym_value[i]+"\" H "+str(sym_X[i]+offX+100)+" "+str(sym_Y[i]+offY-200)+" 50  0000 L CNN\n")
	outfl.write("	1    "+str(sym_X[i]+offX)+" "+str(sym_Y[i]+offY)+"\n")
	if sym_orient[i]=="R0"   : outfl.write("	 1    0    0    -1  \n")
	if sym_orient[i]=="R90"  : outfl.write("	 0    1    1     0  \n")
	if sym_orient[i]=="R180" : outfl.write("	-1    0    0     1  \n")
	if sym_orient[i]=="R270" : outfl.write("	 0   -1   -1     0  \n")
	if sym_orient[i]=="M0"   : outfl.write("	-1    0    0    -1  \n")
	if sym_orient[i]=="M90"  : outfl.write("	 0   -1    1     0  \n")
	if sym_orient[i]=="M180" : outfl.write("	 1    0    0     1  \n")
	if sym_orient[i]=="M270" : outfl.write("	 0    1   -1     0  \n")
	outfl.write("$EndComp\n")
# export each wires and calculate connections
for i in range(0,len(wireX1)):
	outfl.write("Wire Wire Line\n	"+str(wireX1[i]+offX)+" "+str(wireY1[i]+offY)+" "+str(wireX2[i]+offX)+" "+str(wireY2[i]+offY)+"\n")
# add a connection if at least 3 wires have the same end point
for i in range(0,len(wireX1)-1):
	nb_conn = 0
	conn_rgstr = 0
	for j in range(i+1,len(wireX1)):
		if ((wireX1[i]==wireX1[j] and wireY1[i]==wireY1[j]) or (wireX1[i]==wireX2[j] and wireY1[i]==wireY2[j])) :
			nb_conn = nb_conn + 1
	for j in range(0,len(conn_X)):
		if (wireX1[i]==conn_X[j] and wireY1[i]==conn_Y[j]) :
			conn_rgstr = 1
	if (nb_conn > 1  and  conn_rgstr==0):
		outfl.write("Connection ~ "+str(wireX1[i]+offX)+" "+str(wireY1[i]+offY)+"\n")
# add a connection if an end of wire is over another wire
# >> idea not needed

# export each wire annotation and pins
for i in range(0,len(flag_text)):
	if flag_text[i]=="0" :
		outfl.write("$Comp\nL GND #PWR?\nU 1 1 59E9AE0E\nP "+str(flag_X[i]+offX)+" "+str(flag_Y[i]+offY)+"\nF 0 \"#PWR?\" H "+str(flag_X[i]+offX)+" "+str(flag_Y[i]+offY-250)+" 50  0001 C CNN\nF 1 \"GND\" H "+str(flag_X[i]+offX)+" "+str(flag_Y[i]+offY-150)+" 50  0000 C CNN\n	1    "+str(flag_X[i]+offX)+" "+str(flag_Y[i]+offY)+"\n	1    0    0    -1\n$EndComp\n")
	else :
		outfl.write("Text Label "+str(flag_X[i]+offX)+" "+str(flag_Y[i]+offY)+" 0    60   ~ 0\n"+flag_text[i]+"\n")

# export each free text lines
for i in range(0,len(text_text)):
	outfl.write("Text Notes "+str(text_X[i]+offX)+" "+str(text_Y[i]+offY+120*text_text[i].count('\\n'))+" 0    60   ~ 0\n"+text_text[i]+"\n")

outfl.write("$EndSCHEMATC")
outfl.close()