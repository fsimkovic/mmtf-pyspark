#!/usr/bin/env python

import unittest
from pyspark.sql import SparkSession
from mmtfPyspark.io.mmtfReader import download_mmtf_files
from mmtfPyspark.webfilters import BlastCluster
from mmtfPyspark.mappers import StructureToPolymerChains


class BlastClustersTest(unittest.TestCase):

    def setUp(self):
        self.spark = SparkSession.builder.master("local[*]") \
                                 .appName("blastClustersTest") \
                                 .getOrCreate()
    
        pdbIds = ["1O06", "2ONX"]
        self.pdb = download_mmtf_files(pdbIds)

    def test1(self):

        pdb_1 = self.pdb.filter(BlastCluster(40))
        results_1 = pdb_1.keys().collect()

        self.assertTrue('1O06' in results_1)
        self.assertFalse('1O06.A' in results_1)
        self.assertFalse('2ONX' in results_1)

    def test2(self):

        pdb_2 = self.pdb.filter(BlastCluster(40))
        pdb_2 = pdb_2.flatMap(StructureToPolymerChains())
        results_2 = pdb_2.keys().collect()

        self.assertFalse('1O06' in results_2)
        self.assertTrue('1O06.A' in results_2)
        self.assertFalse('2ONX' in results_2)

    def tearDown(self):
        self.spark.stop()


if __name__ == '__main__':
    unittest.main()
