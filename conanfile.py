#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class ZMQConan(ConanFile):
    name = "zmq"
    version = "4.3.2"
    url = "https://github.com/ulricheck/conan-zmq"
    description = "ZeroMQ is a community of projects focused on decentralized messaging and computing"
    license = "https://github.com/someauthor/somelib/blob/master/LICENSES"
    exports_sources = ["LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    def configure(self):
        del self.settings.compiler.libcxx

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

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED"] = self.options.shared
        cmake.definitions["BUILD_STATIC"] = not self.options.shared
        cmake.definitions["ZMQ_BUILD_TESTS"] = False
        cmake.configure(source_dir="sources")
        cmake.build()
        cmake.install()

    def package(self):
        with tools.chdir("sources"):
            self.copy(pattern="LICENSE")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.compiler == 'Visual Studio':
            self.cpp_info.libs.extend(['ws2_32', 'Iphlpapi'])
            if not self.options.shared:
                self.cpp_info.defines.append('ZMQ_STATIC')
        elif self.settings.os == "Linux":
            self.cpp_info.libs.append('pthread')
