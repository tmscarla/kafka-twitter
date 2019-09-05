from multiprocessing import Process, Manager

def worker(x, i, *args):
    sub_l = manager.list(x[i])
    sub_l.append(i)
    x[i] = sub_l


if __name__ == '__main__':
    manager = Manager()
    x = manager.list([[]]*5)
    print(x)
    p = []
    for i in range(5):
        p.append(Process(target=worker, args=(x, i)))
        p[i].start()

    for i in range(5):
        p[i].join()

    print(x)
