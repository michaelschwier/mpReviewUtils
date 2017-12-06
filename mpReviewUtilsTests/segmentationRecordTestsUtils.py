# defining some utility functions that are handy for several
# of the test classes that deal with segmentation records.

from mpReviewUtils import SegmentationRecord

def generateTestSegmentationRecords(noStudies = 1, noSeries = 1, 
                                    noTypes = 1, noStructs = 1,
                                    noReaders = 1, labelValue = 1):
  """generates testdata with all possible permutations of the
     given number of properties"""
  segmentationRecords = []
  for study in range(noStudies):
    for series in range(noSeries):
      for typ in range(noTypes):
        for struct in range(noStructs):
          for reader in range(noReaders):
            segRec = SegmentationRecord("Pat", 
                                        "Study" + str(study), 
                                        "Series" + str(series), 
                                        "Type" + str(typ), 
                                        "Struct" + str(struct), 
                                        labelValue, 
                                        "Reader" + str(reader), 
                                        "Label-File-0815", 
                                        "OrigFile", 
                                        "DICOM_Folder",
                                        None)
            segmentationRecords.append(segRec)
  return segmentationRecords
