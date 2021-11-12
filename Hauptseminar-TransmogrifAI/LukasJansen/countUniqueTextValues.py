import pandas as pd
translationdict = {"int64":"int","float64":"float","object":"string"}
import argparse
import numpy as np
import sys


parser = argparse.ArgumentParser(description='Generate a Avro Schema with the help of the Pandas Parser')
parser.add_argument('inputfile', type=str,
                    help='Input file')

args = parser.parse_args()


filepath = args.inputfile



df = pd.read_csv(filepath)
#df = df[[col for col, dtype in df.dtypes.items() if str(dtype) == "object"]]
print(df.agg(lambda col: pd.Series({'nans': col.isna().sum(), 'unqiues':len(col.unique())}), axis=0).to_csv(sep="\t"))