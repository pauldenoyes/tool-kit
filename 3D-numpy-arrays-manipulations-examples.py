#3D numpy arrays manipulations examples
import numpy as np

a = [[[1., 2.87498398469379846, 3., 4.],[0., 0., 0., 0.]],
    [[11., 12., 13., 14.],[14., 15., 16., 17]],
    [[21., 22., 23., 24],[24., 25., 26., 27.]]]

print("")
print(a)

#Average on axis 0
print("")
b = np.mean(a, axis=0)
print(b)

#Average on axis 1
print("")
b = np.mean(a, axis=1)
print(b)

#Average on axis 2
print("")
b = np.mean(a, axis=2)
print(b)

#Average on several axis (here: 1 and 2)
print("")
b = np.mean(a, axis=(1,2))
print(b)

#Shapes
print("")
print(np.array(a).shape)

print("")
print(len(a))

print("")
print(len(a[0]))

print("")
print(len(a[0][0]))

print("")
b = np.reshape(a, (6, 4))
print(b)

#Transpose the 3D array in order to have the firs element of each sub-sub-list as a row in a 2D array
print("")
b = np.transpose(a, (0, 2, 1))
print(b)
c = np.reshape(b, (12, 2))
print(c)

#Extend array with inner values for a specific step size
print("")
print(np.repeat(a, 3))

# Average accross a secific dimention without taking the 0s in account
import time
print("")
start=time.time()
for i in range (0, 10000):
    #Replace zeros by nan because we can ignore them in np.nanmean
    b = np.array([[[x if x != 0 else np.nan for x in c] for c in b] for b in a])
    #Then only make the average
    c = np.nanmean(b, axis=1)
print("")
print(b)
print("")
print(c)
print(time.time()-start)
a = np.array(a)
print("")
start=time.time()
for i in range (0, 10000):
    d = np.true_divide(a.sum(1),(a!=0).sum(1))
print(d)
print(time.time()-start)
start=time.time()
for i in range (0, 10000):
    e = np.ma.masked_equal(a, 0).mean(axis=1)
print(e)
print(time.time()-start)

# Add a new column on second axis of a 3D array
print(a)
    # Shape of a
print(np.array(a).shape)
    # Create the "column" to add
c = [[[3], [3]]] * len(a)
    # Check this "column" shape
print(np.array(c).shape)
    # Add it to a
b = np.concatenate((a, c), axis=2)
print(b)

# Add elements along a NEW dimension (i.e. the inputs are 3D but the output will be 4D)
d = np.stack((a,a))
print(d)
    ## Accross other axis
d = np.stack((a,a), axis = 1)
print(d)
d = np.stack((a,a), axis = 2)
print(d)
d = np.stack((a,a), axis = -1)
print(d)

# Get the average of consecutive groups of N rows, for our 2D array a, having c columns (c/N must be an integer)
# Ok it's only 2D, but that one was so cool I couldn't resist to write it down here.
# Comes from that guy: https://stackoverflow.com/users/6583684/jona
# "Sort of" SQL NTILE
b = a.transpose().reshape(-1,N).mean(1).reshape(c,-1).transpose()
print(b)
