# asteroids
Modified version of the asteroid program tutorial from Real Python to fit into a single lesson

## Step 0
Clone the repository on github using GitHub Desktop and open the project using vscode. This repository is `KillarneyHeightsHS\asteroids`

Remember in vscode you can have a terminal window with a command line open by pressing ``Ctrl+` ``
## Step 1
Ensure Python is installed
windows: `py.exe --version`
or
mac: `python3 --version`

If you have install python previously but will not run from the command line, try reinstalling and ensure that you check the option to include python in you `PATH`.

## Step 2
Ensure pip is installed. 

pip is a package manager for python. It helps add and manage 3rd party libraries that you can use for coding.

windows: `py.exe -m ensurepip`
or
mac: `python3 -m ensurepip`

If pip is installed you should see something similar to the following:
```
PS C:\Users\abeverley3\Documents\GitHub\asteroids> py.exe -m ensurepip
Looking in links: c:\Users\abeverley3\AppData\Local\Temp\tmpox97ui65
Requirement already satisfied: pip in c:\users\abeverley3\appdata\local\programs\python\python313\lib\site-packages (25.0.1)
```

## Step 3
Create a virtual environment. This will allow us to run our code in its own space and help ensure that all commands work without the need to change the overall computer setup.

`py.exe -m venv .venv`
or 
`python3 -m venv .venv`

To confirm this has worked and start the virtual environment type the following:
windows: `.\.venv\Scripts\Activate.bat`
or 
mac: `source .venv/bin/activate`

If this is successful your terminal should look something like:
- windows:
```
(.venv) PS C:\Users\abeverley3\Documents\GitHub\asteroids\.venv\Scripts>
```
- mac:
```
(.venv) aaron@Mac asteroids %
```

## Step 4
Install the required libraries using pip
`pip install -r requirements.txt`

## Step 5
Run the code to check that everything is working.
`python.exe main.py`
or
`python3 main.py`