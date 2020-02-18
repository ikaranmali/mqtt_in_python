import paho.mqtt.client as mqtt 
import json
import sys
import time
import argparse
import logging
import logging.handlers


def parse_argv(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--conf", required=True)
    parser.add_argument("--data", required=True)
    args = parser.parse_args(argv)
    args = vars(args)    
    return args

#Reading Params from Conf file
try:
    args = parse_argv(sys.argv[1:])
    
    if args is None:
        pass
            
    conf_file=args.get("conf")

    with open(conf_file,"r+") as fp:
        params   = json.load(fp)
        broker = params.get("broker")
        topic  = params.get("topic")
        port   = params.get("port")
        t      = params.get("time")
        qos    = params.get("qos")
        log    = params.get("log")
        

    assert broker is not None, "param broker missing"
    assert topic is not None, "param topic missing"
    assert port is not None, "param port missing"
    assert qos is not None, "Param qos missing"
    assert log is not None, "param log missing"
    assert t is not None,"param time missing"
    
        
except Exception as e:
	print(e)
    # logger.info("Exception in reading conf file {}".format(repr(e)))
	pass

try:
    logger = logging.getLogger("Records")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
            handler_records = logging.handlers.RotatingFileHandler(log, maxBytes=512000, backupCount=1000)
            formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s for %(message)s')
            handler_records.setFormatter(formatter)
            logger.addHandler(handler_records)

except Exception as e:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    # Suppress overly verbose logs from libraries that aren't helpful
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)


#Mqtt object for connection  
client = mqtt.Client()

#Establishing Connection with broker
try:
    client.connect(broker,port)
    logger.info("Connected to broker started publishing..")
    print("\n Data Published on Topic-({}) at QOS level-({}) \n".format(topic,qos))
    # print("Successfully Connected to Broker")
    
    #Publishing Json data to the topic
    try:
        while True:
            #Reading the data file to export data
            try:
                data_file = args.get("data")
                with open(data_file,"r+")as dp:
                    data_stream = json.load(dp)
                data = str(data_stream)
            except Exception as e:
                logger.info("could not load conf file {}".format(repr(e)))
            client.loop_start()
            client.publish(topic,payload=data,qos=qos)
            #inducing 1 second of sleep to send data at everysecond
            time.sleep(t)

    except Exception as e:
        logger.info("Error in publishing data {}".format(repr(e)))
        pass

except Exception as e:
    print("could not start due to {} \n ".format(e))
    logger.info("Error in making connection to broker {}".format(repr(e)))
    pass

except KeyboardInterrupt:
    print("\n stopped \n")
    client.loop_stop()
    logger.info(" User stopped ")
    sys.exit()

