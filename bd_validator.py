import pathlib
from pathlib import Path
import bagit 
import argparse
import logging


def args():
    #validate and return paths for main directory and subdirs
    def main_dir(arg):
        path = Path(arg)
        if not path.is_dir():
            raise argparse.ArgumentTypeError(
                f'{path} is not a directory'
            )
        return path
    
    def dir_of_dirs(arg):
        path = main_dir(arg)
        subdirs = []
        for child in path.iterdir():
            if child.is_dir():
                subdirs.append(child)
        return subdirs
    
    parser = argparse.ArgumentParser(
        description="takes package directory"
    )
    #argument for single package to be validated 
    parser.add_argument(
        '-p', '--package',
        type=main_dir,
        help='input path to an ami package, as string with double quotes',
        #required=True,
        nargs='+',
        action='store'
    )
    parser.add_argument(
        '-d', '--directory',
        type=dir_of_dirs,
        help='input path to an ami package, as string with double quotes',
        #required=True,
        action='store'
    )

    args=parser.parse_args()
    return args

def is_valid_bag(package: pathlib.Path) -> bool:
    bag = bagit.Bag(str(package))
    return bag.validate()

#get structure would have to change to incorporate a list of packages
def get_structure(package: pathlib.Path) -> list:
    contents = []
    meta = []
    for item in Path(package).iterdir():
        if item.is_dir() and item.name == 'data':
            for subdir in Path(item).iterdir():
                contents.append(subdir)

        else:
            meta.append(item.name)
    
    print(contents)
    print(f'the following files are on the first level: {meta}')
    return contents

def main():
    source = args().package
    get_structure(source)


if __name__ == '__main__':
    main()