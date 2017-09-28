#!/usr/bin/env python3

import tqdm
import argparse
import sys
import os
import logging
import time
import multiprocessing.dummy # multithread
#import multiprocessing # multiprocess

class TqdmLoggingHandler(logging.Handler):
    def __init__(self, level = logging.NOTSET):
        super(self.__class__, self).__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.tqdm.write(msg)
            self.flush()
        except(KeyboardInterrupt, SystemExit):
            raise
        except:
            print('oh no')
            pass
            # TODO fix this
            #self.handleError(record)

def worker(args):
    # Do stuff (no printing because it would interfere with progress bar)
    time.sleep(0.1)
    return True

def multithread_func(threads=1):
    log = logging.getLogger(__name__)

    # Create things for workers to do
    worker_args = []
    for i in range(100):
        worker_args.append('item_{}'.format(str(i)))

    # Create threads and handle their results
    pool = multiprocessing.dummy.Pool(threads)
    it = pool.imap_unordered(worker, worker_args)
    pbar = tqdm.tqdm(total=100)
    for results in enumerate(it):
        # Handle results
        if results[1] is True:
            log.info('Thread {} finished successfully.'.format(results[0]))
        else:
            log.error('Thread {} did not finish successfully.'.format(results[0]))
        pbar.update()

    pbar.close()
    pool.close()
    pool.join()

def main(argv):
    parser = argparse.ArgumentParser(description='The description goes here.')

    parser.add_argument(
        '-d', '--debug',
        help='Print lots of debugging statements',
        action='store_const', dest='loglevel', const=logging.DEBUG,
        default=logging.ERROR,
    )
    parser.add_argument(
        '-v', '--verbose',
        help='Be verbose',
        action='store_const', dest='loglevel', const=logging.INFO,
        default=logging.ERROR,
    )
    # TODO argument for number of threads

    args = parser.parse_args()
    
    # Set up logging
    log = logging.getLogger(__name__)
    log.setLevel(args.loglevel)
    handler = TqdmLoggingHandler()
    handler.setLevel(args.loglevel)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)

    # Stuff goes here
    multithread_func()

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted by user.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
