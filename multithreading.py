from threading import Thread


def multithreading(*args):
    for arg in args:
        Thread(target=arg.run).start()
