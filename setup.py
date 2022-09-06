import setuptools

with open("README.md") as f:
	long_description = f.read()

setuptools.setup(
	name = "lzstr",
	packages = setuptools.find_packages(),
	version = "0.0.2",
	license = "gpl-3.0",
	description = "Native Python implementation of LZString string compression",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	author = "Johannes Bauer",
	author_email = "joe@johannes-bauer.com",
	url = "https://github.com/johndoe31415/pylzstring",
	download_url = "https://github.com/johndoe31415/pylzstring/archive/v0.0.2.tar.gz",
	keywords = [ "python", "lzstring" ],
	classifiers = [
		"Development Status :: 3 - Alpha",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3 :: Only",
		"Programming Language :: Python :: 3.10",
	],
)
