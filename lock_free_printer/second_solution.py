import time
import argparse

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", default=1.0)
    parser.add_argument("-t", default='Hello')
    return parser

parser = create_parser()
namespace = parser.parse_args()

print(namespace.s, namespace.t)

time.sleep(float(namespace.s))
print(namespace.t)