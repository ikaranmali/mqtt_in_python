import paho.mqtt.client as mqtt #import the client1
import json
import sys
import time
import argparse


def parse_argv(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--conf", required=True)
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
        topic = data.get("topic")
        broker = data.get("broker")
        port = data.get("port")
		
except Exception as e:
	print(e)
	pass

client = mqtt.Client() #create new instance
print("connecting to broker: {}" .format(broker))

try:
    client.connect(broker,port) #connect to broker
    client.subscribe(topic)
    print("subscribed to: {}".format(topic))

except Exception as e:
    print(e)
    print("Unable to connect to broker, please check the broker's IP.")
    sys.exit()

except KeyboardInterrupt:
    print("\n Stopped \n")
    sys.exit()


def on_message(client, userdata, msg):
    msg_payload = msg.payload.decode("utf-8")
    print(msg_payload)

try:
    client.on_message = on_message
    client.loop_forever()
except KeyboardInterrupt:
    print("\n Stopped \n")
    sys.exit()