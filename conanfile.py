from conan import ConanFile
from conan.errors import ConanException
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, cmake_layout, CMakeToolchain
from conan.tools.scm import Git
import os


class PBNIFrameworkRecipe(ConanFile):
    name = "lib.cpp.base.pbni-framework"
    package_type = "static-library"

    license = "MIT"
    author = "micha.wehrli@informaticon.com"
    url = "https://github.com/informaticon/lib.cpp.base.pbni-framework"
    description = "Framework for creating PowerBuilder Extensions using PBNI"

    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "CMakeLists.txt", "src/**"

    options = { "pb_version": ["ANY"] }

    generators = "CMakeDeps", "CMakeToolchain"

    def requirements(self):
        self.requires("boost/1.85.0", transitive_headers=True)

    def validate(self):
        if self.settings.compiler.cppstd:
            check_min_cppstd(self, 20)

    def set_version(self):
        if not self.version:
            try:
                git = Git(self)
                tag = git.run("describe --tags")
                self.version = tag.lstrip('v')
            except ConanException:
                self.version = "0.0.0-trunk"

    def layout(self):
        cmake_layout(self)

    def build(self):
        pbni_dir = f"C:/Program Files (x86)/Appeon/PowerBuilder {self.options.pb_version}/SDK/PBNI/"
        assert os.path.exists(pbni_dir)

        cmake = CMake(self)
        cmake.configure({ "PBNI_SDK_DIRECTORY": pbni_dir })
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
    
    def package_info(self):
        self.cpp_info.objects = [f"lib/objects-{self.settings.build_type}/lib.cpp.base.pbni-framework/*.obj"]
        self.cpp_info.defines = ["UNICODE", "_UNICODE", "WIN32_LEAN_AND_MEAN", "NOMINMAX"]
        if self.settings.compiler == "msvc":
            self.cpp_info.cxxflags = ["/Zc:preprocessor"]

