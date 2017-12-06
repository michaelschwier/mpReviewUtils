from .segmentationRecordsParserBase import SegmentationRecordsParserBase

import os

from .segmentationRecord import SegmentationRecord
from .seriesParser import SeriesParser

class StudyParser(SegmentationRecordsParserBase):
  """
  This parser goes through an mpReview study sub-directory structure and collects 
  all links to segmentations, meta information for each segmentation as well  
  as the link to the corresponding original image and measurments file.
  All info for each segmentation is stored in a SegmentationRecord.
  """
  def __init__(self, studyDirectory):
    self._studyDirectory = studyDirectory
    self._studyName = self._getStudyName(studyDirectory)


  def getSegmentationRecords(self):
    segmentationRecords = []
    seriesNames = self._getAllSeriesNames()
    for series in seriesNames:
      seriesDirectory = os.path.join(self._studyDirectory, series)
      seriesParser = SeriesParser(seriesDirectory, self._studyName)
      segmentationRecords.extend(seriesParser.getSegmentationRecords())
    return segmentationRecords


  #----------------------------------------------------------------------------
  # Internal methods
  #----------------------------------------------------------------------------
  def _getAllSeriesNames(self):
    dirList = self._getAllValidDirs(self._studyDirectory)
    return dirList


  def _getStudyName(self, studyDirectory):
    oneDirUp = os.path.split(os.path.normpath(studyDirectory))[0]
    return os.path.basename(oneDirUp)




