# Python
1. Check your Python install:
|  Operating system  |  Command  |
| ------------- | ------------- |
|  Windows  |  `py -3 -V`, `py -V`, `python -3 -V` or `python -V`  |
|  Linux  | `python3 -V`  |

If 

If any of these commands on your operating system give an error similar to `command "python" not found`, then you will need to install Python. Proceed to the next step to do so.

2. [Install Python 3.7+](https://www.python.org/downloads/)
![](images/install_python/install.png)

3. Check your Python version:

4. Create a virtual environment:
|  Operating system  |  Command  |
| ------------- | ------------- |
|  Windows  |  `py -3 -m pip install --user -r requirements.txt`  |
|  Linux  | `python3 -m pip install --user -r requirements.txt`  |

# Config file
1. Within `config/`, create a new file called `config.json`.
2. Copy the internals of `config.txt` into the .json file.
3. insert data from the steps that will be taken in the following instructions.