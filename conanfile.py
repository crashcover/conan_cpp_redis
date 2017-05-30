from conans import ConanFile, CMake


class CppredisConan(ConanFile):
    name = "cpp_redis"
    description = "C++11 Lightweight Redis client: async, thread-safe, no dependency, pipelining, multi-platform."
    version = "3.5.1"
    license = "MIT License"
    url = "https://github.com/crashcover/conan_cpp_redis"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    folder_name = "cpp_redis"

    def source(self):
        self.run("git clone --recursive https://github.com/Cylix/cpp_redis.git")
        self.run("cd cpp_redis && git checkout tags/%s" % self.version)

    def build(self):
        cmake = CMake(self)
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        self.run('cmake %s %s %s' % (self.folder_name, cmake.command_line, shared))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*", dst="include", src=self.folder_name+"/includes")
        self.copy("*", dst="include", src=self.folder_name+"/tacopie/includes")
        self.copy("*.lib", dst="lib", src="lib")
        self.copy("*.lib", dst="lib", src=self.folder_name+"/deps/lib")
        self.copy("*.so", dst="lib", src="lib")
        self.copy("*.so", dst="lib", src=self.folder_name+"/deps/lib")
        self.copy("*.a", dst="lib", src="lib")
        self.copy("*.a", dst="lib", src=self.folder_name+"/deps/lib")

    def package_info(self):
        self.cpp_info.libs = ["cpp_redis", "tacopie"]
