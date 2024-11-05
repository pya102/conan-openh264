from conan import ConanFile
from conan.tools.files import get, copy, rmdir
from conan.tools.env import VirtualBuildEnv
import os

class OpenH264Conan(ConanFile):
    name = "openh264"
    version = "2.4.1"
    license = "BSD-2-Clause"
    url = "https://github.com/cisco/openh264"
    description = "OpenH264 is a codec library for encoding and decoding H.264 video streams."
    settings = "os", "arch", "compiler", "build_type"
    exports_sources = "CMakeLists.txt"
    package_type = "shared-library"
    build_policy = "missing"

    def build_requirements(self):
        self.tool_requires("make/4.3")  # Adjust the version if needed

    def generate(self):
        # Create a virtual build environment
        env = VirtualBuildEnv(self)
        env.generate()

    def source(self):
        get(self, f"https://github.com/cisco/openh264/archive/refs/tags/v{self.version}.tar.gz",
            strip_root=True)

    def build(self):
        # Compile openh264 with make
        self.run(f"make ARCH={self.settings.arch}")

    def package(self):
        # Install openh264 to the package folder
        self.run("make install PREFIX={}".format(self.package_folder))

        # Copy licenses
        copy(self, "LICENSE", self.source_folder, os.path.join(self.package_folder, "licenses"))

    def package_info(self):
        self.cpp_info.libs = ["openh264"]
