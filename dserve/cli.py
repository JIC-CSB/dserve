import os
import argparse

from dtoolcore import DataSet

from dserve import app


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-d", "--dataset_path",
        default=os.environ.get("DSERVE_DATASET_PATH", None))
    parser.add_argument("-p", "--port", type=int, default=5000)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.dataset_path is None:
        parser.error("Please specify a dataset path")
    dataset = DataSet.from_path(args.dataset_path)
    app._dataset = dataset
    app.run(port=args.port, debug=args.debug, host="0.0.0.0")


if __name__ == '__main__':
    main()
