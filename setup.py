from setuptools import setup, find_packages

setup(
	name='friar',
	version='0.0.1',
	description='A data toolkit for working with betting markets',
	long_description='A data toolkit for working with betting markets',
	url='http://friar.jameselford.com',
	author='James Elford',
	author_email='james.p.elford@gmail.com',
	license='MIT',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Programming Language :: Python :: 3.4',
	],
	keywords='data betfair',

	packages=find_packages(exclude=['test*']),
	install_requires=['requests'],
	tests_require=[],
)

	
