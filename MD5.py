import md5
import pandas as pd

df = pd.DataFrame({'var_1': [1, 2, 3], 'var_2': ['hello', 'hello', 'hello'], 'var_3': ['goodbye', 'goodbye', 'goodbye']})
df = df.astype(str)
df['row_hash'] = df.apply(lambda x: '(' + ','.join(x.dropna().values) + ')', axis=1)

def rowhasher(row):
    m = md5.new()
    m.update(row)
    return m.hexdigest()

def pandastopostgresqlhashprocessor(df):
    pass


df['row_hash_value'] = df['row_hash'].map(rowhasher)
print(df)