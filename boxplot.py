# arquivo boxplot.py
# library & dataset
import seaborn as sns
# Instruções de instalação
import matplotlib.pyplot as plt
import pandas as pd

def example1():
    mydata=[1,2,3,4,5,6,12]
    mydata2 = [10, 20, 30, 40, 50, 60]
    sns.boxplot(y=mydata) # Also accepts numpy arrays
    plt.show()

def example2():
    df = sns.load_dataset('iris')
    #returns a DataFrame object. This dataset has 150 examples.
    print(df)
    # Make boxplot for each group
    sns.boxplot( data=df.loc[:,:] )
    # loc[:,:] means all lines and all columns
    plt.show()
example1()
# example2()