from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="gemini-http-server",
    version="1.0.0",
    author="Kenneth Joroge",
    author_email="your-email@example.com",
    description="A lightweight, security-focused HTTP server with React frontend integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/gemini-http-server",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "gemini-server=gemini_server.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "gemini_server": ["templates/*.html"],
    },
)