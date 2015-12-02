import zmq

class ZMQLocalContext(zmq.Context):
    # Pass everything to parent class init method
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def publisher(self, filename):
        socket = self.socket(zmq.PUB)
        socket.bind("ipc://%s" % filename)
        print('Write to ZMQ Socket through file: ', filename)
        return socket

    def lazy_subscriber(self, filename):
        try:
            socket = self.socket(zmq.SUB)

            socket.setsockopt(zmq.SUBSCRIBE, b'')
            socket.setsockopt(zmq.CONFLATE, 1)
            socket.setsockopt(zmq.RCVTIMEO, 300)

            socket.connect("ipc://%s" % filename)
            print('Listen to ZMQ Socket through file: ', filename)
        except zmq.ZMQError:
            print('Invalid socket connection.')
            traceback.print_exc()
            sys.exit()
        return socket
