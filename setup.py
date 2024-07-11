import os
import sys
import re
import platform
from setuptools import find_packages, setup

project_name = "deeplake"

this_directory = os.path.abspath(os.path.dirname(__file__))

def read_requirements(file):
    with open(os.path.join(this_directory, file)) as f:
        return [line.strip() for line in f if line.strip()]

requirements = read_requirements("deeplake/requirements/common.txt")
tests = read_requirements("deeplake/requirements/tests.txt")

with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

req_map = {}
for req in requirements:
    match = re.match(r"^(([^!=<>~]+)(?:[!=<>~].*)?)$", req)
    if match:
        req_map[match.group(2)] = match.group(1)

extras = {
    "audio": ["av"],
    "video": ["av"],
    "av": ["av"],
    "gcp": ["google-cloud-storage", "google-auth", "google-auth-oauthlib"],
    "azure": ["azure-cli", "azure-identity", "azure-storage-blob"],
    "dicom": ["pydicom", "nibabel"],
    "medical": ["pydicom", "nibabel"],
    "visualizer": ["IPython", "flask"],
    "gdrive": [
        "google-api-python-client",
        "oauth2client",
        "google-auth",
        "google-auth-oauthlib",
    ],
    "point_cloud": ["laspy"],
}

def libdeeplake_available():
    py_ver = sys.version_info
    if sys.platform == "linux":
        if py_ver >= (3, 6) and py_ver <= (3, 12):
            return True
    if sys.platform == "darwin":
        mac_ver = list(map(int, platform.mac_ver()[0].split(".")))
        if (
            (mac_ver[0] > 10 or mac_ver[0] == 10 and mac_ver[1] >= 12)
            and py_ver >= (3, 7)
            and py_ver < (3, 12)
        ):
            return True
    return False

all_extras = {r for v in extras.values() for r in v}
install_requires = [req_map[r] for r in req_map if r not in all_extras]
extras_require = {k: [req_map.get(r, r) for r in v] for k, v in extras.items()}

extras_require["all"] = [req_map.get(r, r) for r in all_extras]

if libdeeplake_available():
    libdeeplake = "libdeeplake==0.0.119"
    extras_require["enterprise"] = [libdeeplake, "pyjwt"]
    extras_require["all"].append(libdeeplake)
    install_requires.append(libdeeplake)

init_file = os.path.join(project_name, "__init__.py")

def get_property(prop):
    result = re.search(
        rf'{prop}\s*=\s*[\'"]([^\'"]*)[\'"]',
        open(init_file).read(),
    )
    return result.group(1)

config = {
    "name": project_name,
    "version": get_property("__version__"),
    "description": "Activeloop Deep Lake",
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
    "author": "activeloop.ai",
    "author_email": "support@activeloop.ai",
    "packages": find_packages(),
    "install_requires": install_requires,
    "extras_require": extras_require,
    "tests_require": tests,
    "include_package_data": True,
    "zip_safe": False,
    "entry_points": {},
    "dependency_links": [],
    "project_urls": {
        "Documentation": "https://docs.activeloop.ai/",
        "Source": "https://github.com/activeloopai/deeplake",
    },
    "license": "MPL-2.0",
    "classifiers": [
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
    ],
}

setup(**config)
