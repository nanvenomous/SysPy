import setuptools

with open("readme.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="syspy",
	version="0.0.52",
	author="Matthew Garelli",
	author_email="mgarelli@alumni.stanford.edu",
	description="A module to do certain unix system tasks",
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: Unix",
	],
)
