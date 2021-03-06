#!/usr/bin/env python3
"""!
@file: run_vunit.py

Based on https://vunit.github.io/user_guide.html#introduction
"""
import vunit


class Library:
    def __init__(self, vu):
        """
        Create the VUnit library.
        """
        # Note that the library name 'work' is not allowed.
        self.lib = vu.add_library("lib")
        self.ghdl_common_flags = ["--std=08"]
        self.sources = ["half_adder.vhd", "half_adder_tb.vhd"]

    def setup(self):
        """
        Add sources and configure library.
        """
        self.add_sources()
        self.configure_compile()
        self.configure_run()

    def add_sources(self):
        """
        Point VUnit to the source files.
        """
        for s in self.sources:
            self.lib.add_source_file(s)

    def configure_compile(self):
        """
        Configure how VUnit builds the design and tests.
        """
        self.lib.add_compile_option("ghdl.a_flags", self.ghdl_common_flags)

    def configure_run(self):
        """
        Configure how VUnit runs the tests.
        """
        self.lib.set_sim_option("ghdl.elab_flags", self.ghdl_common_flags)
        # Find test bench in lib
        tb = self.lib.test_bench("half_adder_tb")
        # Find test in test bench
        test = tb.test("logic")
        # We'll be overwriting the default configuration,
        # so need to add it explicitly.
        test.add_config("default")
        # Add a configuration with generic "fail" set to true
        # to demonstrate test failure.
        test.add_config("fail", generics={"fail": True})


def main():
    # Create VUnit instance from command line arguments
    vu = vunit.VUnit.from_argv()
    Library(vu).setup()
    # Run VUnit
    vu.main()


if __name__ == "__main__":
    # Runs when this file is executed, not when it is imported.
    main()
