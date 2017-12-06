from collections import namedtuple

class SegmentationRecord(namedtuple("SegmentationRecord", "patient, study, series, canonicalType, "
                                                          "segmentedStructure, labelValue, reader, "
                                                          "labelFileName, origFileName, dicomFolder, "
                                                          "measurements")):
  """
  Data structure to hold all meta information for a segmentation.
  All properties are just strings except:
  "measurements": a dict containing the content of the measurments file 
                  ascosciated with the segmentation.
  """
  __slots__ = () # Prevents the creation of instance dictionaries, thus keeping the class immutable.


