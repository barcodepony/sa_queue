from multiprocessing.connection import Listener
from basic_queue.Queue import Queue
from threading import Thread, Lock
from common.DBConnector import DBC
class QueueListener(object):
    def __init__(self, address: str = "0.0.0.0", port: int = 6000, authkey=b'defaultkey'):
        self.address = address
        self.port = port
        self.__key = authkey
        self.listener = Listener((self.address, self.port), authkey=self.__key)

    def listen(self, lock: Lock, queue: Queue):
        while True:
            with self.listener.accept() as conn:
                print("connection accepted from: ", self.listener.last_accepted)
                data = conn.recv()
                lock.acquire()
                queue.enqueue(data)
                lock.release()


def main():
    queue = Queue(size=10)
    lock = Lock()
    dbc = DBC()
    dbc.connect()
    dataListener = QueueListener()
    thread = Thread(target=dataListener.listen, args=(lock, queue))
    thread.start()

    print("Queue is active")
    while True:
        if not thread.isAlive():
            print("ERR: DataListener is not Active, shutting down.")
            break
        queue.execute_clearance(dbc.safe_execute_sql, lock)
    print("Queue is deactivated")


if __name__ == "__main__":
    print("Starting Queue Handle..")
    main()
    print("Terminating Queue Handle..")
