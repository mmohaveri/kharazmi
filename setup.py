#!/usr/bin/env python

import os
import subprocess


from setuptools import setup, find_packages


def run_setup():
    requirements = [
        "sly>=0.4",
    ]

    python_requirement = ">=3.6"

    with open('README.md', 'r') as f:
        long_description = f.read()

    setup(
        name='kharazmi',
        version=git_version(),

        author='Mahdi Mohaveri',
        author_email='mmohaveri@gmail.com',

        package_dir={'': 'src'},
        packages=find_packages('src'),
        package_data={
            'kharazmi': ['py.typed'],
        },
        include_package_data=True,

        license='MIT License',

        description='An equation parser/calculator module for python.',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/mmohaveri/kharazmi",

        install_requires=requirements,
        python_requires=python_requirement,

        zip_safe=True,
        keywords=[
            'development',
            'expression',
            'algebra',
            'equation'
        ],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Topic :: Software Development',
            'Topic :: Utilities',
            'Typing :: Typed'
        ],
    )


def git_version():
    git_commit_cmd = ['git', 'rev-parse', '--short', 'HEAD']
    git_version_cmd = ['git', 'describe', '--abbrev=1', '--tags']

    return _run_cmd(git_version_cmd) or _run_cmd(git_commit_cmd) or "Unknown"


def _run_cmd(cmd):
    cwd = os.path.abspath(os.path.dirname(__file__))

    env = {key: os.environ.get(key) for key in [
        'SYSTEMROOT', 'PATH', 'HOME'] if os.environ.get(key) is not None}
    env['LANGUAGE'] = 'C'
    env['LANG'] = 'C'
    env['LC_ALL'] = 'C'

    child = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env, cwd=cwd)
    output, err = child.communicate()

    if err is not None or child.returncode != 0:
        return None

    return output.strip().decode('ascii')


if __name__ == "__main__":
    run_setup()
