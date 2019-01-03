import time
from threading import Lock
class Queue:
    def __init__(self, size=10):
        self.items = list()
        self.__size = size
        self.last_clearance = time.time()

    def is_empty(self):
        return len(self.items) == 0

    def is_full(self):
        return len(self.items) >= self.__size

    def enqueue(self, item):
        """
        insert item at the beginning
        :param item: the inserted item
        :return True if inserted, False if not inserted, length
        """
        if not self.is_full():
            self.items.insert(0, item)
            print("QUEUE-ADD item: %s" % item)
            return True
        return False

    def dequeue(self):
        """
        :return: item, err
        """
        if self.is_empty():
            return None, ValueError("List is empty, cannot pop!")
        item = self.items.pop()
        print("QUEUE-POP item: %s" % item)

        if self.is_empty():
            self.last_clearance = time.time()
        return item, None

    def size(self):
        return len(self.items)

    def max_size(self):
        return self.__size

    def get_last_clearance(self):
        return self.last_clearance

    def execute_clearance(self, method_to_execute, lock: Lock):
        """
        Locks the Queue and pops all items after time threshold or when the Queue is full.
        :param method_to_execute:
        :param lock:
        :return:
        """
        cleared_items = 0
        if time.time() - self.last_clearance > 10:
            lock.acquire()
            self.last_clearance = time.time()
            while not self.is_empty():
                item, err = self.dequeue()

                if err is None:
                    method_to_execute(item)
                    cleared_items += 1
                else:
                    print("ERROR: %s" % err)
            lock.release()
        elif self.is_full():
            self.last_clearance = time.time()
            lock.acquire()
            while not self.is_empty():
                item, err = self.dequeue()
                if err is None:
                    method_to_execute(item)
                    cleared_items += 1
                else:
                    print("ERROR: %s" % err)
            lock.release()

        time.sleep(0.1)
        if cleared_items > 0:
            print("Cleared %s items" % cleared_items)
        return cleared_items






