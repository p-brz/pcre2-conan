from conans import ConanFile, ConfigureEnvironment
import os
from os import path
from conans.tools import download, unzip, untargz, check_sha256
from conans import CMake

class PCRE2ConanFile(ConanFile):
    name = "pcre2"
    version = "10.22"
    branch = "stable"
    license = "BSD"
    url="https://github.com/paulobrizolara/pcre2-conan.git"
    settings = "os", "compiler", "build_type", "arch"

    BASE_URL_DOWNLOAD = "https://sourceforge.net/projects/pcre/files/pcre2"
    FILE_URL = BASE_URL_DOWNLOAD + "/10.22/pcre2-10.22.tar.bz2/download"
    ZIP_FOLDER_NAME = "pcre2-10.22"
    FILE_SHA256 = 'b2b44619f4ac6c50ad74c2865fd56807571392496fae1c9ad7a70993d018f416'

    def source(self):
        zip_name = "pcre2.zip"
        download(self.FILE_URL, zip_name)
        check_sha256(zip_name, self.FILE_SHA256)
        untargz(zip_name)
        os.unlink(zip_name)

    def build(self):
        #Make install dir
        self.install_dir = path.abspath(path.join(".", "install"))
        self._try_make_dir(self.install_dir)

        #Change to extracted dir
        os.chdir(self.ZIP_FOLDER_NAME)

        env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
        self.run_configure(env)
        self.run("%s make" % env.command_line)
        self.run("%s make install" % env.command_line)

    def run_configure(self, env):
        opts = ["--enable-pcre2-16",
                    "--enable-pcre2-32",
                    "--disable-stack-for-recursion",
                    "--prefix=%s" % self.install_dir]
        options = " ".join(opts)

        configure_file = path.join('.', 'configure')
        configure_cmd = "%s %s %s" % (env.command_line, configure_file, options)
        self.output.info(configure_cmd)

        self.run(configure_cmd)

    def package(self):
        #Copy all install dir content to the package directory
        self.copy("*", src=self.install_dir, dst=".")

    def package_info(self):
        #TODO: allow select libraries in options
        self.cpp_info.libs = ["pcre2-8","pcre2-16","pcre2-32"]

    def chmod_files(self, dir, mode):
        content = os.listdir(dir)

        for f in content:
            f = path.join(dir, f)

            if not path.isdir(f):
                os.chmod(f, mode)

    def _try_make_dir(self, dir):
        try:
            os.mkdir(dir)
        except OSError:
            #dir already exist
            pass
