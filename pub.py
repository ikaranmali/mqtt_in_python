import paho.mqtt.client as mqtt 
import json
import sys
import time
import argparse


def parse_argv(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--conf", required=True)
    parser.add_argument("--data", required=True)
    args = parser.parse_args(argv)
    args = vars(args)    
    return args

try:
    args = parse_argv(sys.argv[1:])
    
    if args is None:
        pass
            
    conf=args.get("conf")

    with open(conf,"r+") as fp:
        data = json.load(fp)
        broker = data.get("broker")
        topic = data.get("topic")
        port = data.get("port")

except Exception as e:
	print(e)
	pass


client = mqtt.Client()

try:
    data_file = args.get("data")
    with open(data_file,"r+")as dp:
        data_stream = json.load(dp)
        data = str(data_stream)
except Exception as e:
    print(e)

try:
    client.connect(broker,port)
    print("Successfully Connected to Broker")
    print("\n Testing data is Published on Topic : {} \n".format(topic))
    
    while True:
        client.publish(topic,payload=data)
        time.sleep(1)

except KeyboardInterrupt:
    print("\n stopped \n")
    sys.exit()

except Exception as e:
    print("could not start due to {} \n ".format(e))
    

