#!/usr/bin/env python3

import yaml
import sys
from pprint import pprint
import json

def data_merge(a, b):
    """merges b into a and return merged result

    NOTE: tuples and arbitrary objects are not handled as it is totally ambiguous what should happen"""

    key = None
    try:
        if a is None or isinstance(a, str) or isinstance(a, bool) or isinstance(a, int):
            a = b
        elif isinstance(a, list):
            if isinstance(b, list):
                a.extend(b)
            else:
                a.append(b)
        elif isinstance(a, dict):
            if isinstance(b, dict):
                for key in b:
                    if key in a:
                        a[key] = data_merge(a[key], b[key])
                    else:
                        a[key] = b[key]
            else:
                raise YamlReaderError('Cannot merge non-dict "%s" into dict "%s"' % (b, a))
        else:
            raise YamlReaderError('NOT IMPLEMENTED "%s" into "%s"' % (b, a))
    except TypeError as e:
        raise YamlReaderError('TypeError "%s" in key "%s" when merging "%s" into "%s"' % (e, key, b, a))
    return a

def pretty_print(uglies):
    print('\n---\n'.join([ yaml.dump(uglies[doc]) for doc in uglies ]))

manifests = {}

def main():
    for I in sys.argv[1:]:
        docs = yaml.safe_load_all(open(I, 'r'))
        for doc in docs:
            try:
                name = doc['metadata']['name']
            except:
                print(f'Error parsing doc from {I}', file=sys.stderr)
            if name not in manifests:
                manifests[name] = {}
            data_merge(manifests[name], doc)
    pretty_print(manifests)
         

if __name__ == '__main__':
  main()
