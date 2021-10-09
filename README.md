# MQTT in Python
Python Scripts for MQTT Publish and Subcribe
# List of files
- pub.py 
- data.json
- pub_conf.json
- sub.py
- sub_conf.json
- requirements.txt
- Dockerfile
- docker-compose

Description of files

- requirements.txt - required pip package for running the scripts
- data.json - Put required data in json format in data.json and pub.py sends that file as a msg-payload max size limit upto(255 mb)
- pub_conf - publisher configuration such as broker address, port and topic
- sub_conf - subscriber configuration such as broker address, port and topic

Usage

- pip install -r requirements.txt
- python pub.py --conf \path\of\pub_conf.json --data \path\of\data.json
- python sub.py --conf \path\of\sub_conf.json
