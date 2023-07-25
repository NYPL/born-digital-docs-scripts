import pathlib
from pathlib import Path
import bagit 
import argparse


def args():
    parser = argparse.ArgumentParser(
        description="takes package directory"
    )
    parser.add_argument(
        '-s', '--source',
        type=str,
        help='input path to an ami package, as string with double quotes',
        required=True,
        action='store'
    )

    args=parser.parse_args()
    return args

def is_valid_bag(source: pathlib.Path) -> bool:
    bag = bagit.Bag(str(source))
    return bag.validate()

def get_structure(source: pathlib.Path) -> list:
    contents = []
    other = []
    for dir in Path(source).iterdir():
        if dir.is_dir() and dir.name == 'data':
            for subdir in Path(dir).iterdir():
                contents.append(subdir)

        else:
            other.append(dir.name)
    
    print(contents)
    print(f'the following files are on the first level: {other}')
    return contents

def main():
    source = args().source
    get_structure(source)


if __name__ == '__main__':
    main()