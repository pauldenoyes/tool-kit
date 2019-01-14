#3D numpy arrays manipulations examples
import numpy as np

a = [[[1., 2., 3., 4.],[5., 6., 7., 0.]],
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

#Extend array with inner values for a specific step size
print("")
print(np.repeat(a, 3))

# Average without taking the 0s in account
print("")
#Replace zeros by nan because we can ignore them in np.nanmean
b = np.array([[[x if x != 0 else np.nan for x in c] for c in b] for b in a])
print(b)
#Then only make the average
print("")
c = np.nanmean(b, axis=0)
print(c)
