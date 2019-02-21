# lets use a GPU with tensorflow
# check if your GPU is supported here: https://developer.nvidia.com/cuda-gpus
# you will need to install CUDA Toolkit and cuDNN if you haven't already
# dont forget to install the tensorflow-gpu package with pip
# you can do this with the provided powershell script
# update your graphics drivers, this will only work with CUDA (driver should be => 384.x)
# if this does not run, please make sure CuDNN is added to your Path
import tensorflow

# Logging Device Placement, lets detect what we've got!

# lets create a graph
a = tensorflow.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3], name='a')
b = tensorflow.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2], name='b')
c = tensorflow.matmul(a, b)

# lets create a session with log_device_placement set to True
session = tensorflow.Session(config=tensorflow.ConfigProto(log_device_placement=True))

# run
print(session.run(c))

# the above will automatically use GPU:0 if its found, otherwise fall back to CPU:0
# if we would like to manually choose which Device to use we can do this:

# lets create a graph again but this time with tensorflow.device('/cpu:0')
with tensorflow.device('/cpu:0'):
  a = tensorflow.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3], name='a')
  b = tensorflow.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2], name='b')
c = tensorflow.matmul(a, b)

# lets create a session with log_device_placement set to True
session = tensorflow.Session(config=tensorflow.ConfigProto(log_device_placement=True))

# Run
print(session.run(c))

# lets allow GPU Memory Growth
# by default, tensorflow will eat up as much memory of each GPU attached as it can, according to CUDA_VISIBLE_DEVICES
# lets make it so this is not the case and have it grow memory as needed instead

# using allow_growth 
# attempts to allocate only as much GPU memory based on runtime allocations: 
# it starts out allocating very little memory, and as Sessions get run and more GPU memory is needed, 
# we extend the GPU memory region needed by the TensorFlow process. Note that we do not release memory, 
# since that can lead to even worse memory fragmentation. 
# To turn this option on, set the option in the ConfigProto by:

config = tensorflow.ConfigProto()
config.gpu_options.allow_growth = True
session = tensorflow.Session(config=tensorflow.ConfigProto(log_device_placement=True))

# Run
print(session.run(c))

# using per_process_gpu_memory_fraction 
# determines the fraction of the overall amount of memory that each visible GPU should be allocated. 
# For example, you can tell TensorFlow to only allocate 40% of the total memory of each GPU by:

config = tensorflow.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.4
session = tensorflow.Session(config=tensorflow.ConfigProto(log_device_placement=True))

# Run
print(session.run(c))

# what if we have more than 1 GPU????
# the first GPU (lowest ID) is selected first
# you must tell Tensorflow if you want to use another:
# if you do not have '/device:GPU:2' this will fail unless using allow_soft_placement
# which will choose next supported device

# Graph
with tensorflow.device('/device:GPU:2'):
  a = tensorflow.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3], name='a')
  b = tensorflow.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2], name='b')
  c = tensorflow.matmul(a, b)

# Session with allow_soft_placement
session = tensorflow.Session(config=tensorflow.ConfigProto(allow_soft_placement=True, log_device_placement=True))

# Run
print(session.run(c))

# now lets use multiple GPUs at once:
# once again, will fail if we don't have these devices and do not use allow_soft_placement

# Graph
c = []
for gpus in ['/device:GPU:2', '/device:GPU:3']:
  with tensorflow.device(gpus):
    a = tensorflow.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3])
    b = tensorflow.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2])
    c.append(tensorflow.matmul(a, b))
with tensorflow.device('/cpu:0'):
  sum = tensorflow.add_n(c)


# Session
session = tensorflow.Session(config=tensorflow.ConfigProto(allow_soft_placement=True, log_device_placement=True))

# Run
print(session.run(sum))

