import pandas as pd
import numpy as np
l = np.load('saves/outputs1.npy')
df = pd.DataFrame(l)
print(df.sum()/df.shape[0])
l = np.load('saves/outputs2.npy')
df = pd.DataFrame(l)
print(df.sum()/df.shape[0])