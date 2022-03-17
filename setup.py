from setuptools import setup, find_packages

desc = "Mass DHCP Client Emulator"

with open('requirements.txt', 'r') as f:
    requires = [x.strip() for x in f if x.strip() and not x.startswith('--')]

print(requires)

setup(
    name='massdhclient',
    version="0.0.1",
    author="Steffen Schumacher",
    author_email="ssch@wheel.dk",
    description=desc,
    long_description=desc,
    long_description_content_type="text/markdown",
    url="https://github.com/steffenschumacher/massdhclient/",
    packages=find_packages(),
    scripts=["massdhclient.py"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    include_package_data=True,
    install_requires=requires,
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
