import bd_validator as bv
import pytest
from pathlib import Path

@pytest.fixture
def good_package():
    return Path("fixtures/simple_video_pk")

def test_is_package_bag(good_package):
    result = bv.is_valid_bag(good_package)
    assert result is True

def test_expected_folders_present(good_package):
    #a list of approved directory names for package structure
    expected = ['ArchiveOriginals', 'EditMasters','ServiceCopies','Images','Transcripts','Captions','Releases'] 
    #the subdirectories present in the source package
    present = bv.get_structure(good_package)

    #compare present list to expected
    for item in present:
        assert item.name in expected

    #notes: compensating for incorrect spelling, is the function to hard coded?

# def test_expected_folders_match_package_contents(good_package):
    present = bv.get_structure(good_package)
    filetypes = {'ao':'ArchiveOriginals', 'em':'EditMasters','sc':'ServiceCopies','Images','Transcripts','Captions','Releases'}

# def arguments_capture_valid_package_path(good_package)

#def arguments_capture_valid_directory_paths(good_package)
