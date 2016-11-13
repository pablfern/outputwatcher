# https://github.com/liris/websocket-client
# https://blockchain.info/es/api/api_websocket

import json
import websocket
import thread
import time
from datetime import datetime, timedelta

def on_message(ws, message):
    print message

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    def run(*args):
        next_ping = datetime.now() + timedelta(seconds=25)
        while True:
            time.sleep(1)
            if datetime.now()>next_ping:
                ws.send(json.dumps({"op": "ping"}))
                next_ping = datetime.now() + timedelta(seconds=25)
            else:
                ws.send(json.dumps({"op":"unconfirmed_sub"}))
        ws.close()
        print "thread terminating..."
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.blockchain.info/inv",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()




