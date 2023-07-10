# It allows you to define the project's metadata, manage dependencies, and customize the distribution, making it easier for others to install and use your code.
from typing import List
from setuptools import find_packages, setup

E_DOT='-e .'

def get_requirements(file_path:str)->List[str]:
    requirements=[]
    with open(file_path) as file_ptr:
        requirements=file_ptr.readlines()
        requirements=[req.replace('\n', '') for req in requirements]

        if E_DOT in requirements:
            requirements.remove(E_DOT)
            
        return requirements

setup(
    name='WhatsappChatAnalyser',
    version='0.0.1',
    author='Ankit Rajput',
    author_email='rajputankit72106@gmail.com',
    install_requires=get_requirements('requirements.txt'),
    packages=find_packages()  #automatically finds all the packages to include in the distribution based on the project structure.
)