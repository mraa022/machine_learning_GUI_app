import pandas as pd


df = pd.read_csv('/Users/adnanbadri/Documents/web_dev/Personal_Projects/machine_learning_gui/media/datasets/formated_dataset.csv')
dummies = pd.get_dummies(df.Pclass,drop_first=True)
df = df.drop(columns=['Pclass'])
df = pd.concat([df,dummies],axis=1)
print(df.head())
print('\n')
print(pd.read_csv('/Users/adnanbadri/Documents/web_dev/Personal_Projects/machine_learning_gui/media/datasets/formated_dataset.csv').head())