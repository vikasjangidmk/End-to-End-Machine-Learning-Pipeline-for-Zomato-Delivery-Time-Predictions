from setuptools import setup, find_packages
from typing import List

PROJECT_NAME = "Machine Learning Project"
VERSION = "0.0.1"
DESCRIPTION = "This is our machine learning project in modular coding"
AUTHOR_NAME = "Vikas Jangid"
AUTHOR_EMAIL = "vikasjangidmk@gmail.com"

REQUIREMENTS_FILE_NAME = "requirements.txt"

HYPHEN_E_DOT = "-e ."
# requirements.txt file open and 
# read
# \n ""
def get_requirements_list() -> List[str]:
    with open(REQUIREMENTS_FILE_NAME) as requirements_file:
        requirement_list = requirements_file.readlines()
        # Removing newline characters from each requirement name
        requirement_list = [requirements_name.replace("\n", "") for requirements_name in requirement_list]
        
        if HYPHEN_E_DOT in requirement_list:
            requirement_list.remove(HYPHEN_E_DOT)
    return requirement_list

setup(
    name=PROJECT_NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(),  # call src/__init__.py
    install_requires=get_requirements_list()  # Corrected parameter name
)
