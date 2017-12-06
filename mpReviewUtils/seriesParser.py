from .segmentationRecordsParserBase import SegmentationRecordsParserBase

import os
import glob
from collections import defaultdict

from .segmentationRecord import SegmentationRecord
from .segmentationRecordBuilder import SegmentationRecordBuilder

class SeriesParser(SegmentationRecordsParserBase):
  """
  This parser goes through an mpReview series sub-directory structure and collects 
  all links to segmentations, meta information for each segmentation as well  
  as the link to the corresponding original image and measurments file.
  All info for each segmentation is stored in a SegmentationRecord.
  """
  def __init__(self, seriesDirectory, parentStudyName):
    self._baseDirectory = seriesDirectory
    self._seriesName = self._getSeriesName(seriesDirectory)
    self._parentStudyName = parentStudyName


  def getSegmentationRecords(self):
    segmentationRecords = []
    allSegFileNames = self._getAllSegmentationFileNames()
    groupedSegFiles = self._groupSegmentationFileNames(allSegFileNames)
    onlyNewestSegFiles = self._getNewestSegFilePerGroup(groupedSegFiles)
    validSegRecords = self._getSegmentationRecordsFromFileNames(onlyNewestSegFiles)
    return validSegRecords


  #----------------------------------------------------------------------------
  # Internal methods
  #----------------------------------------------------------------------------
  def _getAllSegmentationFileNames(self):
    segmentationsDir = os.path.join(self._baseDirectory, "Segmentations")
    searchPattern = os.path.join(segmentationsDir, "*.nrrd")
    fileList = glob.glob(searchPattern)
    segFileNames = []
    for f in fileList:
      if self._isValidSegmentationFileName(f):
        segFileNames.append(f)
    return segFileNames


  def _isValidSegmentationFileName(self, fileName):
    fileName = os.path.basename(fileName)
    if len(fileName.split("-")) == 3:
      return True
    else:
      return False

  
  def _groupSegmentationFileNames(self, segFileNames):
    """Group by reader and structure as filename prefix"""
    groups = defaultdict(list)
    for f in segFileNames:
      key = f.rsplit("-", 1)[0]
      groups[key].append(f)
    return groups


  def _getNewestSegFilePerGroup(self, groupedSegFileNames):
    """Getting the newest file per group based on the encoded
       date and time in the segmentation file names groups"""
    newestSegFileNames = []
    for key, fileList in groupedSegFileNames.items():
      fileList.sort()
      newestSegFileNames.append(fileList[-1])
    return newestSegFileNames


  def _getSegmentationRecordsFromFileNames(self, fileNames):
    segRecords = []
    for fn in fileNames:
      segRecords.append(self._createSegmetationRecord(fn))
    return segRecords
  

  def _createSegmetationRecord(self, segFile):
    segRecBuilder = SegmentationRecordBuilder()
    segRecBuilder.study = self._parentStudyName
    segRecBuilder.series = self._seriesName
    segRecBuilder.segLabelFileName = segFile
    return segRecBuilder.build()

  
  def _getSeriesName(self, seriesDirectory):
    return os.path.basename(os.path.normpath(seriesDirectory))



