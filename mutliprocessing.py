from multiprocessing import Pool

def f(x):
    return x*x

result_list = []
def log_result(result):
    result_list.append(result)

pool = Pool()
for each in range(1000):
    pool.apply_async(f, args=(each, ), callback=log_result)

pool.close()
pool.join()
print(result_list)