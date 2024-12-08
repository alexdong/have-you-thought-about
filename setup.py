from setuptools import setup, find_packages

setup(
    name="consilio",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'anthropic>=0.8.0',
        'better-exceptions>=0.3.3',
        'prompt-toolkit>=3.0.0',
        'PyYAML>=6.0.1',
        'Jinja2>=3.1.0',
    ],
)
