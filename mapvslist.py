import time


def test_function(x):
    return x * 1


class TimeDecorator():

    def __init__(self, repeat=10):
        print("Repeating {} times".format(repeat))
        self.repeat = repeat

    def __call__(self, func):
        def wrapper():
            time_event = []
            for _ in range(self.repeat):
                start = time.time()
                func()
                end = time.time()
                time_event.append(end - start)
            return sum(time_event) / self.repeat
        return wrapper


@TimeDecorator(repeat=100)
def test_1(repeat=100000):
    event = [x * 1 for x in range(repeat)]
    pass

@TimeDecorator(repeat=100)
def test_2(repeat=100000):
    event = map(lambda x: x * 1, range(repeat))
    pass

print(test_1())
print(test_2())

