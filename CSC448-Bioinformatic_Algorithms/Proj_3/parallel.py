import multiprocessing as mp

pool = mp.Pool(num_process = 5)
pool.map(function, input[1])