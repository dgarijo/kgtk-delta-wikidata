import os
from hmac import new
from unittest import TestCase
from pathlib import Path
from calculate_deltas import calculate_deltas


class Test(TestCase):

    def test_calculate_deltas(self):
        old_file = os.path.join(Path(__file__).parent, 'old_test1.tsv')
        new_file = os.path.join(Path(__file__).parent, 'new_test1.tsv')
        calculate_deltas(old_file,new_file,'.')
        file = open("added.tsv", "r",encoding="utf-8")
        line_count = 0
        for line in file:
            if line != "\n":
                line_count += 1
        file.close()
        os.remove('added.tsv')
        os.remove('deleted.tsv')
        os.remove('modified_qual.tsv')
        if line_count is not 3:
            self.fail


    def test_calculate_deltas_1(self):
        old_file = os.path.join(Path(__file__).parent, 'old_test2.tsv')
        new_file = os.path.join(Path(__file__).parent, 'new_test2.tsv')
        calculate_deltas(old_file, new_file, '.')
        file = open("deleted.tsv", "r",encoding="utf-8")
        line_count = 0
        for line in file:
            if line != "\n":
                line_count += 1
        file.close()
        os.remove('added.tsv')
        os.remove('deleted.tsv')
        os.remove('modified_qual.tsv')
        if line_count is not 4:
            self.fail

    def test_calculate_deltas_2(self):
        old_file = os.path.join(Path(__file__).parent, 'old_test3.tsv')
        new_file = os.path.join(Path(__file__).parent, 'new_test3.tsv')
        calculate_deltas(old_file, new_file, '.')
        file = open("deleted.tsv", "r",encoding="utf-8")
        line_count_deleted = 0
        for line in file:
            if line != "\n":
                line_count_deleted += 1
        file.close()
        file = open("modified_qual.tsv", "r", encoding="utf-8")
        line_count_m = 0
        for line in file:
            if line != "\n":
                line_count_m += 1
        file.close()
        os.remove('added.tsv')
        os.remove('deleted.tsv')
        os.remove('modified_qual.tsv')
        if line_count_deleted is not 6 and line_count_m is not 3:
            self.fail

