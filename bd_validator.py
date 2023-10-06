import pathlib
from pathlib import Path
import bagit 
import argparse
import logging
import re


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
    
    #print(contents)
    #print(f'the following files are on the first level: {meta}')
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
    files_dict = []
    for file in all_files:
        dict ={'name':file.name,
            'strpath':file.absolute(),
            'pospath':file}
        files_dict.append(dict)           
    # print(test)
    return files_dict

#check to see the expected folders are in package based on file extension
def validate_folder_content_types(files_dict):
    types = {"_ao":"ArchiveOriginals",
             "_em":"EditMasters",
             "_sc":"ServiceCopies",
             "_pm":"PreservationMasters"}

    # dict ={'name': file.name,
    #         'path':file}

    inspect =[]

    # for item in files_dict:
    #     for key in types:
    #         if re.search(key, files_dict['name']):
    #             print(f'{files_dict["name"]} is {types[key]}')

    for item in files_dict:
        for key in types:
            if re.search(key, item['name']) and re.search(types[key], item['strpath']):
                print(f'{item["name"]} is in {types[key]} as expected')
            else:
                inspect.append(item)
    
    # for item in inspect:
    #     print(f'what is this?: {item}')

#if this works, try with not and result = true/false as written below
    # result = True
    # for item in contents:
    #     if not item.name in expected:
    #         result = False
            
    # return result

# #check to see files are in appropriate folders:
# def validate_folders_file_match():
#     return True

def main():
    args = parse_args()
    print(args)
    #for loop for accessing namespace list of one or more
    for source in args.packages:
        folders = get_structure(source)
        files  = get_files(source)
        validate_folder_content_types(files)


if __name__ == '__main__':
    main()