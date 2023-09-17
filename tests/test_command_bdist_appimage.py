"""Tests for cx_Freeze.command.bdist_appimage."""
from __future__ import annotations

import platform
import sys
from pathlib import Path
from subprocess import check_output

import pytest
from setuptools import Distribution

from cx_Freeze.exception import PlatformError

if sys.platform == "linux":
    from cx_Freeze.command.bdist_appimage import (
        BdistAppImage as bdist_appimage,
    )

FIXTURE_DIR = Path(__file__).resolve().parent

DIST_ATTRS = {
    "name": "foo",
    "version": "0.0",
    "description": "cx_Freeze script to test bdist_appimage",
    "executables": [],
    "script_name": "setup.py",
}


@pytest.mark.skipif(sys.platform != "linux", reason="Linux tests")
def test_bdist_appimage_not_posix(monkeypatch):
    """Test the bdist_appimage fail if not on posix."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_appimage(dist)
    monkeypatch.setattr("os.name", "nt")
    with pytest.raises(PlatformError, match="don't know how to create App"):
        cmd.finalize_options()


@pytest.mark.skipif(sys.platform != "linux", reason="Linux tests")
def test_bdist_appimage_target_name():
    """Test the bdist_appimage with extra target_name option."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_appimage(dist)
    cmd.target_name = "mytest"
    cmd.finalize_options()
    cmd.ensure_finalized()
    assert cmd.fullname == "mytest-0.0"


@pytest.mark.skipif(sys.platform != "linux", reason="Linux tests")
def test_bdist_appimage_target_name_and_version():
    """Test the bdist_appimage with extra target options."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_appimage(dist)
    cmd.target_name = "mytest"
    cmd.target_version = "0.1"
    cmd.finalize_options()
    cmd.ensure_finalized()
    assert cmd.fullname == "mytest-0.1"


@pytest.mark.skipif(sys.platform != "linux", reason="Linux tests")
@pytest.mark.datafiles(FIXTURE_DIR.parent / "samples" / "icon")
def test_bdist_appimage_target_name_with_extension(datafiles: Path):
    """Test the icon sample, with a specified target_name that includes an
    ".AppImage" extension.
    """
    name = "output.AppImage"
    output = check_output(
        [sys.executable, "setup.py", "bdist_appimage", "--target-name", name],
        text=True,
        cwd=datafiles,
    )
    print(output)
    file_created = datafiles / "dist" / name
    assert file_created.is_file()


@pytest.mark.skipif(sys.platform != "linux", reason="Linux tests")
@pytest.mark.datafiles(FIXTURE_DIR.parent / "samples" / "icon")
def test_bdist_appimage_skip_build(datafiles: Path):
    """Test the icon sample with bdist_appimage."""
    name = "Icon sample"
    version = "0.4"
    arch = platform.machine()
    output = check_output(
        [sys.executable, "setup.py", "build_exe"], text=True, cwd=datafiles
    )
    print(output)
    output = check_output(
        [sys.executable, "setup.py", "bdist_appimage", "--skip-build"],
        text=True,
        cwd=datafiles,
    )
    print(output)

    file_created = datafiles / "dist" / f"{name}-{version}-{arch}.AppImage"
    assert file_created.is_file(), f"{name}-{version}-{arch}.AppImage"


@pytest.mark.skipif(sys.platform != "linux", reason="Linux tests")
@pytest.mark.datafiles(FIXTURE_DIR.parent / "samples" / "simple")
def test_bdist_appimage_simple(datafiles: Path):
    """Test the simple sample with bdist_appimage."""
    name = "hello"
    version = "0.1.2.3"
    arch = platform.machine()

    output = check_output(
        [sys.executable, "setup.py", "bdist_appimage", "--quiet"],
        text=True,
        cwd=datafiles,
    )
    print(output)

    file_created = datafiles / "dist" / f"{name}-{version}-{arch}.AppImage"
    assert file_created.is_file(), f"{name}-{version}-{arch}.AppImage"
