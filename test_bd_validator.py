import bd_validator as bv
import pytest
from pathlib import Path

@pytest.fixture
def good_package():
    return Path("fixtures/simple_video_pk")

@pytest.fixture
def good_structure(good_package):
    return bv.get_structure(good_package)

def test_is_package_bag(good_package):
    result = bv.is_valid_bag(good_package)
    assert result is True

def test_expected_folders_present(good_structure):
    result = bv.valid_structure(good_structure)
    assert result

def test_warning_unexpected_folder(good_structure):
    good_structure.append(Path('unknown_folder')) #not sure if this is correct
    result = bv.valid_structure(good_structure)
    assert not result

def test_required_folders_present(good_structure):
    # do we have these?
    assert False


def test_warn_on_required_folders_missing(good_structure):
    # do we have these?
    assert False

    


# def test_expected_folders_match_package_contents(good_package):
#   present = bv.get_structure(good_package) 
    assert result
#   filetypes = {'ArchiveOriginals':'ao', 'EditMasters':'em','ServiceCopies':'sc','Images':['.jpg','.JPEG','.tif','.tiff'],'Transcripts':['.pdf'],'Captions','Releases', 'Project Files'}

#@pytest.parametrize(filetypes)
# def test_warn_on_folder_file_mismatch(good_package, filetypes):
    # corrupt one folder at a time and get the right warning message

# def arguments_capture_valid_package_path(good_package)

#def arguments_capture_valid_directory_paths(good_package)
