# Crop-O-Matic

This is a quick and dirty cropping utility I made using Python 3.7 and Tkinter. The code is not pretty but it works. I intend to eventually make the code way more readable and organized; right now I needed something that worked good, and I needed it fast.

## Installation

To run this utility, you need Python 3.7 or greater and the Tkinter library, which noramlly comes prepackaged with Python. On Linux, you also need to install the package `python3-tk`. On Windows, the situation may be a little bit different... From the tkdocs:

>Tkinter (and, since Python 3.1, ttk) is included in the Python standard library. We highly recommend installing Python using the standard binary distributions from python.org. These will automatically install Tcl/Tk, which of course is needed by Tkinter.
>
>If you're instead building Python from source code, the Visual Studio projects included in the PCbuild directory can automatically fetch and compile Tcl/Tk on your system.
>
>Once you've installed or compiled, test it out to make sure it works. From the Python prompt, enter these two commands:
>
>```python
>>>> import tkinter
>>>> tkinter._test()
>```
>
>This should pop up a small window; the first line at the top of the window should say "This is Tcl/Tk version 8.6"; make sure it is not 8.4 or 8.5!

Once Python 3.7 or greater and Tkinter are installed on your computer, you need to meet the requirements of the `requirements.txt` file. Preferably within a vitrual environment, you would do:

```
$ cd path/to/crop-o-matic
$ pip install -r requirements.txt
```

To create a virtual environment before you install the requirements, you can use for instance venv. Be sure that you use venv with a version of Python that is greater or equal to 3.7, as I do in this example:

```
$ cd path/to/crop-o-matic
$ python3.7 -m venv .venv
$ source .venv/bin/activate
(.venv) $
```

Note that the `source` command may not work on Windows. I am not sure how virtual environments work on that platform.

## Usage

To launch the program, simply run the script, as such:

```
$ python crop-o-matic.py
```

Remember that the version of Python must be 3.7 or greater. I greatly recommend a virtual environment for this kind of thing.

Click on the button at the top left to load some pictures' filenames into memory (you may select more than one). Once a picture is loaded, the crop zone (a big red rectangle) will appear. It is the biggest rectangle that can fit inside the picture while still being at a 1.77 ratio. This ratio may be width:height or height:width, depending on the geometry of the picture. Once the crop zone is at an appropriate place on the picture, press the `c` key to crop. **The program will automatically override the old picture with the new cropped one, so be careful.**
