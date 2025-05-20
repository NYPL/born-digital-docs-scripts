from pathlib import Path

import pytest

import born_digital_docs_scripts.lint_bdami as bd


@pytest.fixture
def good_package(tm_path: Path):
    pkg = tmp_path.joinpath("fixtures/simple_bdami_pk")
    #pkg = tmp_path.joinpath("fixtures/ncov1234")

    ao_folder = pkg.joinpath("data/ArchiveOriginals")
    ao_folder.mkdir(parents=True)
    #here add a fake video but also a folder with a couple levels

    em_folder = pkg.joinpath("data/EditMasters")
    em_folder.mkdir(parents=True)

    sc_folder = pkg.joinpath("data/ServiceCopies")
    sc_folder.mkdir(parents=True)
    

    ao_filepath = ao_folder.joinpath("myd_mgzidf123456_v01_ao.mp4")
    ao_folderpath = ao_folder.joinpath("/myd_mgzidf123456_v01_ao/CLIPS")
    ao_mxf = ao_folderpath.joinpath("myd_mgzidf123456_v01_ao.mp4")
    ao_xml = ao_folderpath.joinpath("myd_mgzidf123456_v01_ao.xml")
    ao_bpav = 


    em_filepath = em_folder.joinpath("myd_mgzidf123456_v01_em.mov")
    sc_filepath = sc_folder.joinpath("myd_mgzidf123456_v01_sc.mp4")

    for file in [
        ao_filepath,
        em_filepath,
        sc_filepath,
        (pkg/"bagit.txt"),
        (pkg/"manifest-md5.txt")
    ]

    return pkg


@pytest.fixture
def good_structure(good_package):
    return bd.get_structure(good_package)


def test_is_package_bag(good_package):
    result = bd.is_valid_bag(good_package)
    assert result is True


def test_expected_folders_present(good_structure):
    result = bd.valid_structure(good_structure)
    assert result


def test_warning_unexpected_folder(good_structure):
    good_structure.append(Path("unknown_folder"))  # not sure if this is correct
    result = bd.valid_structure(good_structure)
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

# @pytest.parametrize(filetypes)
# def test_warn_on_folder_file_mismatch(good_package, filetypes):
# corrupt one folder at a time and get the right warning message

# def arguments_capture_valid_package_path(good_package)

# def arguments_capture_valid_directory_paths(good_package)
