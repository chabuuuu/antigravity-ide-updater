from setuptools import setup, find_packages

setup(
    name="antigravity-ide-updater",
    version="1.0.0",
    author="Ha Phu Thinh",
    author_email="haphuthinh332004@gmail.com",
    description="Cross-platform auto-updater for Google Antigravity IDE (Linux & Windows) with zero data loss guarantee.",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "antigravity-ide-updater=src.__main__:main",
        ],
    },
    python_requires=">=3.8",
)
