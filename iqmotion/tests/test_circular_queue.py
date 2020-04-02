import pytest
from iqmotion.communication.circular_queue import CircularQueue


class TestCircularQueue:
    def test_init(self):
        desired_queue_size = 5
        queue = CircularQueue(desired_queue_size)

        assert queue.maxlen == desired_queue_size

    def test_init_from_iterable(self):
        iterable = [1, 2, 3, 4, 5]
        queue = CircularQueue.from_iterable(iterable)

        assert len(queue) == len(iterable)
        assert queue[::] == iterable
        assert type(queue) == CircularQueue

    def test__iter__(self):
        data = [1, 2, 3, 4, 5]
        queue = CircularQueue(5)
        for x in queue:
            # nothing is in queue, should not be reached
            assert 0

        queue.extend(data)
        for ind, x in enumerate(queue):
            assert x == data[ind]

        # test for circularity
        poped_item = queue.popleft()
        queue.append(poped_item)
        poped_item = queue.popleft()
        queue.append(poped_item)
        new_data = [3, 4, 5, 1, 2]

        for ind, x in enumerate(queue):
            assert x == new_data[ind]

    def test__len__(self):
        desired_queue_size = 3
        queue = CircularQueue(desired_queue_size)
        assert len(queue) == 0

        for i in range(3):
            queue.append(i)
            assert len(queue) == i + 1

        queue.append(4)
        assert len(queue) == desired_queue_size

        for i in range(3, 0, -1):
            queue.pop()
            assert len(queue) == i - 1

    def test__str__(self):
        data = [1, 2, 3]
        queue = CircularQueue.from_iterable(data)

        assert data.__str__() == queue.__str__()

    def test__getitem__list(self):
        data = [0, 1, 2, 3]
        queue = CircularQueue.from_iterable(data)
        with pytest.raises(TypeError):
            queue[1.1::]
        with pytest.raises(TypeError):
            queue[:1.1:]
        with pytest.raises(TypeError):
            queue[::1.1]

        for i in range(4):
            assert queue[:i] == data[:i]

        assert queue[2:-1] == data[2:-1]
        assert queue[2:] == data[2:]
        assert queue[::-1] == data[::-1]

    def test__getitem__single(self):
        data = [0, 1, 2, 3]
        queue = CircularQueue.from_iterable(data)

        with pytest.raises(IndexError):
            queue[4]
        with pytest.raises(IndexError):
            queue[-5]

        for i in range(4):
            assert queue[i] == data[i]

        # test for circularity
        queue.popleft()
        queue.append(11)
        queue.popleft()
        queue.append(12)
        new_data = [2, 3, 11, 12]

        for i in range(4):
            assert queue[i] == new_data[i]

    def test_append(self):
        desired_queue_size = 3
        queue = CircularQueue(desired_queue_size)

        for i in range(desired_queue_size):
            assert queue.append(i) == True
            assert queue[-1] == i

        assert queue.append(4) == False

    def test_extend(self):
        desired_queue_size = 3
        data = [0, 1, 2]
        queue = CircularQueue(desired_queue_size)

        queue.extend(data)

        assert queue.extend([1, 2]) == 0

        assert len(queue) == len(data)
        assert queue[::] == data

    def test_pop(self):
        desired_queue_size = 3
        queue = CircularQueue(desired_queue_size)

        assert queue.pop() == None

        for i in range(desired_queue_size):
            queue.append(i)

        for i in range(desired_queue_size - 1, -1, -1):
            assert queue.pop() == i

        assert queue.pop() == None

    def test_popleft(self):
        desired_queue_size = 3
        queue = CircularQueue(desired_queue_size)

        assert queue.popleft() == None

        for i in range(desired_queue_size):
            queue.append(i)

        for i in range(desired_queue_size):
            assert queue.popleft() == i

        assert queue.popleft() == None

    def test_clear(self):
        data = [0, 1, 2, 3]
        queue = CircularQueue.from_iterable(data)

        queue.clear()
        assert len(queue) == 0

    def test_copy(self):
        data = [0, 1, 2, 3]
        queue = CircularQueue.from_iterable(data)

        queue_copy = queue.copy()

        assert queue[::] == queue_copy[::]

    def test_maxlen(self):
        desired_queue_size = 3
        data = [0, 1, 2, 3]
        queue1 = CircularQueue(desired_queue_size)
        queue2 = CircularQueue.from_iterable(data)

        assert queue1.maxlen == desired_queue_size
        assert queue2.maxlen == len(data)

    def test_is_full(self):
        desired_queue_size = 3
        queue = CircularQueue(desired_queue_size)

        for i in range(desired_queue_size):
            assert queue.is_full == False
            queue.append(i)

        assert queue.is_full == True

        for i in range(desired_queue_size):
            queue.pop()
            assert queue.is_full == False

    def test_is_empty(self):
        desired_queue_size = 3
        queue = CircularQueue(desired_queue_size)

        assert queue.is_empty == True

        for i in range(desired_queue_size):
            queue.append(i)
            assert queue.is_empty == False

        for i in range(desired_queue_size):
            queue.pop()

        assert queue.is_empty == True
