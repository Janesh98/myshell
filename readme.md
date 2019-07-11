# Shell Manual

##cd:

changes the current directory, if a directory name is given, eg. cd  <directory>, the current 
working directory Is changed to the given named directory. If no name is given, cd will change 
to the home directory. Note : you can acess a super directory by the command <cd ..>.

##clr:

simply clears the screens leaving it blank aside from the command prompt.

##dir:

lists the contents of the current working directory.

##environ:

lists all the environment variables line by line of the current environment sorted 
alphabetically.
An environment variable is a dynamic object containing an editable value, a key[value] pair
similar to a dictionary, they are used by programs to know where to install directory files, 
temporary files and user profile settings, they help shape the environment programs run within.

##echo:

displays a comment on the display, e.g echo <example>

##hello:

says hello, if a name is given it greets you with it, eg. hello <Donal>

##pause:

pauses operation of the shell until the Enter key is pressed

##quit:

quits the shell, ending the program

##myshell:

provides batchfile support, a batchfile is a file with a list of commands. A batchfile can be 
ran by the command myshell followed by the file with the relevant file extension eg, myshell <
batchfile.txt>.

##help:

provides a short simple explanation for all commands within the shell, if an argument is given
 eg. help <topic>, the relevant explanation is provided. If no argument Is given, all 
 documented commands are listed.
If help <more> is entered this file will be displayed in a block of twenty lines on each Enter 
key press

##program exexcution:

the shell can execute programs as in a regular shell, to run a program simply type the program 
name followed by the command line arguments if any.
e.g. ProgramName.py args
note: can aslo execute command upon executing the shell e.g. myshell.py example.py, the shell
will exit upon completion

##output redirection:

available for the following commands: help, dir, environ, echo and also program execution.
With output redirection the content that would usually appear on the screen is now written to 
a given file instead.
if the redirection character is > then the outputfile is created if it does not exist and 
overwritten by the new contents if it does. 
If the redirection token is >> then outputfile is created if it does not exist and appended to 
if it does.

##Examples:

		echo args example > output.txt
		ProgramName.py  args > output.txt
		echo args example >> output.txt
		ProgramName.py args >> output.txt
