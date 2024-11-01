from setuptools import setup, find_packages

setup(
    name="flash_detector",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "opencv-python>=4.5.0",
        "numpy>=1.19.0",
        "gradio>=3.0.0",
        "psutil>=5.8.0",
    ],
    author="Your Name",
    author_email="your@email.com",
    description="A tool for detecting flash sequences in videos",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/flash_detector",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
