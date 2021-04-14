import pandas as pd
from scipy.stats import zscore

def check_datasets(position):
    # position: the path of the csv file
    df = pd.read_csv(position)
    if ('Adj Close' not in df.columns):
        print("This dataset does not contain Adj Close, please find another one")
    else:
        if (not df.isnull):
            print('The dataset is ok')
        else:
            print('The dataset has NaN values')
            for col in df.columns:
                if (df[col].dtype == float or df[col].dtype == int):
                    median=df[col].median()
                    df[col].fillna(median, inplace=True)
                    print("The dataset is ok")
    return df  


def normalized_data(position, metric):
    # position: path of the csv
    # way to normalize
    df = check_datasets(position)
    if (metric.lower() == 'zscore'):
        for col in df.columns:
            if (df[col].dtype == float or df[col].dtype == int):
                df[col] = zscore(df[col])
    elif (metric.lower() == 'minmax'):
        for col in df.columns:
            if (df[col].dtype == float or df[col].dtype == int):
                xmin, xmax = df[col].min(), df[col].max()
                df[col] = (df[col] - xmin) / (xmax - xmin)
    return df 

 def split_dataset(position, normalize=False, size=[0.9, 0.05]):
     # position: path of the csv
     # normalize: choose to normalize the data or not
     # size: array containing the size of the [train_set, val_set]
    if (normalize):
         metric = input('Enter which way you want to normalize your data(zscore or MinMax):' )
         df = normalized_data(position, metric)
    else:
        df = check_datasets(position)
    if ((1 - size[0] - size[1]) < 0):
        size[0] = 0.9
         size[1] = 0.05
    train_set = df.loc[:int(len(df) * size[0])]
    val_set = df.loc[int(len(df) * size[0]) : int((size[0] + size[1]) * len(df))]
    test_set = df.loc[int((size[0] + size[1]) * len(df)) : ]
    
    train_set.to_csv('./train_set.csv')
    test_set.to_csv('./test_set.csv')
    val_set.to_csv('./val_set.csv')
    return train_set, val_set, test_set   
        

            

