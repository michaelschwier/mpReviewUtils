from abc import ABCMeta, abstractmethod
import os

class SegmentationRecordsParserBase:
  """
  Base class for Parsers that work on the mpReview Data/File Structure
  """
  __metaclass__ = ABCMeta

  @abstractmethod
  def getSegmentationRecords(self):
    pass


  def _getAllValidDirs(self, baseDir):
    if not os.path.isdir(baseDir):
      return []
    else:
      dirList = os.listdir(baseDir)
      dirList = [d for d in dirList if os.path.isdir(os.path.join(baseDir, d))]
      dirList = [d for d in dirList if not d.startswith(".")]
      return dirList
    





