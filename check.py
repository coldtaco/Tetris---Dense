import pandas as pd
l = ",".join(open('saves/outputs1.txt').readlines())
l = eval(l)
df = pd.DataFrame(l)
print(df.sum()/df.shape[0])
l = ",".join(open('saves/outputs2.txt').readlines())
l = eval(l)
df = pd.DataFrame(l)
print(df.sum()/df.shape[0])