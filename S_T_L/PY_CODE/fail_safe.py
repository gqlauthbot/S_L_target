from multiprocessing import Process, Queue, Array

def process1(in_queue, out_queue):
    # Receives data, modifies it and sends it back
    while True:
        data = in_queue.get() # Receive data
        if data is None:
            out_queue.put(None)  # send feedback about END message
            out_queue.close()
            out_queue.join_thread()
            break

        data *= 2 # Data modification
        out_queue.put(data) # Send data

def process2(in_queue, out_queue, how_many):
    data = 0

    # Receives data, increments it and sends data back
    while how_many > 0:
        data += 1 # Data modification
        out_queue.put(data) # Send data
        how_many -= 1

        data = in_queue.get() # Receive data
        if data is None:
            break

    # send END message
    out_queue.put(None)
    out_queue.close()
    out_queue.join_thread()
    assert in_queue.get() is None


if __name__ == "__main__":
    q1 = Queue()
    q2 = Queue()

    process_1 = Process(target=process1, args=(q1, q2))
    process_2 = Process(target=process2, args=(q2, q1, 10))
    process_1.start()
    process_2.start()

    process_2.join()
    process_1.join()
    q1.close()
    q2.close()
    q1.join_thread()
    q2.join_thread()