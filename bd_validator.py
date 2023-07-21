import pathlib
import bagit 

def is_valid_bag(source: pathlib.Path) -> bool:
    bag = bagit.Bag(str(source))
    return bag.validate()