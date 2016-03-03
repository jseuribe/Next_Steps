########################################
##
## Makefile
## LINUX compilation 
##
##############################################

#FLAGS
C++FLAG = -g -std=c++0x -Wall

#Math Library
MATH_LIBS = -lm
EXEC_DIR=.

#Rule for .cpp files
# .SUFFIXES : .cpp.o 

.cpp.o:
	g++ $(C++FLAG) $(INCLUDES)  -c $< -o $@

#Including
INCLUDES=  -I. 
LIBS_ALL =  -L/usr/lib -L/usr/local/lib $(MATH_LIBS) 

#ZEROTH PROGRAM
PROGRAM_0=main
ALL_OBJ0=$(PROGRAM_0).o
$(PROGRAM_0): $(ALL_OBJ0)
	g++ $(C++FLAG) -o $(EXEC_DIR)/$@ $(ALL_OBJ0) $(INCLUDES) $(LIBS_ALL)

#Compiling all
all: 	
		make $(PROGRAM_0)

#Clean obj files
clean:
	(rm -f *.o;)

(:
