import pandas as pd
translationdict = {"int64":"int","float64":"double","object":"string"}
import argparse
import json
import sys


parser = argparse.ArgumentParser(description='Generate a Avro Schema with the help of the Pandas Parser')
parser.add_argument('inputfile', type=str,
                    help='Input file')
parser.add_argument('--namespace','-p',
                    help='Namespace (Java like)', required=True)
parser.add_argument('--name','-n',
                    help='Name', required=True)
parser.add_argument('--resultfield','-r',
                    help='Resultf ield, not nullable')

args = parser.parse_args()


filepath = args.inputfile
name = args.name
namespace = args.namespace


df = pd.read_csv(filepath)
if(args.resultfield is not None and args.resultfield not in df.columns ):
    print("Field not found!", file=sys.stderr)
    exit(1)
fields = [{"name":key, "type":(translationdict[str(val)] if args.resultfield==key else [translationdict[str(val)], "null"])} for key, val in df.dtypes.items()]
res = {"type":"record","name":name,"namespace":namespace, "fields":fields}
print(json.dumps(res, indent=4))