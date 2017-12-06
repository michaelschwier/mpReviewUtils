import os, sys
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
# setup supported/required command line arguments
cmdlParser = argparse.ArgumentParser(description = "Select all segmentations that match the provided conditions.")
cmdlParser.add_argument("dir", 
                        help = "The abs path to the root data directory to parse")
cmdlParser.add_argument("--studies",
                        nargs = "*",
                        help = "List of all studies that should be selected.")
cmdlParser.add_argument("--series",
                        nargs = "*",
                        help = "List of all series that should be selected.")                        
cmdlParser.add_argument("--types",
                        nargs = "*",
                        help = "List of all series/canonical types that should be selected")
cmdlParser.add_argument("--structures",
                        nargs = "*",
                        help = "List of identifiers for all segmented structures that should be selected, e.g.: \"WholeGland\" \"PeripheralZone\".")
cmdlParser.add_argument("--readers",
                        nargs = "*",
                        help = "List of reader names that should be selected.")
cmdlParser.add_argument("--conditionsFile",
                        help = "JSON file setting filter conditions. If this parameters is provided all other filter arguments are ignored.")
cmdlParser.add_argument("--copyTo",
                        nargs = "?",
                        help = "The abs path to a directory to which to copy the selected segmentation and orig file. The copied files will be renamed to have a unique recognizable name.")


import os, shutil

from mpReviewUtils import MpReviewParser
from conditionsParser import ConditionsParser
from mpReviewUtils import SegmentationRecordsFilter


class SelectSegmentationsMain(object):
  """
  Main application class for the selectSegmentations comdl tool.
  Needs to be initialized with command line arguments parsed by
  argparse.
  """
  def __init__(self, args):
     self._args = args
     self._mpReviewParser = MpReviewParser(self._args.dir)
     self._conditionsParser = ConditionsParser(self._args)


  def run(self):
    selectedSegRecs = self.getSelectedSegmentationRecords()
    self.printSegmentationRecords(selectedSegRecs)
    if (self._args.copyTo):
      self.copySegAndOrigFiles(selectedSegRecs, self._args.copyTo)
  

  def getSelectedSegmentationRecords(self):
    segmentationRecords = self._mpReviewParser.getSegmentationRecords()
    filterConditions = self._conditionsParser.getFilterConditions()
    filter = SegmentationRecordsFilter(segmentationRecords)
    for propertyName, acceptedValues in filterConditions.items():
      filter.addCondition(propertyName, acceptedValues)
    return filter.getResults()


  def printSegmentationRecords(self, segmentationRecords):
    for i, segRec in enumerate(segmentationRecords):
      print str(i).zfill(3), segRec.study, segRec.series, \
            segRec.canonicalType, segRec.segmentedStructure, \
            "\n   \'-->", "Mean:", segRec.measurements["Mean"] if segRec.measurements is not None else "None"


  def copySegAndOrigFiles(self, segmentationRecords, destDir):
    if not os.path.exists(destDir):
      os.makedirs(destDir)
    for segRec in segmentationRecords:
      imageFileBaseName = segRec.study + "-" + segRec.series + "-" \
                          + segRec.canonicalType \
                          + "-image.nrrd"
      destImageFileName = os.path.join(destDir, imageFileBaseName)
      segFileBaseName = segRec.study + "-" + segRec.series + "-" \
                        + segRec.canonicalType + "-" + segRec.segmentedStructure \
                        + "-seg-label.nrrd"
      destSegFileName = os.path.join(destDir, segFileBaseName)
      shutil.copyfile(segRec.origFileName, destImageFileName)
      shutil.copyfile(segRec.labelFileName, destSegFileName)




if __name__ == "__main__":
  args = cmdlParser.parse_args()
  main = SelectSegmentationsMain(args)
  main.run()


