#This program tests the checksum function of the task2.py program. It uses asserts to ensure the checksum is calculated correctly. All tests will pass.

#Imports the libraries/program needed for this program to work as intended.

import task2
import unittest


class testTask2(unittest.TestCase):
    #Tests the default output for Task 2, provided in the worksheet.
    def testTask2Default(self):
        assert task2.compute_checksum(10, 42, 'Welcome to IoT UDP Server'.encode()) == 15307, "Should be 15307"
    #Tests the output for Task 2, with a customised payload but identical ports.
    def testTask2Custom1(self):
        assert task2.compute_checksum(10, 42, 'Hello World'.encode()) == 26417, "Should be 26417"
    #Tests the output for Task 2, with customised ports and a customised payload.
    def testTask2Custom2(self):
        assert task2.compute_checksum(67, 505, 'Custom Ports'.encode()) == 34160, "Should be 34160"

#Main function to run all of the unit tests.
if __name__ == '__main__':
    unittest.main()
