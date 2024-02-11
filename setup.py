from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='LLM-Curriculum',
    version='0.1.0',
    description='LLM Curriculum Learning for Reinforcement Learning.',
    author='Logan',
    author_email='locross93@gmail.com',  # Replace with your email
    url='https://github.com/sunfanyunn/LLM-Curriculum',  # Replace with your repository URL
    packages=find_packages(),
    install_requires=required,
    entry_points={
        'console_scripts': [
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)