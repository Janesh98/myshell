from cmd import Cmd
from threading import Thread
import os, sys, subprocess

class MyShell(Cmd):

    prompt = os.getcwd() + "$ "

    def do_hello(self, args):
        """Says hello. If you provide a name, it will greet you with it."""
        if not args:
            args = 'stranger'
        print ("Hello, %s" % args)

    def do_quit(self, args):
        """Quits the program."""
        print ("Quitting.")
        raise SystemExit

    def write_or_append(self, args):
        """decide whether the file mode should be set to write or append.
           one > character mean write, two >> means append."""
        if args.split()[-2] == ">":
            mode = "w"
        else:
            mode = "a"
        return mode

    """changed help_redirection to h_redirection as it would appear in the help command
       list and crashed the program if you typed help redirection"""
    def h_redirection(self, args):
        mode = self.write_or_append(args)
        file = args.split()[-1]
        save = self.stdout
        args = args.split()[:-2]
        args = " ".join(args)

        with open(file, mode) as f:
            self.stdout = f
            super().do_help(args)
        self.stdout = save

    def help_more(self):
        """displays the user manual 20 lines at a time on each Enter key press"""
        with open("readme.txt", "r") as f:
            count = 0
            for line in f:
                if count == 20:
                    count = 0
                    while True:#loop until enter key is pressed
                        if input() == "":
                            break
                        continue

                print(line.strip())
                count+=1

    def do_help(self, args):
        """provides helpful info about commands. Type help <topic>"""
        """overrides cmd module super function help to support redirection
        and display the user manual"""
        if self.ensure_redirection(args):
            self.h_redirection(args)
        else:
            super().do_help(args)

    def ensure_redirection(self, args):
        """ensure its output redirection and not 
        just a > or >> in an command eg. echo > >.txt"""
        try:
            return args.split()[-2] in [">", ">>"] and args.split()[-1].split(".")[-1] == "txt"
        except:
            return False

    def dir_redirection(self, args):
        output_file = args.split()[-1]
        files = os.listdir(".")
        #sort and remove hidden files
        files = [f for f in sorted(files) if f[0] != "."]

        mode = self.write_or_append(args)

        with open(output_file, mode) as f:
            """ add a new line so if appending more text after,
                it is seperated and not clumped together"""
            f.write("\n".join(files) + "\n")

    def do_dir(self, args):
        """lists the contents of the current directory."""
        if not args:
            files = os.listdir('.')
            files = sorted(files)
            for f in files:
                if f[0] != ".": # don't show hidden files
                    print(f)

        elif self.ensure_redirection(args):
            self.dir_redirection(args)

    def environ_redirection(self, args):
        file = args.split()[-1]

        mode = self.write_or_append(args)

        with open(file, mode) as f:
            f.write(str(os.environ) + "\n")

    def do_environ(self, args):
        """prints current environment"""
        if not args:
            for key in os.environ:
                # os.environ behaves like a dictionary. key[value] pair.
                print(key + "=" + os.environ[key])

        elif self.ensure_redirection(args):
                self.environ_redirection(args)

    def echo_redirection(self, args):
        mode = self.write_or_append(args)
        args = args.split()
        file = args[-1]
        s = " ".join(args[:-2])
        with open(file, mode) as f:
            f.write(s + "\n")

    def do_echo(self, args):
        """Writes arguments to standard output."""
        if ">" in args:
            # ensure it is an i/o redirection command
            if self.ensure_redirection(args):
                self.echo_redirection(args)
        else:
            print(args)

    def do_clr(self,args):
        """clears the screen"""
        subprocess.run('clear', shell=True)

    def do_cd(self, args):
        """Change the current working directory."""
        try:
            if args:
                os.chdir(args)#change directory to cd <directory>
            else:
                # if no argument is given cd to the users home directory
                os.chdir(os.path.expanduser("~"))

            self.prompt = os.getcwd() + "$ "

        # can not cd to non existent directory
        except FileNotFoundError:
            print("No such file or directory: '%s'" %args)

        # can not cd to a file
        except NotADirectoryError:
            print("Not a directory: '%s'" %args)

    def do_pause(self, args):
        """pauses until Enter key is pressed"""
        input("Press Enter to continue...")

    def do_myshell(self, file):
        """run batchfiles via command line argument"""
        try:
            #with automatically closes the file object when finished
            if not file:
                file = input("Enter batchfile with relevant file extension: ")

            threads = []

            with open(file, "r") as f:
                f = f.readlines()
                for line in f:
                    line = line.strip()
                    if len(line.split()) == 1:
                        cmd = line
                        args = ""
                    else:
                        cmd = line.split()[0]
                        args = line.split()[1:]
                        args = " ".join(args)

                    name = "do_" + cmd # create the do_cmd() string
                    myfunc = getattr(self, name)# find the function in this class

                    """each command is given its own thread to execute,
                        speeds up the process. mulitprocessing was originally used
                        but was significantly slower and sometimes froze the system,
                        also if a cd command was given within the batchfile, when the processes
                        finished, the current working directory was not updated,
                        with threading it is, as seen by the prompt after execution."""
                    t = Thread(target=myfunc, args=(args,))
                    threads.append(t)

            self.handle_processing(threads)

        except FileNotFoundError:
            print("No such file or directory: '%s'" %file)

        except AttributeError:
            print("No function called: %s" %name)

    def handle_processing(self, threads):
        #in function to be used by another function to handle threads
        for t in threads:
            # starts each thread
            t.start()

        for t in threads:
            """waits for the threads to finish, also ensures stdout is not used at the same
            time causing text to be jumbled together."""
            t.join()

    def run_program_redirection(self, args):
        #redirect program output to given file if any
        mode = self.write_or_append(args)
        args = args.split()
        file = args[0]
        output_file = args[-1]
        args = args[1:-2]

        with open(output_file, mode) as f:
            subprocess.run([sys.executable, file] + args, stdout=f)

    def run_program(self, args):
        length = len(args.split())
        args = args.split()

        subprocess.run([sys.executable] + args)

    def default(self, args):
        """overides the super function from the cmd module
           to run python files like in a normal shell"""
        try:
            """try to ensure not redirection, will be an issue if > used as arg for progam
            as it wont enter the if statement and not execute, re module pattern matching
            would be better at more accurately ensuring redirection"""
            if ">" not in args and args.split()[0][-3:] == ".py" or args[-3:] == ".py":
                self.run_program(args)
            #same as above except tries to esnure redirection
            elif args.split()[0][-3:] == ".py" and args.split()[-2] in [">", ">>"]:
                self.run_program_redirection(args)

            else:
                """calls super command as args is not a correct command to issue
                   the appropriate error message"""
                super().default(args)
        except:
            """ if an error occurs above it will skip else and jump to this so
            call super command as it is not a valid argument"""
            super().default(args)

if __name__ == '__main__':
    shell = MyShell()
    #execute a command as a command line argument when running program eg. myshell.py <args>
    if len(sys.argv) > 1:
        shell.onecmd(' '.join(sys.argv[1:]))
    else:
        """starts the main cmd loop, which repeatedly issues a prompt, accepts input
        parses input, passing remainder of the line to action methods as an argument"""
        shell.cmdloop('Starting Shell...')