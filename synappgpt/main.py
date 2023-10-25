from argparse import ArgumentParser

from module import load_data
from module import answer

parser = ArgumentParser()
parser.add_argument('--query',  type=str, help='Write a query to answer')
parser.add_argument('--update',  type=str, help='"True" if you want to update data.')
args = parser.parse_args()
if args.query:
    response = answer(args.query)
    print(response)
if args.update == 'True':
    load_data()
