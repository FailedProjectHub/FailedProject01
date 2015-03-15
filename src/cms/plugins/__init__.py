__all__ = [
    'cd',
    'ls',
    'mkdir',
    'rm',
    'chmod',
    'chown',
    'touch',
    'lna',
    'mv'
]


from . import *

Register = base.basepluginMetaclass.Register


def print_docs():
    for k, v in Register.items():
        print(k)
        v.parser.print_help()
