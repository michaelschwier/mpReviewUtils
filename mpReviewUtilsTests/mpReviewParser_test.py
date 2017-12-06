import unittest
import os

from mpReviewUtils import MpReviewParser
from mpReviewUtils import SegmentationRecord

class TestMpReviewParser(unittest.TestCase):

  def setUp(self):
    self.baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "testData"))
    self.parser = MpReviewParser(self.baseDir)
    self.invalidDir = os.path.join(self.baseDir, "INEXISTENT")
    self.invalidParser = MpReviewParser(self.invalidDir)
  
  def tearDown(self):
    self.parser = None

  def test_initWasSucessfull(self):
    self.assertIsNotNone(self.parser)

  def test_getAllValidDirs_returnsValidDirsOnValidBaseDir(self):
    self.assertListEqual(self.parser._getAllValidDirs(self.baseDir), ["P-01_20040701_0927", 
                                                                      "P-01_20040713_1325", 
                                                                      "P-12_20051226_1314"])

  def test_getAllValidDirs_returnsEmptyListOnInvalidDir(self):
    self.assertListEqual(self.parser._getAllValidDirs(self.invalidDir), [])

  def test_getAllStudies_returnsStudiesOnValidBaseDir(self):
    testList = self.parser._getAllStudyNames()
    refList = ["P-01_20040701_0927",
               "P-01_20040713_1325",
               "P-12_20051226_1314"]
    self.assertListEqual(testList, refList)

  def test_getAllStudies_returnsEmptyListOnInvalidDir(self):
    self.assertListEqual(self.invalidParser._getAllStudyNames(), [])

  def test_getSegmentationRecords_returnsCorrectNumberOfResultsFromTestData(self):
    self.assertEqual(len(self.parser.getSegmentationRecords()), 8)
  
  def test_getSegmentationRecords_returnsCorrectNumberOfResultsFromTestDataAllowingMultipleLabels(self):
    self.assertEqual(len(self.parser.getSegmentationRecords(onlySingleLabelSegmentations = False)), 10)
  
  def test_getSegmentationRecords_returnedSegmentationRecordsHaveCorrectLabelFile(self):
    refList = ["readerone-TumorROI_PZ_1-20160112105458.nrrd",
               "readerone-WholeGland-20160112105458.nrrd",
               "readerone-PeripheralZone-20160112105458.nrrd",
               "readerone-TumorROI_PZ_1-20151215114032.nrrd",
               "readerone-TumorROI_PZ_1-20160112104825.nrrd",
               "readerone-WholeGland-20160112104825.nrrd",
               "readerone-NormalROI_PZ_1-20160211162158.nrrd",
               "readerone-TumorROI_PZ_1-20160211162158.nrrd"]
    refList.sort()
    testList = self.parser.getSegmentationRecords()
    testList = [os.path.basename(segRec.labelFileName) for segRec in testList]
    testList.sort()
    self.assertListEqual(testList, refList)

  def test_getSegmentationRecords_returnedSegmentationRecordIsCorrect(self):
    refSeriesPath = os.path.join(self.baseDir, "P-01_20040701_0927", "RESOURCES", "801")
    refSegFilePath = os.path.join(refSeriesPath, "Segmentations", "readerone-TumorROI_PZ_1-20160112105458.nrrd")
    refOrigFilePath = os.path.join(refSeriesPath, "Reconstructions", "801.nrrd")
    refDicomFolder = os.path.join(refSeriesPath, "DICOM")
    refSegRec = SegmentationRecord("P-01", #patient
                                   "P-01_20040701_0927", #study
                                   "801", #series
                                   "ADC500", #canonical type
                                   "TumorROI_PZ_1", #segmented structure
                                   1, #labelValue
                                   "readerone", #reader
                                   refSegFilePath, #label file
                                   refOrigFilePath, #origFile 
                                   refDicomFolder, #DICOM folder
                                   None) #measurments
    testList = self.parser.getSegmentationRecords()
    testList = [t for t in testList if t.labelFileName == refSegFilePath]
    self.assertEqual(len(testList), 1)
    testSegRec = testList[0]
    self.assertEqual(testSegRec, refSegRec)

  def test_getSegmentationRecords_dicomFoldersInReturnedSegmentationRecordsAreCorrect(self):
    testList = self.parser.getSegmentationRecords()
    for segRec in testList:
      if (segRec.study == "P-01_20040701_0927") and (segRec.series == "901"):
        self.assertIsNone(segRec.dicomFolder)
      else:
        refDicomFolder = os.path.join(self.baseDir, segRec.study, "RESOURCES", segRec.series, "DICOM")
        self.assertEqual(segRec.dicomFolder, refDicomFolder)

if __name__ == "__main__":
  unittest.main()


