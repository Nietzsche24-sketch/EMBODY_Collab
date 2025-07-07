#!/usr/bin/env python

import os
import sys
from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
from distutils.version import LooseVersion
import numpy

# Validate Python version
if LooseVersion(sys.version) < LooseVersion("3.6") or LooseVersion(sys.version) >= LooseVersion("3.9"):
    raise RuntimeError(f"TTS requires Python >=3.6 and <3.9, but your version is {sys.version}")

# Load version
version = "0.0.10.3"

# Load requirements and filter numpy to control version manually
cwd = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(cwd, "requirements.txt"), "r") as f:
    raw_requirements = f.readlines()
requirements = [r.strip() for r in raw_requirements if not r.strip().startswith("numpy")]

# Load long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Define Cython extension
extensions = [
    Extension(
        name="TTS.tts.layers.glow_tts.monotonic_align.core",
        sources=["TTS/tts/layers/glow_tts/monotonic_align/core.pyx"]
    )
]

setup(
    name="TTS",
    version=version,
    author="Eren Gölge",
    author_email="egolge@coqui.ai",
    description="Deep learning for Text to Speech by Coqui",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coqui-ai/TTS",
    license="MPL-2.0",
    packages=find_packages(include=["TTS*"]),
    include_package_data=True,
    ext_modules=cythonize(extensions, language_level=3),
    include_dirs=[numpy.get_include()],
    install_requires=requirements + ["numpy==1.22.4"],
    python_requires=">=3.6, <3.9",
    entry_points={
        "console_scripts": [
            "tts=TTS.bin.synthesize:main",
            "tts-server=TTS.server.server:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    zip_safe=False
)
