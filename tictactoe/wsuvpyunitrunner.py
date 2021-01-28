# reference: https://github.com/python/cpython/blob/master/Lib/unittest/runner.py


import sys
import time
import json

import unittest
from unittest import result
from unittest import TextTestResult

# Utility functions for deriving automatic stage and label names from a test object

def stageFromTest(test):
    namestr = type(test).__name__
    if namestr.endswith("Tests"):
        namestr = namestr[:-len("Tests")]
    return namestr

def labelFromTest(test):
    namestr = test._testMethodName
    if namestr.startswith("test"):
        namestr = namestr[len("test"):]
    return namestr

def simpleHintFromErr( err):
    _, value, _ = err
    return str(value)


# Extension of TextTestResult that builds up semantic JSON in a dictionary

class WSUVTextTestResult(TextTestResult):
    def __init__(self, *args, **kwargs):
        super(WSUVTextTestResult, self).__init__(*args, **kwargs)

        # This will be just like the failures and errors members
        self.successes = []

        self._allSemanticResults = dict()

        self._allSemanticResults["_presentation"] = "semantic"
        self._allSemanticResults["stages"] = []

    def _addItemToStage(self, stage, label, data):
        self._addStageIfNotExists(stage)
        self._allSemanticResults[stage][label] = data

    def _addStageIfNotExists(self, stageName):
        if stageName not in self._allSemanticResults["stages"]:
            self._allSemanticResults["stages"].append(stageName)
            self._allSemanticResults[stageName] = dict()

    def registerSemanticFailureMetadata(self, stage, label, optionalHint=""):
        meta = { "passed": False, "hint": optionalHint }
        self._addItemToStage(stage, label, meta)

    def registerSemanticSuccessMetadata(self, stage, label):
        meta = { "passed": True }
        self._addItemToStage(stage, label, meta)

    def registerSemanticMetadata(self, stage, label, value):
        self._addItemToStage(stage, label, value)

    def addSuccess(self, test):
        # Fires on the success of a test
        super(WSUVTextTestResult, self).addSuccess(test)
        self.successes.append(test)
        self.registerSemanticSuccessMetadata(stageFromTest(test), labelFromTest(test))

    def addError(self, test: unittest.case.TestCase, err) -> None:
        super(WSUVTextTestResult, self).addError(test, err)
        self.registerSemanticFailureMetadata(stageFromTest(test), labelFromTest(test), simpleHintFromErr(err))

    def addFailure(self, test: unittest.case.TestCase, err) -> None:
        super(WSUVTextTestResult, self).addFailure(test, err)
        self.registerSemanticFailureMetadata(stageFromTest(test), labelFromTest(test), simpleHintFromErr(err))

# A TextTestRunner that opens a config file before testing and uses the
# WSUVTextTestResult class to access semantic feedback

class WSUVTextTestRunner(unittest.TextTestRunner):
    resultclass = WSUVTextTestResult

    def __init__(self, **kwargs):
        """Construct a TextTestRunner.

        Subclasses should accept **kwargs to ensure compatibility as the
        interface changes.
        """
        super(WSUVTextTestRunner, self).__init__(**kwargs)


    def run(self, test):
        "Run the given test case or test suite."

        # Load the json file first, so a student can't overwrite it...
        with open('wsuvtest.json') as fin:
            config = json.load(fin)

        result = super(WSUVTextTestRunner, self).run(test)
        run = result.testsRun
        failed, errored = 0,0
        if not result.wasSuccessful():
            failed, errored = len(result.failures), len(result.errors)
        pts = (run-failed-errored)*1.0*config['scores']['Correctness']/run

        return "\n".join([
            "Total points %.1f out of %.1f"%(pts, config['scores']['Correctness']),  # Normal text piece
            json.dumps(result._allSemanticResults),                                  # Semantic Feedback (with stages) piece
            '{"scores": {"Correctness": %.1f}}'%(pts)                                # Scoring piece
        ])

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='store_true')
    args = parser.parse_args()
    
    test_modules = unittest.defaultTestLoader.discover(start_dir='.',
                                                       pattern='*tests.py',
                                                       top_level_dir=None)

    try:
        fout = sys.stdout
        if args.f:
            fout = open('wsuvpyunitrunner.out', 'wt')
            
        runner = WSUVTextTestRunner(verbosity=5, stream=fout)
        result = runner.run(test_modules)
        print(result, file=fout)
    finally:
        if args.f and fout:
            fout.close()
