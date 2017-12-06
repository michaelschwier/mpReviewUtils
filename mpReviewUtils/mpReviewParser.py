from .segmentationRecordsParserBase import SegmentationRecordsParserBase

import os
import numpy

from .segmentationRecord import SegmentationRecord
from .studyParser import StudyParser

class MpReviewParser(SegmentationRecordsParserBase):
  """
  This parser goes through an mpReview root Directory structure and collects 
  all links to segmentations, meta information for each segmentation as well  
  as the link to the corresponding original image and measurments file.
  All info for each segmentation is stored in a SegmentationRecord.
  """
  
  def __init__(self, baseDirectory):
    self._baseDirectory = os.path.abspath(baseDirectory)
    self._currentStudy = None

  
  def getSegmentationRecords(self, onlySingleLabelSegmentations = True):
    segmentationRecords = []
    studyNames = self._getAllStudyNames()
    for study in studyNames:
      studyDirectory = self._getStudyDirectory(study)
      studyParser = StudyParser(studyDirectory)
      segmentationRecords.extend(studyParser.getSegmentationRecords())
    if onlySingleLabelSegmentations:
      segmentationRecords = [segRec for segRec in segmentationRecords if isinstance(segRec.labelValue, (int, numpy.integer))]
    return segmentationRecords


  #----------------------------------------------------------------------------
  # Internal methods
  #----------------------------------------------------------------------------
  def _getAllStudyNames(self):
    dirList = self._getAllValidDirs(self._baseDirectory)
    studyNames = []
    for studyName in dirList:
      studyDir = self._getStudyDirectory(studyName)
      if os.path.isdir(studyDir):
        studyNames.append(studyName)
    return studyNames


  def _getStudyDirectory(self, studyName):
    studyDir = os.path.join(self._baseDirectory, studyName, "RESOURCES")
    return studyDir





