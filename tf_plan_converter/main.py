import argparse
import logging
import sys
from tfplanconverter.plan import Plan

logging.basicConfig(level=logging.INFO)
from tfplanconverter.converter import Converter
from pathlib import Path


def parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("--plan", type=str, required=True)
    parser.add_argument(
        "--template",
        type=str,
        required=False,
        default="../templates/templateText.txt.j2",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=False,
        default="txt",
    )
    ## if "yes" it will check if there are only changes in the plan and return true
    parser.add_argument(
        "--checkmode",
        required=False,
        type=str,
        default="no",
    )
    return parser.parse_args()


def main():
    try:
        args = parser()
        plan = Plan()
        plan.jsonload(args.plan)
        dictionary = plan.extractDictionary(args.checkmode)
        c = Converter()
        if args.output == "txt":
            print(Path(c.convertTxt(dictionary, args.template)).read_text())
        else:
            print(Path(c.convertHtml(dictionary, args.template)).read_text())

    except Exception as e:
        logging.exception(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
