import shutil
from pathlib import Path
from setuptools import setup, find_packages
from setuptools.dist import Distribution

class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True

# Find the built module from build/ directory
build_dir = Path(__file__).parent / "build"
module_files = list(build_dir.glob("_nigiri.cpython-*.so"))

if not module_files:
    raise FileNotFoundError(
        "Python module not found. Please build it first with:\n"
        "  mkdir -p build && cd build && cmake .. && cmake --build . --target _nigiri"
    )

module_file = module_files[0]

# Copy the .so file to the nigiri package directory
package_dir = Path(__file__).parent / "nigiri"
package_dir.mkdir(exist_ok=True)
shutil.copy2(module_file, package_dir / module_file.name)

setup(
    name="nigiri",
    version="0.1.0",
    description="Nigiri transit routing Python bindings",
    packages=find_packages(),
    package_data={
        "nigiri": [module_file.name],
    },
    include_package_data=True,
    distclass=BinaryDistribution,
    python_requires=">=3.11",
    zip_safe=False,
)
