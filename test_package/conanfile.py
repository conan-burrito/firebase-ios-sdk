from conans import tools, ConanFile, CMake
import os


class Test(ConanFile):
    settings = 'os', 'arch', 'compiler', 'build_type'

    generators = 'cmake'

    def build(self):
        cmake = CMake(self, generator='Xcode')
        cmake.definitions['CMAKE_OSX_ARCHITECTURES'] = 'x86_64'
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self.settings):
            bin_path = os.path.join('bin', 'test')
            self.run("{0}".format(bin_path), run_environment=True)
