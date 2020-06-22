class CircularQueue:
    """ A fix size circular queue implemented with a list() for O(1) memory movement costs anywhere in the queue
        The queue is FIFO if you use the __iter__ method and/or popleft(), but can be LIFO with pop()
    """

    def __init__(self, maxlen: int):
        """ Create an empty circular queue of ints of size "size"

        Args:
            size (int): Size of the circular queue
        """

        self._queue = [None for i in range(maxlen)]
        self._front = -1
        self._rear = -1
        self._count = 0
        self._maxlen = maxlen

    @classmethod
    def from_iterable(cls, iterable: iter):
        """ Create an circular queue from an iterable with size len(iterable)

        Args:
            iterable (iter): The iterable the queue will copy
        """
        iterable_len = len(iterable)

        new_queue = CircularQueue(iterable_len)
        new_queue.extend(iterable)

        return new_queue

    def __iter__(self):
        """ Peek iteratively over the queue in a FIFO way, this method does NOT pop the element
        """
        if not self.is_empty:

            front_index = self._front
            for _ in range(self._count):
                peeked_element = self._queue[front_index]
                front_index = (front_index + 1) % self._maxlen

                yield peeked_element

    def __len__(self):
        return self._count

    def __str__(self):
        list_from_queue = self._queue[self._front : self._rear + 1]
        return list_from_queue.__str__()

    def __getitem__(self, key):
        """ Slicing multiple elements is not fast, this will copy the queue as a list and slice this list.
            Slicing one element is alot faster, equivalent to a "peek" but for any index position
        """
        if isinstance(key, slice):
            return self._parse_queue_from_slice(key)

        self._check_key_in_range(key)

        actual_index = self._calculate_actual_queue_index(key)

        return self._queue[actual_index]

    def _parse_queue_from_slice(self, wanted_slice):
        queue_as_list = []
        for item in self:
            queue_as_list.append(item)

        return queue_as_list[wanted_slice]

    def _check_key_in_range(self, key):
        if key >= 0:
            if key > self._count - 1:
                raise IndexError("IndexError: queue index out of range")

        elif abs(key) > self._count:
            raise IndexError("IndexError: queue index out of range")

    def _calculate_actual_queue_index(self, key):
        if key < 0:
            wanted_index = self._count + key
        else:
            wanted_index = key

        actual_index = self._front + wanted_index
        if actual_index > self._maxlen - 1:
            actual_index = actual_index % self._count

        return actual_index

    def append(self, x):
        """ Add an item to the end of the list.

        Args:
            x: Item you want to append.

        Returns:
            true: if succesful
            false: if circular queue is full
        """
        if self.is_full:
            return 0

        # condition for empty queue
        if self.is_empty:
            self._front = 0
            self._rear = 0
        else:
            # next position of rear
            self._rear = (self._rear + 1) % self._maxlen

        self._count += 1
        self._queue[self._rear] = x

        return 1

    def extend(self, iterable: iter):
        """ Extend the list by appending all the items from the iterable.

        Args:
            iterable (iter): Iterable object you want to add to your queue.

        Returns:
            true: if succesful
            false: if circular queue is full
        """
        for x in iterable:
            if not self.append(x):
                return 0

        return 1

    def pop(self):
        """ Remove and return an element from the right side of the circular queue.

        Returns:
            None: if queue is empty
            poped_element: element from queue that got poped
        """
        if self.is_empty:
            return None

        poped_element = self._queue[self._rear]

        # condition for only one element
        if self._front == self._rear:
            self._front = -1
            self._rear = -1
        else:
            self._rear = (self._rear - 1) % self._maxlen

        self._count -= 1
        return poped_element

    def popleft(self):
        """ Remove and return an element from the left side of the circular queue.

        Returns:
            None: if queue is empty
            poped_element: element from queue that got poped
        """
        if self.is_empty:
            return None

        poped_element = self._queue[self._front]

        # condition for only one element
        if self._front == self._rear:
            self._front = -1
            self._rear = -1
        else:
            self._front = (self._front + 1) % self._maxlen

        self._count -= 1
        return poped_element

    def clear(self):
        """ Remove all elements from the circular queue.
        """
        self._front = -1
        self._rear = -1
        self._count = 0

    def copy(self):
        """ copy of the circular queue.

        Return:
            (CircularQueue): copy of circular queue
        """
        cq = CircularQueue.from_iterable(self)
        return cq

    @property
    def maxlen(self):
        """ Maximum size of the circular queue.

        Return:
            Maximum size of the circular queue.
        """
        return self._maxlen

    @property
    def is_full(self):
        """ Check if queue is full

        Returns:
            true: if queue is full
        """
        # condition if queue is full
        if (self._rear + 1) % self._maxlen == self._front:
            return 1

        return 0

    @property
    def is_empty(self):
        """ Check if queue is empty

        Returns:
            true: if queue is empty
        """
        if not self._front == -1:
            return 0

        return 1
