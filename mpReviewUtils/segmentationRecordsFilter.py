from collections import defaultdict

from .segmentationRecord import SegmentationRecord

class SegmentationRecordsFilter(object):
  """
  Filters the given Segmentation Records based on user defined conditions
  on properties.
  A condition is simply a combination of a property name and one or more
  values. If no condition is given for a property (default), all values for
  this property will be considered.
  To be considered as a result, each property of a Segmentation Record
  must match a condition.
  """
  def __init__(self, segmentationRecords):
    self._segmentationRecords = segmentationRecords
    self._conditions = defaultdict(list)


  def getResults(self):
    results = []
    for segRec in self._segmentationRecords:
      if (self._matchesConditions(segRec)):
        results.append(segRec)
    return results


  def addCondition(self, propertyName, acceptedValues):
    if type(acceptedValues) is list:
      self._conditions[propertyName].extend(acceptedValues)
    else:
      self._conditions[propertyName].append(acceptedValues)


  #----------------------------------------------------------------------------
  # Internal methods
  #----------------------------------------------------------------------------
  def _matchesConditions(self, segRec):
    for propertyName, acceptedValues in self._conditions.items():
      if getattr(segRec, propertyName) not in acceptedValues:
        return False
    return True


