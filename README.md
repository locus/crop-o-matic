You need Python 3.7 or greater, and the package python3-tk on Linux.

From the tkdocs:

Tkinter (and, since Python 3.1, ttk) is included in the Python standard library. We highly recommend installing Python using the standard binary distributions from python.org. These will automatically install Tcl/Tk, which of course is needed by Tkinter.

If you're instead building Python from source code, the Visual Studio projects included in the PCbuild directory can automatically fetch and compile Tcl/Tk on your system.

Once you've installed or compiled, test it out to make sure it works. From the Python prompt, enter these two commands:

>>> import tkinter
>>> tkinter._test()

This should pop up a small window; the first line at the top of the window should say "This is Tcl/Tk version 8.6"; make sure it is not 8.4 or 8.5!
