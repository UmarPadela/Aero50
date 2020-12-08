This is my final project for CS50. It is an airfoil analysis tool.
Video:
https://youtu.be/k2RsEiC_zo0

## INSTALLATION:

To use this code, you will need to download a few modules. First is matplotlib. If you do not have matplotlib, you can install it using

```
python -m pip install -U pip
python -m pip install -U matplotlib
```

in the command line. Next is numpy. If you do not have numpy, you can install it using

```
pip install numpy
(https://numpy.org/install/)
```

in the command line. The code also uses the CS50 Python module. If you do not have it, you can install it using

```
pip3 install cs50
(https://github.com/cs50/python-cs50/blob/develop/README.md)
```

in the command line. The code also uses Flask. If you do not have it, you can still it using

```
pip install Flask
(https://flask.palletsprojects.com/en/1.1.x/installation/)
```

in the command line. Finally, the code uses a Python implementation of XFOIL. This can be installed using

```
pip install xfoil
(https://pypi.org/project/xfoil/)
```

## TESTING:

To test that you have installed all of these modules correctly, open your IDE and try importing them. For example, you can type the following:

```
import matplotlib
import numpy
import cs50
import flask
from xfoil import XFoil
```

If you are able to run this without error, it means you have installed the necessary modules correctly. 

## USAGE: 

I worked in VSC, and to execute my code, I had to run the following: 

```
$env:FLASK_APP = "application.py"
flask run
```

Once you've done this, you should be able to open the webapp. From there, you can register an account and play around with the analyze, favorites, and history tabs. The analyze tab allows you to input airfoil parameters for which you would like to run an analysis. These parameters include the airfoil to be analyzed, the independent variable (angle of attack or coefficient of lift), the analysis type (inviscid or viscous), and the maximum iterations. If you are unsure of which analysis you would like to run, you can use the following as a test case.

```
Airfoil: 2412
Independent Variable: Angle of Attack
Starting Angle of Attack: 0
Ending Angle of Attack: 15
Step for Angle of Attack: 0.5
Analysis Method: Inviscid
Max Iterations: 100
```

The code will take a few seconds to run, and you will get an output with a lift curve, drag polar, minimum pressure curve, pressure distribution, and pitching moment curve. If you like the analysis, you can save it to your favorites by clicking the button "save to favorites" at the bottom of the page. This will bring you to your favorites page, where you can view your analyses and click buttons to see their plots. The history tab shows all of your analyses, but does not save your plots. 
