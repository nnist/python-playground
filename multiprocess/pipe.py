import multiprocessing as mp
import os

def info(conn):
    conn.send("Hello from {}\nppid = {}\npid={}".format(mp.current_process().name, os.getppid(), os.getpid()))
    conn.close()

if __name__ == '__main__':

    parent_conn, child_conn = mp.Pipe()
    p = mp.Process(target=info, args=(child_conn,))
    p.daemon = True
    p.start()
print(parent_conn.recv())
