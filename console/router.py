from argparse import ArgumentParser
from console import load_from_file
from console import navigation_move
from console import serve


def parse_arguments():
    argument_parser = ArgumentParser()
    subparsers = argument_parser.add_subparsers()

    serve_argument_parser = subparsers.add_parser('serve')
    serve_argument_parser.set_defaults(function=serve)

    load_argument_parser = subparsers.add_parser('load')
    load_argument_parser.add_argument('--content-filename')
    load_argument_parser.add_argument('--title')
    load_argument_parser.add_argument('--route')
    load_argument_parser.add_argument('--show-in-navigation', action='store_true', default=False)
    load_argument_parser.add_argument('--short-description')
    load_argument_parser.set_defaults(function=load_from_file)
    nav_move_argument_parser = subparsers.add_parser('move')

    nav_move_argument_parser.add_argument('--route')
    nav_move_argument_parser.add_argument('--order', type=int)
    nav_move_argument_parser.set_defaults(function=navigation_move)

    return argument_parser.parse_args()