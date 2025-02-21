from conan import ConanFile
from conan.errors import ConanException
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.build import can_run
import os


class PBNIFrameworkTest(ConanFile):
    package_type = "static-library"

    requires = ["boost/1.85.0"]
    settings = "os", "compiler", "build_type", "arch"

    options = { "pb_version": ["ANY"] }
    generators = "CMakeDeps", "CMakeToolchain"

    def validate(self):
        if self.settings.compiler.cppstd:
            check_min_cppstd(self, 20)

    def build(self):
        pbni_dir = f"C:/Program Files (x86)/Appeon/PowerBuilder {self.options.pb_version}/SDK/PBNI/"
        assert os.path.exists(pbni_dir)

        cmake = CMake(self)
        cmake.configure({ "PBNI_SDK_DIRECTORY": pbni_dir })
        cmake.build(target="install")

    def layout(self):
        cmake_layout(self)