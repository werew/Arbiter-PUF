import matplotlib
import re
import matplotlib.pyplot as plt


f = open('out','r')

apuf = []
xpuf = []


for l in f:
    r = re.search("XOR PUF \(\d* stages\): (.*)",l)
    if r:
        xpuf.append(float(r.group(1)))
    else:
        r = re.search("Score arbiter PUF \(\d* stages\): (.*)",l)
        apuf.append(float(r.group(1)))

def avg(l):
    return sum(l)/len(l)
print avg(apuf)
print avg(xpuf)

quit()
y = [a for a in range(10,901)]
plt.plot(y,apuf,label="Arbiter PUF")
plt.plot(y,xpuf,label="XOR PUF")
plt.xlim([10,900])
plt.ylabel("Score")
plt.xlabel("Size training set")
plt.legend()
plt.show()

