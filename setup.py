from setuptools import setup, find_packages

setup(
    name="jama-abstract-mcp",
    version="1.0.0",
    description="JAMA tıp dergisi makalelerinden abstract görselleri oluşturmak için MCP servisi",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "mcp>=1.0.0",
        "selenium>=4.15.0",
        "beautifulsoup4>=4.12.0",
        "requests>=2.31.0",
        "Pillow>=10.1.0",
        "opencv-python>=4.8.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "pandas>=2.1.0",
        "aiohttp>=3.9.0",
        "typing-extensions>=4.8.0",
        "webdriver-manager>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ]
    },
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "jama-abstract-mcp=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)