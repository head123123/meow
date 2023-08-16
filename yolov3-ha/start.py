import os

os.popen('pip install -r /usr/app/requirements.txt')
os.popen('python /usr/app/smartcam-ocv.py -c config.yaml')