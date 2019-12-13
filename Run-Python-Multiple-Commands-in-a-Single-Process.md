### For Windows 10 and Python 3.7.5 :

#### Examples of Windows multiple commands, ran sequentially within the same process, and launched by a Python script :

*List of the commands we are going to use*

 \- echo something : echo "ok" (note that on Windows, && is the separator between the commands)
 
 \- Run several distinct lines of Python code (pay attention to double double quotes) within a single command : python -c "ggl = 10**100; text = ""Googol (Ten duotrigintillion) :""; print(text + "" \t %s"" % (ggl)); print(""Scientific notation (dirty method) :"" + "" \t "" + str(ggl/1))"
 
 \- Change directory : cd C:\\Users\\PathToMyPythonScript
 
 \- List content of that directory : dir
 
 \- Launch an external Python script who is in that directory, with parameters, using the local path of the directory : python myPythonScript.py value1ofParam1 value2ofParam2


```python
# =============================================================================
# Example of external script file myPythonScript.py you can use for a try.
# This script just outputs the arguments you've passed to it
import sys
print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
# =============================================================================
```

### With subprocess.check_output :
_Note_ that with the check_output function, or the call function, your program is temporarily blocked and will wait the call to the function to be finished before continuing it's run.

```python
output = subprocess.check_output('echo "ok" && python -c "ggl = 10**100; text = ""Googol (Ten duotrigintillion) :""; print(text + "" \t %s"" % (ggl)); print(""Scientific notation (dirty method) :"" + "" \t "" + str(ggl/1))" && cd C:\\Users\\PathToMyPythonScript && dir && python myPythonScript.py value1ofParam1 value2ofParam2', universal_newlines=True, shell=True)
print(output)
```

If shell=True, Windows will launch cmd.exe, the command prompt (it looks up the COMSPEC environment variable but defaults to cmd.exe if not present), but for instance on POSIX, it's the SHELL environment variable that will specify which binary to invoke as the "shell". The disadvantages of that are security reasons (shell injection) and it also makes the calls more platform dependant.

On another hand, the subprocess (check_output, Popen etc...) expects a list of strings for non-shell calls and a string for shell calls.

So without shell=True, the syntax will be a bit different, let's rewrite acording to this:

```python
output = subprocess.check_output(["C:\Windows\System32\cmd.exe", "/k", "echo", '"ok"', "&&", "python", "-c", "ggl = 10**100; text = 'Googol (Ten duotrigintillion) :'; print(text + ' \t %s' % (ggl)); print('Scientific notation (dirty method) :' + ' \t ' + str(ggl/1))", "&&", "cd", "C:\\Users\\PathToMyPythonScript", "&&", "dir", "&&", "python", "myPythonScript.py", "value1ofParam1", "value2ofParam2"], universal_newlines=True)
print(output)
print('\r\n') #Just to leave some space
```

Observe that now, we specify that we want to use "cmd" at the beginning.

Observe also that now you are in your Python environment, displayed at the end of the output, (my_env) C:\Users\PathToMyPythonScript> 

For Windows, the arg sequence will be converted to a string, according to these [specifications](http://lagrange.univ-lyon1.fr/docs/python/2.7.13/library/subprocess.html#converting-argument-sequence) :

The /k is a windows cmd shell command switch that allow to Run Command and then return to the CMD prompt.

C:\Windows\System32\cmd.exe can usually be replaced by cmd.exe or just cmd.


### With subprocess.Popen :
_Note_ that using Popen, your program is NOT blocked and will not wait the end of the call to Popen to move forward. Moreover, for that one we'll add a couple of additional details

```python
result = subprocess.Popen('echo "ok" && python -c "ggl = 10**100; text = ""Googol (Ten duotrigintillion) :""; print(text + "" \t %s"" % (ggl)); print(""Scientific notation (dirty method) :"" + "" \t "" + str(ggl/1))" && cd C:\\Users\\PathToMyPythonScript && dir && python myPythonScript.py value1ofParam1 value2ofParam2',
                          shell=True, universal_newlines=True, #universal_newlines makes result display more friendly
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print("Process ID of the child process: \t\t\t\t %d" % (result.pid)) #If shell=True, it's the process ID of the spawned shell.
print("Return code of the process (subprocess) before it ends : \t ", result.returncode)

print("\r\n", "# Now visualize the output of our commands", "\r\n")

try:
    output, error = result.communicate(timeout=15) #Note1 : Popen.communicate() returns a tuple (stdout_data, stderr_data)
                                                   #--------------------------------------------------
                                                   #Note2 : Popen.communicate()) will also set the returncode attribute value.
                                                   #On the former lines, returncode attribute value is None, 
                                                   #which means that the process is not terminated.
                                                   #On the last line, the returncode attribute value is 0,  
                                                   #which means that it ran successfully
                                                   #--------------------------------------------------
                                                   #Note3 : Use communicate() rather than stdin.write(), stdout.read()
                                                   #or stderr.read() to avoid deadlocks due to any of the other
                                                   #OS pipe buffers filling up and blocking the child process.
except subprocess.TimeoutExpired:
    result.kill()
    output, error = result.communicate()

print (output)
print(error)    #Empty if no errors raised

print("Return code of the process (subprocess) after it ends : \t ", result.returncode)
```
