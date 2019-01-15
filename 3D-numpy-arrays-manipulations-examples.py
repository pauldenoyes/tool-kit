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
