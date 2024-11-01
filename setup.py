from setuptools import setup, find_packages

setup(
    name="flash_detector",
    version="1.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "opencv-python>=4.5.0",
        "numpy>=1.19.0",
        "gradio>=3.0.0",
        "psutil>=5.8.0",
    ],
)
