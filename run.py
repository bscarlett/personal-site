from console import parse_arguments


if __name__ == '__main__':
    arguments = parse_arguments()
    arguments.function(**vars(arguments))
