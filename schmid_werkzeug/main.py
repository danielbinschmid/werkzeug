import argparse
from .ml_eval import evaluate_json


def print_help():
    print("hello world")


def main():
    parser = argparse.ArgumentParser(description="My command line tool")
    parser.add_argument("mode", help="Execution mode")
    parser.add_argument("sub_mode", help="submode")
    parser.add_argument("arg1", help="first arg")
    args = parser.parse_args()

    mode = args.mode
    sub_mode = args.sub_mode
    arg1 = args.arg1

    if args.mode == "ml_eval":
        if args.sub_mode == "extract_json":
            evaluate_json(arg1)
        else:
            print_help()
    else:
        print_help()
