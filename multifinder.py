from multiprocessing import Process, Queue, Pool
import os
from pathlib import Path

# End of data
sentinel = -1


def FindFilesToProcess(dirList, q):
    """
    OS walk rootdir, finding files and enqueuing them to q
    """
#    print('Creating data and putting it on the queue')
#    for item in data:
#       q.put(item)
    print("{} Producer working".format(os.getpid()))
    while dirList:
        aPath = dirList.pop()

        #check for subdirs & enque to dirList
        subdirs = [x for x in aPath.iterdir() if x.is_dir()]
        dirList.extend(subdirs)

        #check for files and enque to q
        filelist = [x for x in aPath.iterdir() if x.is_file()]
        for fname in filelist:
            #print('Found file: %s' % fname)
            print(".", end="")
            q.put(fname)

    #no more dirs, thus we're done
    q.put(sentinel)



def my_consumer(q):
    """
    Consumes some data and works on it

    In this case, all it does is double the input
    """
    mypid = os.getpid()
    mysimpleid = int(repr(mypid)[-1])
    myworkcount = 0
    print("{} Consumer working".format(mypid))
    while True:
        data = q.get()
        if data is sentinel:
            q.put(sentinel) # putback on for the other threads
            print("{} Consumer quitting".format(os.getpid()))
            break;
        # data is a Path otherwise
        #print('data found to be processed: {}'.format(data))
        print("{}".format(mysimpleid))
        myworkcount += 1
        #processed = data * 2
        #print(processed)
    print("\nid:{} done, itemsprocessed: {}".format(mysimpleid, myworkcount))




if __name__ == '__main__':
    q = Queue()
    NUMPROCESSTHREADS = 5
    #data = [5, 10, 13, 25, 45, 100, 1000-1]
    #pathtoscan = 'c:\\Intel'
    dirList =  [Path('/Users/accoday/Documents/')]
    # windows version: dirList = [Path('c:\\cygwin64')]
    process_one = Process(target=FindFilesToProcess, args=(dirList, q))
    the_pool = Pool(NUMPROCESSTHREADS, my_consumer, (q,))

    #process_two = Process(target=my_consumer, args=(q,))
    process_one.start()
    #process_two.start()

    # mark the queue to be joined (i.e. wait for process one to finish)
    q.close()
    q.join_thread()

    process_one.join()
    #process_two.join()
