# Don't include pip if on Ubuntu
py -3.7 -m pip install --upgrade pip virtualenv

py -3.7 -m virtualenv venv
source venv/Scripts/activate

py -3.7 -m pip install -r requirements.txt
