import argparse
import logging
import re
import pathlib
from pathlib import Path
import mimetypes
import csv
from datetime import datetime
#  mimetypes.init()

def parse_args():
    # validate and return paths for main directory and subdirs
    def main_dir(arg):
        path = Path(arg)
        if not path.is_dir():
            raise argparse.ArgumentTypeError(f"{path} is not a directory")
        return path

    def dir_of_dirs(arg):
        path = main_dir(arg)
        subdirs = []
        for child in path.iterdir():
            if child.is_dir():
                subdirs.append(child)
        return subdirs

    '''I suspect since we are using this script in 0_borndigitalstaging 
    then a single package as input is less important. May only need dir_of_dirs'''

    parser = argparse.ArgumentParser(description="takes package directory")
    # argument for single package to be validated
    parser.add_argument(
        "-p",
        "--package",
        type=main_dir,
        help="input path to an ami package",
        # required=True,
        dest="packages",
        action="append",
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=dir_of_dirs,
        help="input path to a directory of ami packages",
        # required=True,
        dest="packages",
        action="extend",
    )
    parser.add_argument(
        '-o', '--output',
        "-o",
        "--output",
        help="report destination directory",
        type=str,
        required=True
    )

    return parser.parse_args()

def get_name_bytes_count(source_dir: pathlib.Path) -> list[str, int, int]:

    #Loop through the packages in the given source dir
    '''for each package should we write package name, number of files and total bytes of package
    #to a dataframe for easy csv generation? --> answered'''
    #for package in source_dir.iterdir():
    if source_dir.is_dir():
        name = source_dir.name
        file_count = 0
        total_bytes = 0

        for item in source_dir.rglob("*"):
                if item.is_file():
                    file_count += 1
                    total_bytes += item.stat().st_size


    #print(name, file_count, total_bytes)
    # print(total_bytes)
    return name, file_count, total_bytes
    

'''get classmark and division'''
def get_metadata_from_title(source_dir: pathlib.Path) -> tuple[str, str]:
    name = source_dir.name
  
    '''key should be the classmark, value should division, in one to one relatiopnships'''
    codes = { "ncov": "theatre", "ncow":"theatre", "mgzdoh":"dance", "mgzidf": "dance"
    }
    division = "unknown" 
    for classmark, div in codes.items():
        if classmark in name:
            # print(f"the substring {classmark} is in {name}")
            division = div 
            break

    patterns = { "theatre": [r'.*(ncov\w+)', r'.*(ncow\w+)'],
     "dance": [r'.*(mgzdoh\w+)', r'.*(mgzidf\w+)'], "unknown": []
    }
    classmark = "unknown"
    for pattern in patterns[division]:
        match = re.search(pattern, name)
        if match:
            classmark = match.group(1) 
            break

    return division, classmark


#is this package_dir the directory of directories or an individual package?
def get_edit_file_count(source_dir: pathlib.Path) -> int:
    em_count = 0
    for item in source_dir.rglob("*"):
        #Check item is a file and not directory. Check "em" in filename.
        if item.is_file() and "_em" in item.name: #datatype is path here
            # this if statement might be doing too much, maybe we lowercase earlier?
            mime = mimetypes.guess_type(item)
            print(item.name, mime[0])
            '''This returns a tuple with (type, encoding), with type in the form /video/filetype'''
            if mime[0].startswith('video') or mime[0].startswith('audio'): #this could potentially match to our standard exactly with 'video/mp4'
                print(item.name)
                em_count += 1
    return em_count


#   return len([x for x in package_dir.rglob("*") if "_em." in x])
    #may need further check to see if file is a media file?
    #also a check to make sure it's a file first.

#is this how to type hint a list of lists with multiple data types to a csv output?
def write_report(alldata: list[list], dest) -> csv:
    now = datetime.now()
    dt = now.strftime("%Y-%m-%d")
    header = ['package_name', 'total_files', 'total_bytes_count', 'edit_file_count', 'division', 'classmark']
    
    with open(f'{dest}/editreport{dt}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(alldata)


def main():
    args = parse_args()
    dest = args.output
    all_data = []
    # args.packages is a [myd_720_dance, package2, package3...]
    for source in args.packages:
        # print(source)
         data = []
        # each function should get data about one package (myd_720_dance)
         data.extend(get_name_bytes_count(source))
         data.append(get_edit_file_count(source))
         
        
         data.extend(get_metadata_from_title(source))

        # add all the extracted data to ... something
         all_data.append(data)
    
    # print(all_data)
    write_report(all_data, dest)

if __name__ == "__main__":
    main()