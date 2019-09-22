import setuptools
import unittest

with open("readme.md", "r") as fh:
	long_description = fh.read()

def get_test_suite():
	test_loader = unittest.TestLoader()
	test_suite = test_loader.discover('.', pattern='test_*.py')
	return test_suite


if __name__ == '__main__':
	setuptools.setup(
		name="syspy",
		version="0.0.48",
		author="Matthew Garelli",
		author_email="mgarelli@alumni.stanford.edu",
		description="A module to do certain unix system tasks",
		long_description=long_description,
		long_description_content_type="text/markdown",
		packages=setuptools.find_packages(),
		test_suite='setup.get_test_suite',
		classifiers=[
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: Unix",
		],
	)
