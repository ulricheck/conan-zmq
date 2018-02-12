#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class ZMQConan(ConanFile):
    name = "zmq"
    version = "4.2.3"
    url = "https://github.com/ulricheck/conan-zmq"
    description = "ZeroMQ is a community of projects focused on decentralized messaging and computing"
    license = "https://github.com/someauthor/somelib/blob/master/LICENSES"
    exports_sources = ["LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    def system_requirements(self):
        if self.settings.os == "Linux":
            if tools.os_info.linux_distro == "ubuntu" or tools.os_info.linux_distro == "debian":
                arch = ''
                if self.settings.arch == "x86" and tools.detected_architecture() == "x86_64":
                    arch = ':i386'
                installer = tools.SystemPackageTool()
                installer.install('pkg-config%s' % arch)

    def source(self):
        self.run("git clone --branch v%s https://github.com/zeromq/libzmq.git sources" % self.version)
        # extracted_dir = "zeromq-%s" % self.version
        # if self.settings.os == "Windows":
        #     archive_name = "%s.zip" % extracted_dir
        # else:
        #     archive_name = "%s.tar.gz" % extracted_dir
        # source_url = "https://github.com/zeromq/libzmq/releases/download/v%s/%s" % (self.version, archive_name)
        # tools.get(source_url)
        # os.rename(extracted_dir, "sources")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.configure(source_dir="sources")
        cmake.build()
        cmake.install()

    def package(self):
        with tools.chdir("sources"):
            self.copy(pattern="LICENSE")

    def package_info(self):
        if self.settings.compiler == 'Visual Studio':
            self.cpp_info.libs = ['libzmq', 'ws2_32', 'Iphlpapi']
            if not self.options.shared:
                self.cpp_info.defines.append('ZMQ_STATIC')
        else:
            self.cpp_info.libs = ['zmq']
        if self.settings.os == "Linux":
            self.cpp_info.libs.append('pthread')
