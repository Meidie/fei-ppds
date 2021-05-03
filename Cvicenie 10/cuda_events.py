from numba import cuda
import numpy as np

# ARRAY_LEN = 78 * 1024**2
ARRAY_LEN = 78 * 1024


@cuda.jit
def kernel(array):
    thd = cuda.grid(1)
    num_iters = array.size // cuda.blockDim.x
    for j in range(num_iters):
        i = j * cuda.blockDim.x + thd
        for k in range(50):
            array[i] *= 2.0
            array[i] /= 2.0


data = np.random.randn(ARRAY_LEN).astype('float32')
data_gpu = cuda.to_device(data)

start_event = cuda.event()
end_event = cuda.event()

start_event.record()
kernel[1, 64](data_gpu)
end_event.record()

# pockanie na dokoncenie `end_event`
end_event.synchronize()

print('Kernel execution time in milliseconds: %f ' %
      cuda.event.elapsed_time(start_event, end_event))
