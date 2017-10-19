# Intro to pdb
## or: How I Found a bug in Requests



## About Me
* Jesse Jarzynka - [jessejoe.com](http://jessejoe.com) - [github.com/jessejoe](https://github.com/jessejoe) - [j@jessejoe.com](mailto:j@jessejoe.com)

* Senior SDET [@CarbonBlack_Inc](https://twitter.com/CarbonBlack_Inc)

* Career: Tech Support --> Systems Administrator --> Storage Support Engineer --> Automation Engineer

* i.e. not a traditional programmer!



## pdb - The Python Debugger


* Ships with Python

* Always there (your IDE isn't!)

* Makes debugging *fast*

* Probably much simpler to use than you think!

* Minimal (or zero) code modification needed (`print()`, `logging.info()`, etc.)


## Invocation

From the Python interpreter:
```bash
>>> import pdb, mymodule
>>> pdb.run('mymodule.test()')
```
As a script from Python:
```bash
python -m pdb myscript.py
```
Inside a program:
```
import pdb; pdb.set_trace()
```


## Basic commands
* `h` - help
* `b` - show/set breakpoints
* `n` - next line
* `s` - step into
* `r` - continue until return
* `c` - continue
* `var()` - show object variables
* `dir()` - show all object attributes


[example 1 with `python -m pdb`]



## ipdb - IPython debugger


* Debugger from [IPython](http://ipython.org/)

* More features:

    *"tab completion, syntax highlighting, better tracebacks, better introspection with the same interface as the pdb module"*

* I spend **a lot** of time in ipdb

* `pip install ipdb`


[ipdb shell and example 2 with `ipdb example_2*.py`]



## Requests: HTTP for Humans


* One of the most beloved Python libraries *[citation needed]*

* Easily make HTTP requests

* Build API clients


## Simple usage

```python
import requests

r = requests.get('https://httpbin.org/basic-auth/user/passwd',
                 auth=('user', 'passwd'))
```


[example of request response]


## More advanced usage

* Sometimes you want to build requests programmatically

* Useful when building API clients, persisting sessions, etc.


[example 3 code review]


[example 3 fail with `ipdb.set_trace()`]


[example 3 comparison with `ipdb.runcall(requests.post, url='https://httpbin.org/post', json={'foo': 'bar'}).json()`]



## Reporting the bug!
![](requests-presentation/irc1.png)


## Oh...
![](requests-presentation/irc2.png)


## I installed between here :/
![](requests-presentation/github.png)



There's other debuggers too!

* [PuDB](Bhttp://heather.cs.ucdavis.edu/~matloff/pudb.html)
![](http://heather.cs.ucdavis.edu/~matloff/pudb17.png)



## We did it!

Also check out http://www.pythontutor.com/

Links:
* http://jessejoe.com/other/intro_to_pdb/slides/
* https://docs.python.org/3/library/pdb.html
* https://github.com/gotcha/ipdb
* http://docs.python-requests.org
* https://httpbin.org/
