import os
import gdown
from importlib.machinery import SourceFileLoader
from setuptools import setup, find_packages

version = SourceFileLoader('doas.version', os.path.join('doas', 'version.py')).load_module()
core = SourceFileLoader('doas.core', os.path.join('doas', 'core.py')).load_module()

print("Downloading punctuator model.")
punctuator_model_url = 'https://drive.google.com/uc?id=0B7BsN5f2F1fZd1Q0aXlrUDhDbnM'
punctuator_model_output_path = core.PUNCTUATOR_MODEL_PATH
gdown.download(punctuator_model_url, punctuator_model_output_path, quiet=False)

setup(
    name='dayone-audio-summarizer',
    version=version.version,
    description='Generating summarizations of DayOne audio journals in Markdown format',
    author='Jason Cramer',
    author_email='jason.t.cramer@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['doas=doas.cli:main'],
    },
    install_requires=[
        'gensim==3.8.3',
        'punctuator==0.9.5',
        'gdown==3.12.0',
    ],
    package_data={
        'doas': [punctuator_model_output_path]
    },
)