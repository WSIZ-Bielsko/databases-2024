import datetime
from random import randint
from uuid import uuid4

from src.remote_tasks.common import ts


def fooo():
    print(datetime.datetime.now().timestamp())
    z = [datetime.datetime.now().timestamp() for _ in range(100)]
    for e in z:
        print(e)


if __name__ == '__main__':
    x = [i for i in range(10**6)]
    y = [i for i in range(10**6)]
    z = [(i,i) for i in range(10**6)]

    st = ts()
    # uids = [randint(1,10**6) for _ in range(10**6)]
    for zz in zip(x,y):
        z.append(zz)
    en = ts()
    print(f'exec time: {en-st:.3f}')
