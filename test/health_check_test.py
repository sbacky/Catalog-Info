#!/usr/bin/env python3

from health_check import check_cpu_constrained
from health_check import check_disk_space
from health_check import check_memory
from health_check import check_no_network
import unittest
import subprocess

def stress_test(command):
    subprocess.run(command)

class TestCPU(unittest.TestCase):
    def test_under_thresh(self):
        command = ["stress", "--cpu", "2"]
        stress_test(command)
        expected = False
        self.assertEqual(check_cpu_constrained(), expected)

    def test_over_thresh(self):
        command = ["stress", "--cpu", "9"]
        stress_test(command)
        expected = True
        self.assertEqual(check_cpu_constrained(), expected)

    def test_at_thresh(self):
        command = ["stress", "--cpu", "8"]
        stress_test(command)
        expected = True
        self.assertEqual(check_cpu_constrained(), expected)

class TestDiskSpace(unittest.TestCase):
    def test_under_thresh(self):
        testcase =
        expected = False

    def test_over_thresh(self):
        testcase =
        expected = True

    def test_at_thresh(self):
        testcase =
        expected = True

class TestMemory(unittest.TestCase):
    def test_under_thresh(self):
        testcase =
        expected = False

    def test_over_thresh(self):
        testcase =
        expected = True

    def test_at_thresh(self):
        testcase =
        expected = True

unittest.main()
