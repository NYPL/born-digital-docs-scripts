import pathlib
from pathlib import Path
import bagit 
import argparse
import logging


def parse_args():
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
        help='input path to an ami package',
        #required=True,
        dest='packages',
        action='append'
    )
    parser.add_argument(
        '-d', '--directory',
        type=dir_of_dirs,
        help='input path to a directory of ami packages',
        #required=True,
        dest='packages',
        action='extend'
    )

    return parser.parse_args()

def is_valid_bag(package: pathlib.Path) -> bool:
    bag = bagit.Bag(str(package))
    return bag.validate()

#get structure would have to change to incorporate a list of packages
def get_structure(package: pathlib.Path) -> list:
    contents = []
    meta = []
    for item in package.iterdir():
        if item.is_dir() and item.name == 'data':
            for subdir in Path(item).iterdir():
                contents.append(subdir)

        else:
            meta.append(item.name)
    
    print(contents)
    print(f'the following files are on the first level: {meta}')
    return contents
    

def valid_structure(contents: list[Path]) -> bool:
    expected = ['ArchiveOriginals', 
                'EditMasters',
                'ServiceCopies',
                'Images',
                'Transcripts',
                'Captions',
                'Releases', 
                'Project Files']
    
    result = True
    for item in contents:
        if not item.name in expected:
            result = False

    return result


def get_files(package: pathlib.Path) -> list:
    all_items = Path(package).rglob("*")
    all_files = [x for x in all_items if x.is_file()]            
    print(all_files)
    return all_files

#check to see the expected folders are in package based on file extension
def validate_approriate_folders():
    return True

#check to see files are in appropriate folders:
def validate_folders_file_match():
    return True

def main():
    args = parse_args()
    print(args)
    for source in args.packages:
        print(source)
        folders = get_structure(source)
        all_files  = get_files(source)


if __name__ == '__main__':
    main()