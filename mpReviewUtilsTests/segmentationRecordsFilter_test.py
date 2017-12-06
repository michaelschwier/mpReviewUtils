import unittest

from mpReviewUtils import SegmentationRecordsFilter
from . import segmentationRecordTestsUtils

class TestSegmentationRecordsFilter(unittest.TestCase):

  def setUp(self):
    self.testData = segmentationRecordTestsUtils.generateTestSegmentationRecords(2, 2, 2, 2, 2)
    self.filter = SegmentationRecordsFilter(self.testData)

  def test_canInstantiate(self):
    self.assertIsNotNone(self.filter)

  def test_getResults_noFiltersReturnsCorrectNumberOfResults(self):
    filteredSegRecs = self.filter.getResults()
    self.assertEqual(len(filteredSegRecs), 32)

  def test_getResults_raisesAttributeErrorOnNonExisitingProperty(self):
    self.filter.addCondition("non_existent", "bogus")
    with self.assertRaises(AttributeError):
      self.filter.getResults()
  
  def test_getResults_oneConditionOnOnePropertyReturnsCorrectResults(self):
    self.filter.addCondition("study", "Study0")
    filteredSegRecs = self.filter.getResults()
    self.assertEqual(len(filteredSegRecs), 16)
    for segRec in filteredSegRecs:
      self.assertEqual(segRec.study, "Study0")

  def test_getResults_twoConditionsOnOnePropertyReturnsCorrectResults(self):
    self.filter.addCondition("study", "Study0")
    self.filter.addCondition("series", "Series0")
    self.filter.addCondition("series", "Series1")
    filteredSegRecs = self.filter.getResults()
    self.assertEqual(len(filteredSegRecs), 16)
    for segRec in filteredSegRecs:
      self.assertEqual(segRec.study, "Study0")
      self.assertTrue(segRec.series in ["Series0", "Series1"])

  def test_getResults_twoConditionsAsListOnOnePropertyReturnsCorrectResults(self):
    self.filter.addCondition("study", "Study0")
    self.filter.addCondition("series", ["Series0", "Series1"])
    filteredSegRecs = self.filter.getResults()
    self.assertEqual(len(filteredSegRecs), 16)
    for segRec in filteredSegRecs:
      self.assertEqual(segRec.study, "Study0")
      self.assertTrue(segRec.series in ["Series0", "Series1"])

  def test_getResults_conditionsOnTwoPropertyReturnsCorrectResults(self):
    self.filter.addCondition("study", "Study0")
    self.filter.addCondition("series", "Series1")
    filteredSegRecs = self.filter.getResults()
    self.assertEqual(len(filteredSegRecs), 8)
    for segRec in filteredSegRecs:
      self.assertEqual(segRec.study, "Study0")
      self.assertEqual(segRec.series, "Series1")

  def test_getResults_conditionsOnAllPropertiesReturnsOneResult(self):
    self.filter.addCondition("study", "Study0")
    self.filter.addCondition("series", "Series1")
    self.filter.addCondition("canonicalType", "Type1")
    self.filter.addCondition("segmentedStructure", "Struct1")
    self.filter.addCondition("reader", "Reader0")
    filteredSegRecs = self.filter.getResults()
    self.assertEqual(len(filteredSegRecs), 1)
    for segRec in filteredSegRecs:
      self.assertEqual(segRec.study, "Study0")
      self.assertEqual(segRec.series, "Series1")
      self.assertEqual(segRec.canonicalType, "Type1")
      self.assertEqual(segRec.segmentedStructure, "Struct1")
      self.assertEqual(segRec.reader, "Reader0")
    
  def test_getResults_inexistentConditionValueReturnsZeroResults(self):
    self.filter.addCondition("study", "non_existent")
    filteredSegRecs = self.filter.getResults()
    self.assertEqual(len(filteredSegRecs), 0)

if __name__ == "__main__":
  unittest.main()












