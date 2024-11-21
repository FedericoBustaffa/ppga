import sequential
import parallel

import sys


def main(argv: list[str]) -> None:
    sequential.main(argv)
    parallel.main(argv)


if __name__ == "__main__":
    main(sys.argv)
