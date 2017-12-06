import json

class ConditionsParser(object):
  """
  Parses argrparse cmdl arguments to extract conditions to filter mpReview data.
  Resulting filter onditions are provided as dictonary.
  """

  def __init__(self, args):
    self._args = args
    self._cmdlArgToPropertyNameMap = {"readers": "reader", 
                                      "structures": "segmentedStructure",
                                      "studies": "study",
                                      "series": "series",
                                      "types": "canonicalType"}



  def getFilterConditions(self):
    if self._args.conditionsFile:
      return self._getFilterConditionsFromConditionsFile(self._args.conditionsFile)
    else:
      return self._getFilterConditionsFromCmdlArgs(self._args)


  def _getFilterConditionsFromConditionsFile(self, conditionsFile):
    with open(conditionsFile, "r") as jsonFile:
      config = json.load(jsonFile)
      return self._convertToFilterConditions(config)


  def _getFilterConditionsFromCmdlArgs(self, args):
    config = vars(args)
    return self._convertToFilterConditions(config)


  def _convertToFilterConditions(self, config):
    filterConditions = {}
    for key, value in config.items():
      if self._cmdlArgToPropertyNameMap.has_key(key) and value is not None:
        filterConditions[self._cmdlArgToPropertyNameMap[key]] = value
    return filterConditions




