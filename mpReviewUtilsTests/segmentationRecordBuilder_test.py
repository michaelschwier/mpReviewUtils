import unittest
import os

from mpReviewUtils.segmentationRecordBuilder import SegmentationRecordBuilder
from mpReviewUtils.segmentationRecord import SegmentationRecord

class TestSegmentationRecordBuilder(unittest.TestCase):

  def setUp(self):
    self.baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "testData"))

  def test_build_returnsNoneIfNotAllParamtersSet(self):
    self.assertIsNone(SegmentationRecordBuilder().build())
    self.assertIsNone(SegmentationRecordBuilder(study = "A").build())
    self.assertIsNone(SegmentationRecordBuilder(series = "B").build())
    self.assertIsNone(SegmentationRecordBuilder(segLabelFileName = "C").build())
    self.assertIsNone(SegmentationRecordBuilder(study = "A", series = "B").build())
    self.assertIsNone(SegmentationRecordBuilder(study = "A", segLabelFileName = "C").build())
    self.assertIsNone(SegmentationRecordBuilder(series = "B", segLabelFileName = "C").build())

  def test_build_returnsNoneIfFileDoesNotExist(self):
    self.assertIsNone(SegmentationRecordBuilder(study = "A", series = "B", segLabelFileName = "C").build())
  
  def test_build_returnsValidObjectIfAllParametersSetAndMultilabelFileExists(self):
    segRecBuilder = SegmentationRecordBuilder()
    segRecBuilder.study = "P-01_20040701_0927"
    segRecBuilder.series = "801"
    segRecBuilder.segLabelFileName = os.path.join(self.baseDir, "P-01_20040701_0927", "RESOURCES", "801", "Segmentations", "readerone-MultipleLabels-20160206101010.nrrd")
    refOrigFile = os.path.join(self.baseDir, "P-01_20040701_0927", "RESOURCES", "801", "Reconstructions", "801.nrrd")
    refDicomFolder = os.path.join(self.baseDir, "P-01_20040701_0927", "RESOURCES", "801", "DICOM")
    segRec = segRecBuilder.build()
    self.assertEqual(segRec.patient, "P-01")
    self.assertEqual(segRec.study, "P-01_20040701_0927")
    self.assertEqual(segRec.series, "801")
    self.assertEqual(segRec.canonicalType, "ADC500")
    self.assertEqual(segRec.segmentedStructure, "MultipleLabels")
    self.assertListEqual(segRec.labelValue, [1, 2])
    self.assertEqual(segRec.reader, "readerone")
    self.assertEqual(segRec.labelFileName, segRecBuilder.segLabelFileName)
    self.assertEqual(segRec.origFileName, refOrigFile)
    self.assertEqual(segRec.dicomFolder, refDicomFolder)
    self.assertIsNone(segRec.measurements)

  def test_build_returnsValidLabelObjectIfAllParametersSetAndEmptylabelFileExists(self):
    segRecBuilder = SegmentationRecordBuilder()
    segRecBuilder.study = "P-01_20040701_0927"
    segRecBuilder.series = "801"
    segRecBuilder.segLabelFileName = os.path.join(self.baseDir, "P-01_20040701_0927", "RESOURCES", "801", "Segmentations", "readerone-Empty-20160307101214.nrrd")
    refOrigFile = os.path.join(self.baseDir, "P-01_20040701_0927", "RESOURCES", "801", "Reconstructions", "801.nrrd")
    refDicomFolder = os.path.join(self.baseDir, "P-01_20040701_0927", "RESOURCES", "801", "DICOM")
    segRec = segRecBuilder.build()
    self.assertEqual(segRec.patient, "P-01")
    self.assertEqual(segRec.study, "P-01_20040701_0927")
    self.assertEqual(segRec.series, "801")
    self.assertEqual(segRec.canonicalType, "ADC500")
    self.assertEqual(segRec.segmentedStructure, "Empty")
    self.assertIsNone(segRec.labelValue)
    self.assertEqual(segRec.reader, "readerone")
    self.assertEqual(segRec.labelFileName, segRecBuilder.segLabelFileName)
    self.assertEqual(segRec.origFileName, refOrigFile)
    self.assertEqual(segRec.dicomFolder, refDicomFolder)
    self.assertIsNone(segRec.measurements)

  def test_build_returnsValidObjectOnSegmentationTestDataWithMissingMeasurmementsFile(self):
    segRecBuilder = SegmentationRecordBuilder()
    segRecBuilder.study = "P-01_20040701_0927"
    segRecBuilder.series = "801"
    segRecBuilder.segLabelFileName = os.path.join(self.baseDir, "P-01_20040701_0927", "RESOURCES", "801", "Segmentations", "readerone-TumorROI_PZ_1-20160112105458.nrrd")
    refOrigFile = os.path.join(self.baseDir, "P-01_20040701_0927", "RESOURCES", "801", "Reconstructions", "801.nrrd")
    refDicomFolder = os.path.join(self.baseDir, "P-01_20040701_0927", "RESOURCES", "801", "DICOM")
    segRec = segRecBuilder.build()
    self.assertEqual(segRec.patient, "P-01")
    self.assertEqual(segRec.study, "P-01_20040701_0927")
    self.assertEqual(segRec.series, "801")
    self.assertEqual(segRec.canonicalType, "ADC500")
    self.assertEqual(segRec.segmentedStructure, "TumorROI_PZ_1")
    self.assertEqual(segRec.labelValue, 1)
    self.assertEqual(segRec.reader, "readerone")
    self.assertEqual(segRec.labelFileName, segRecBuilder.segLabelFileName)
    self.assertEqual(segRec.origFileName, refOrigFile)
    self.assertEqual(segRec.dicomFolder, refDicomFolder)
    self.assertIsNone(segRec.measurements)

  def test_build_returnsValidObjectOnSegmentationTestDataWithExistingMeasurmementsFile(self):
    segRecBuilder = SegmentationRecordBuilder()
    segRecBuilder.study = "P-01_20040701_0927"
    segRecBuilder.series = "901"
    segRecBuilder.segLabelFileName = os.path.join(self.baseDir, "P-01_20040701_0927", "RESOURCES", "901", "Segmentations", "readerone-PeripheralZone-20160112105458.nrrd")
    refOrigFile = os.path.join(self.baseDir, "P-01_20040701_0927", "RESOURCES", "901", "Reconstructions", "901.nrrd")
    refMeasurements = {"Count": 2158, "SegmentationName": "readerone-PeripheralZone-20160112105458.nrrd", "Median": 781.962890625, "StandardDeviation": 288.7469356104901, "Volume": 3200.341022456119, "Mean": 769.06765523633}
    segRec = segRecBuilder.build()
    self.assertEqual(segRec.patient, "P-01")
    self.assertEqual(segRec.study, "P-01_20040701_0927")
    self.assertEqual(segRec.series, "901")
    self.assertEqual(segRec.canonicalType, "ADC1400")
    self.assertEqual(segRec.segmentedStructure, "PeripheralZone")
    self.assertEqual(segRec.labelValue, 1)
    self.assertEqual(segRec.reader, "readerone")
    self.assertEqual(segRec.labelFileName, segRecBuilder.segLabelFileName)
    self.assertEqual(segRec.origFileName, refOrigFile)
    self.assertIsNone(segRec.dicomFolder)
    self.assertDictEqual(segRec.measurements, refMeasurements)

  def test_isValid_returnsFalseIfNotAllParametersSet(self):
    self.assertIs(SegmentationRecordBuilder().isValid(), False)
    self.assertIs(SegmentationRecordBuilder(study = "A").isValid(), False)
    self.assertIs(SegmentationRecordBuilder(series = "B").isValid(), False)
    self.assertIs(SegmentationRecordBuilder(segLabelFileName = "C").isValid(), False)
    self.assertIs(SegmentationRecordBuilder(study = "A", series = "B").isValid(), False)
    self.assertIs(SegmentationRecordBuilder(study = "A", segLabelFileName = "C").isValid(), False)
    self.assertIs(SegmentationRecordBuilder(series = "B", segLabelFileName = "C").isValid(), False)

  def test_isValid_returnsFalseIfAllParametersSetButFileNotExists(self):
    self.assertIs(SegmentationRecordBuilder(study = "A", series = "B", segLabelFileName = "C").isValid(), False)
  
  def test_isValid_returnsTrueIfAllParametersSetAndFileExists(self):
    segRecBuilder = SegmentationRecordBuilder()
    segRecBuilder.study = "P-01_20040701_0927"
    segRecBuilder.series = "901"
    segRecBuilder.segLabelFileName = os.path.join(self.baseDir, "P-01_20040701_0927", "RESOURCES", "901", "Segmentations", "readerone-PeripheralZone-20160112105458.nrrd")
    self.assertIs(segRecBuilder.isValid(), True)



if __name__ == "__main__":
  unittest.main()


