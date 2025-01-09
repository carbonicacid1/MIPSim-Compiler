# MIPSim-Compiler
This tool was made by a student of Slovak University of Technology, Faculty of Informatics
and Information Technologies to help students in Principles of Computer Engineering.
It was specifically made to compile code for MIPSim overlay v31 and outputs files with ".mp" extension
which stores instruction data.

The compiler isn't perfect and doesn't handle all edge cases. Some will mistakes be ignored,
however certain instructions like "LI $1,$1,1002", will be processed incorrectly if it has
the same format as instructions like "ADDI $1,$1,1002" in which case the "LI $1,$1,1002"
will get processed the same way (This is incorrect, but ignored by MIPSIM, correct instruction
would be "LI $1,1002").

Labels aren't supported! You need to add them yourself or calculate the jumps as shown in example2.txt

Comments are allowed by putting '#' at the end of the instruction as shown in example2.txt too.

Empty spaces between instructions/functions should be filled with NOPs.

Download the release version at https://github.com/carbonicacid1/MIPSim-Compiler/releases

Or compile the program yourself using pyinstaller

pyinstaller compile.py --onefile

here's a video tutorial: https://www.youtube.com/watch?v=bqNvkAfTvIc
