from .segmentationRecord import SegmentationRecord
from collections import defaultdict

class SegmentationRecordsInspector(object):
  """
  Utility class that provides functions to get information from a list of
  segmentation records.
  """

  def __init__(self, segmentationRecords):
    self._segmentationRecords = segmentationRecords


  def getValuesInProperty(self, propertyName):
    values = set()
    for segRec in self._segmentationRecords:
      values.add(getattr(segRec, propertyName))
    return values


  def getStudyNumbersMap(self):
    studyNumbersMap = []
    patientsToStudies = self._getPatientsToStudiesMap()
    for patient, studies in patientsToStudies.items():
      sortedStudies = self._getSortedStudies(studies)
      for i, study in enumerate(sortedStudies):
        entry = self._createStudyNumbersEntry(patient, study, i)
        studyNumbersMap.append(entry)
    return studyNumbersMap



  #----------------------------------------------------------------------------
  # Internal methods
  #----------------------------------------------------------------------------
  def _getPatientsToStudiesMap(self):
    patients = defaultdict(set)
    for segRec in self._segmentationRecords:
      patients[segRec.patient].add(segRec.study)
    return patients


  def _getSortedStudies(self, studies):
    studiesList = list(studies)
    studiesList.sort()
    return studiesList


  def _createStudyNumbersEntry(self, patient, study, i):
    d = dict()
    d["patient"] = patient
    d["study"] = study
    d["studyNumber"] = i
    return d













