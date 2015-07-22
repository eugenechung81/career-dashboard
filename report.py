__author__ = 'eugene'


# find last updated
# with open("gmail_status.csv") as f:
#     lines = [line.rstrip() for line in f]
# for line in (open("gmail_status.csv").readlines()):
#     print line.split(',')[0]
# for line in reversed(open("gmail_status.csv").readlines()):
#     print line.rstrip('\n')
# last_updated = None
# [(line.rstrip('\n').split(',')[0],line.rstrip('\n').split(',')[1]) for line in reversed(open("gmail_status.csv").readlines())]

# produce reverse order '1'
def get_last_updated():
    last_updates = [line.rstrip('\n').split(',')[0] for line in reversed(open("gmail_status.csv").readlines()) if line.rstrip('\n').split(',')[1] == '1']
    ms = float(last_updates[0])
    import datetime
    print 'Last updated: %s' % datetime.datetime.fromtimestamp(ms).strftime('%Y-%m-%d %H:%M:%S')
    return ms

updated = get_last_updated()


# report
import numpy as np
import matplotlib.pyplot as plt

N = 50
x = np.random.rand(N)
# y = np.random.rand(N)
y = np.ones(N) # 1 #[1 for x in range(N)]
colors = np.random.rand(N)
area = np.pi * (15 * np.random.rand(N))**2 # 0 to 15 point radiuses

plt.scatter(x, y, s=area, c=colors, alpha=0.5)
plt.show()


# reporting
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.DataFrame(np.random.rand(50, 4), columns=['a', 'b', 'c', 'd'])
df.plot(kind='scatter', x='a', y='b');
plt.show()

df = pd.read_csv('gmail_status.csv', header=None, names=['timestamp','activity'])
df.plot(kind='scatter', x='timestamp', y='activity')
plt.show()


# 1437238518.32,0
# 1437238530.34,1
# 1437238542.29,1
# 1437238554.13,0
# 1437245954.88,0
# 1437245966.74,0
# 1437245978.41,0
# 1437245990.25,0
# 1437246001.96,1
# 1437246037.72,0
# 1437246026.2,0
# 1437246049.35,0
# 1437246060.83,0

