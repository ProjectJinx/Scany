from setuptools import setup, find_packages

setup(
    # long_description_content_type="text/markdown",
    # long_description=open("readme.md", "r").read(),
    name="Scany",
    version="0.1",
    # description="",
    # author="",
    # author_email="",
    # url="",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    # keywords="",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'Scany = Scany.__main__:main'
        ]
    },
    install_requires=["flask", "werkzeug", "scapy", "dataset"]
)
