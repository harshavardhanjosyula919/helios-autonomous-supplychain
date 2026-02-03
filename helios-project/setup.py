from setuptools import setup, find_packages

setup(
    name="helios-sc",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Autonomous Supply Chain Optimization Engine",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scipy>=1.10.0",
        "pyomo>=6.6.0",
        "gymnasium>=0.28.0",
        "torch>=2.0.0",
        "fastapi>=0.100.0",
    ],
)
