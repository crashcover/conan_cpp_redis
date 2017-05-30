from conans import ConanFile, CMake
import os


channel = os.getenv("CONAN_CHANNEL", "stable")
username = os.getenv("CONAN_USERNAME", "crashcover")


class CppredisTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "cpp_redis/3.5.1@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is in "test_package"
        cmake.configure(source_dir=self.conanfile_directory, build_dir="./")
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")

    def test(self):
        os.chdir("bin")
        self.run(".%sexample" % os.sep)