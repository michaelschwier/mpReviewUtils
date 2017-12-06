import os
import json
import SimpleITK
import numpy
from .segmentationRecord import SegmentationRecord

class SegmentationRecordBuilder(object):

  def __init__(self, study = None, series = None, segLabelFileName = None):
    self.study = study
    self.series = series
    self.segLabelFileName = segLabelFileName


  def build(self):
    if (self.isValid()):
      return self._createSegmentationRecord()
    else:
      return None
  

  def isValid(self):
    if (self.study is not None and
        self.series is not None and
        self.segLabelFileName is not None and
        os.path.isfile(self.segLabelFileName)):
      return True
    else:
      return False
    

  #----------------------------------------------------------------------------
  # Internal methods
  #----------------------------------------------------------------------------
  def _createSegmentationRecord(self):
    segRec = SegmentationRecord(self._getPatientName(),
                                self.study, 
                                self.series, 
                                self._getCanonicalType(),
                                self._getSegmentedStructure(),
                                self._getLabelValue(),
                                self._getReaderName(),
                                self.segLabelFileName,
                                self._getOrigFileName(), 
                                self._getDicomFolder(),
                                self._getMeasurments())
    return segRec
  
  def _getPatientName(self):
    patientName = self.study.split("_")[0]
    return patientName

  def _getReaderName(self):
    labelFileName = os.path.basename(self.segLabelFileName)
    readerName = labelFileName.split("-")[0]
    return readerName

  def _getSegmentedStructure(self):
    labelFileName = os.path.basename(self.segLabelFileName)
    try:
      segmentedStructure = labelFileName.split("-")[1]
      return segmentedStructure
    except Exception:
      return None
  
  def _getLabelValue(self):
    image = SimpleITK.ReadImage(self.segLabelFileName)
    npPixelArray = SimpleITK.GetArrayViewFromImage(image)
    labelValues = numpy.unique(npPixelArray)
    labelValues = [l for l in labelValues if l != 0]
    return self._reduceToSingleLabelValueIfPossible(labelValues)

  def _reduceToSingleLabelValueIfPossible(self, labelValues):
    if len(labelValues) == 1:
      return labelValues[0]
    elif len(labelValues) == 0:
      return None
    else:
      return labelValues

  def _getOrigFileName(self):
    origFileName = os.path.normpath(os.path.join(self._getSeriesDir(), "Reconstructions", self.series + ".nrrd"))
    if os.path.isfile(origFileName):
      return origFileName
    else:
      return None

  def _getCanonicalType(self):
    canonicalFileName = self._getCanonicalFileName()
    if canonicalFileName:
      return self._getCanonicalTypeFromJsonFile(canonicalFileName)
    else:
      return None
  
  def _getCanonicalFileName(self):
    canonicalFileName = os.path.normpath(os.path.join(self._getSeriesDir(), "Canonical", self.series + ".json"))
    if os.path.isfile(canonicalFileName):
      return canonicalFileName
    else:
      return None
  
  def _getCanonicalTypeFromJsonFile(self, jsonFileName):
    with open(jsonFileName, "r") as jsonFile:
      attributes = json.load(jsonFile)
      if "CanonicalType" in attributes:
        return attributes["CanonicalType"]
      else:
        return None

  def _getDicomFolder(self):
    dicomFolder = os.path.normpath(os.path.join(self._getSeriesDir(), "DICOM"))
    if os.path.isdir(dicomFolder):
      return dicomFolder
    else:
      return None
  
  def _getMeasurments(self):
    measurementsFileName = self._getMeasurementsFileName()
    if os.path.isfile(measurementsFileName):
      with open(measurementsFileName, "r") as jsonFile:
        return json.load(jsonFile)
    else:
      return None

  def _getMeasurementsFileName(self):
    measurementsDir = os.path.normpath(os.path.join(self._getSeriesDir(), "Measurements"))
    segStructure = self._getSegmentedStructure() if self._getSegmentedStructure() is not None else ""
    readerName = self._getReaderName() if self._getReaderName() is not None else ""
    measurementsFileName =  self.series + "-" + \
                            segStructure + "-"  + \
                            readerName + ".json"
    measurementsFileName = os.path.join(measurementsDir, measurementsFileName)
    return measurementsFileName

  def _getSeriesDir(self):
    segDir = os.path.dirname(self.segLabelFileName)
    return os.path.normpath(os.path.join(segDir, ".."))




