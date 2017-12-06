import unittest
import os

from mpReviewUtils import SegmentationRecordsInspector
from mpReviewUtils import MpReviewParser
from . import segmentationRecordTestsUtils

class TestSegmentationRecordsInspectorOnSyntheticTestData(unittest.TestCase):

  def setUp(self):
    self.testData = segmentationRecordTestsUtils.generateTestSegmentationRecords(5, 4, 3, 2, 1)
    self.inspector = SegmentationRecordsInspector(self.testData)
  
  def test_canInstantiate(self):
    self.assertIsNotNone(self.inspector)

  def test_getValuesInProperty_returnsFiveCorrectValuesForStudy(self):
    result = self.inspector.getValuesInProperty("study")
    self.assertSetEqual(result, set(["Study0", "Study1", "Study2", "Study3", "Study4"]))

  def test_getValuesInProperty_returnsFourCorrectValuesForSeries(self):
    result = self.inspector.getValuesInProperty("series")
    self.assertSetEqual(result, set(["Series0", "Series1", "Series2", "Series3"]))

  def test_getValuesInProperty_returnsOneCorrectValuesForReaders(self):
    result = self.inspector.getValuesInProperty("reader")
    self.assertSetEqual(result, set(["Reader0"]))

  def test_getValuesInProperty_returnsNoneForMeasurments(self):
    result = self.inspector.getValuesInProperty("measurements")
    self.assertSetEqual(result, set([None]))

  def test_getValuesInProperty_raisesAttributeErrorForNonExistentProperty(self):
    with self.assertRaises(AttributeError):
      result = self.inspector.getValuesInProperty("inexistent")
  
  def test_getStudyNumberMap_returnsCorrectStudyNumbersFromTimeStamps(self):
    result = self.inspector.getStudyNumbersMap()
    for mapping in result:
      self.assertEqual("Study" + str(mapping["studyNumber"]), mapping["study"])
  
  def test_getStudyNumbersMap_returnsCorrectFormatInResultDict(self):
    result = self.inspector.getStudyNumbersMap()
    for mapping in result:
      self.assertEqual(mapping["patient"], "Pat")
      self.assertEqual(mapping["study"][0:-1], "Study")
      self.assertIsInstance(mapping["studyNumber"], int)

  def test_getStudyNumbersMap_returnsCorrectMapSize(self):
    result = self.inspector.getStudyNumbersMap()
    self.assertEqual(len(result), 5)



class TestSegmentationRecordsInspectorOnRealTestData(unittest.TestCase):

  def setUp(self):
    self.baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "testData"))
    self.parser = MpReviewParser(self.baseDir)
    self.testData = self.parser.getSegmentationRecords()
    self.inspector = SegmentationRecordsInspector(self.testData)

  def test_getStudyNumberMap_returnsCorrectMapping(self):
    result = self.inspector.getStudyNumbersMap()
    for mapping in result:
      self.assertIn(mapping["study"], ["P-01_20040701_0927", "P-01_20040713_1325", "P-12_20051226_1314"])
      if mapping["study"] == "P-01_20040701_0927":
        self.assertDictEqual(mapping, {"patient": "P-01", "study": "P-01_20040701_0927", "studyNumber": 0})
      elif mapping["study"] == "P-01_20040713_1325":
        self.assertDictEqual(mapping, {"patient": "P-01", "study": "P-01_20040713_1325", "studyNumber": 1})
      elif mapping["study"] == "P-12_20051226_1314":
        self.assertDictEqual(mapping, {"patient": "P-12", "study": "P-12_20051226_1314", "studyNumber": 0})
      else:
        # if we reach this, then there is an unexpected study in the map
        self.assertFalse(True)

  def test_getStudyNumbersMap_returnsCorrectMapSize(self):
    result = self.inspector.getStudyNumbersMap()
    self.assertEqual(len(result), 3)
    





if __name__ == "__main__":
  unittest.main()


