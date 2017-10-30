# LTspice2Kicad
   # LTspice to Kicad schematic conversion

   Written by Laurent CHARRIER   
   Last update : 30 Oct. 2017   
   Based on : Python on Windows OS
   
Here are some python scripts to transfer symbols and schematics from LTspice to Kicad.
The goal under that script is to design and simulate under LTspice and to automatically transfer the circuit under Kicad to draw the PCB.
For that, you need to have Python installed and in your path under windows only because LTspice is only under Windows.
Note that I use and tested the script with Python 3.6 , LTspiceXVII and Kicad 4.0.7  (for other versions, some minor script(s) changes may be needed)

The method is based on those 2 steps in the directory that contains the LTspice symbols (*.asy) and schematic (*.asc) :  
 1)  run :  LTspice2Kicad.bat  
 2)  run :  python sch_Ltspice2Kicad.py your_schematic.asc

The first step 1. is based on the python script lib_LTspice2Kicad.py and creates many libraries based LTspice symbols library, and also creates a library with all the symbols of the current directory.   
The second step 2. transfers the schematic from LTspice to Kicad and creates 2 files : your_schematic.pro and your_schematic.sch
  
  
  
The current limitations, and so, <B>the to-do list</B> is :
- the hierarchical schematics are not transferred, so <B>only single sheet schematic</B> are properly converted
- the position of the name and value of the component is arbitrary fixed and do not follow the position of LTspice
- the schematics and symbols saved in UTF-16-LE format cannot be converted without script customization, except ADA4807 and ADA4895 symbols
