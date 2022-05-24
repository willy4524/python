import numpy as np
import threading

A = np.zeros((50,80))
B = np.zeros((80,50))
C = np.zeros((50,50))

for i in range(0,49):
    for j in range(0,79):
        A[i][j] = 6.6*i - 3.3*j

for i in range(0,79):
    for j in range(0,49):
        B[i][j] = 100 + 2.2*i - 5.5*j

def task(num):
  print('This is thread: ', num)
  C = format(A.dot(B))

if __name__=='__main__':
  num_threads = 1
  threads_list = []
  for i in range(num_threads):
    threads_list.append(threading.Thread(target = task, args = (i,)))
    threads_list[i].start()

  for i in range(num_threads):
    threads_list[i].join()