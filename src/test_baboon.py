import baboon

import collections
import unittest


class BaboonsTest(unittest.TestCase):

    def setUp(self):
        self.orDict = collections.OrderedDict()
        baboon.setup_keys(self.orDict)

    def test_baboon1_should_be_poly(self):
        self.assertEqual(self.orDict["nrOfPolyType1"], 0)
        baboon.accumulate_poly(2, 0, 0, self.orDict)
        self.assertEqual(self.orDict["nrOfPolyType1"], 1)

    def test_baboon2_should_be_poly(self):
        self.assertEqual(self.orDict["nrOfPolyType2"], 0)
        baboon.accumulate_poly(0, 2, 0, self.orDict)
        self.assertEqual(self.orDict["nrOfPolyType2"], 1)

    def test_baboon3_should_be_poly(self):
        self.assertEqual(self.orDict["nrOfPolyType3"], 0)
        baboon.accumulate_poly(0, 0, 2, self.orDict)
        self.assertEqual(self.orDict["nrOfPolyType3"], 1)

    def test_baboon1And2_should_be_poly(self):
        self.assertEqual(self.orDict["nrOfPolyType1And2"], 0)
        baboon.accumulate_poly(2, 2, 0, self.orDict)
        self.assertEqual(self.orDict["nrOfPolyType1And2"], 1)

    def test_baboon1And3_should_be_poly(self):
        self.assertEqual(self.orDict["nrOfPolyType1And3"], 0)
        baboon.accumulate_poly(2, 0, 2, self.orDict)
        self.assertEqual(self.orDict["nrOfPolyType1And3"], 1)

    def test_baboon2And3_should_be_poly(self):
        self.assertEqual(self.orDict["nrOfPolyType2And3"], 0)
        baboon.accumulate_poly(0, 2, 2, self.orDict)
        self.assertEqual(self.orDict["nrOfPolyType2And3"], 1)

    def test_baboon1And2_for_each_key__should_be_poly(self):
        self.assertEqual(self.orDict["nrOfPolyType1"], 0)
        self.assertEqual(self.orDict["nrOfPolyType2"], 0)
        self.assertEqual(self.orDict["nrOfPolyType1And2"], 0)
        baboon.accumulate_poly(2, 2, 0, self.orDict)
        self.assertEqual(self.orDict["nrOfPolyType1"], 1)
        self.assertEqual(self.orDict["nrOfPolyType2"], 1)
        self.assertEqual(self.orDict["nrOfPolyType1And2"], 1)

    def test_type_not_zero_for_baboon1(self):
        self.assertEqual(self.orDict["typeNotZero"], 0)
        baboon.accumulate_type_not_zero(1, 0, 0, self.orDict)
        self.assertEqual(self.orDict["typeNotZero"], 1)

    def test_type_not_zero_for_baboon1And2(self):
        self.assertEqual(self.orDict["typeNotZero"], 0)
        baboon.accumulate_type_not_zero(1, 1, 0, self.orDict)
        self.assertEqual(self.orDict["typeNotZero"], 1)

    def test_baboon2_baboon3_should_give_statea(self):
        # State A (011)
        self.assertEqual(self.orDict["nrOfStateA"], 0)
        currentState = 0
        currentState, out = baboon.accumulate_state(0, 1, 1,
                                                    currentState, self.orDict)
        self.assertEqual(self.orDict["nrOfStateA"], 1)
        self.assertEqual(currentState, 1)
        self.assertTrue(out)

    def test_baboon1_baboon3_should_give_statea(self):
        # State B (101)
        self.assertEqual(self.orDict["nrOfStateB"], 0)
        currentState = 0
        currentState, out = baboon.accumulate_state(1, 0, 1,
                                                    currentState, self.orDict)
        self.assertEqual(self.orDict["nrOfStateB"], 1)
        self.assertEqual(currentState, 2)
        self.assertTrue(out)

    def test_baboon1_baboon2_should_give_statea(self):
        # State C (110)
        self.assertEqual(self.orDict["nrOfStateC"], 0)
        currentState = 0
        currentState, out = baboon.accumulate_state(1, 1, 0,
                                                    currentState, self.orDict)
        self.assertEqual(self.orDict["nrOfStateC"], 1)
        self.assertEqual(currentState, 3)
        self.assertTrue(out)

    def test_should_not_give_a_state(self):
        currentState, out = baboon.accumulate_state(2, 2, 2, 0, self.orDict)
        self.assertEqual(currentState, 0)
        self.assertFalse(out)

    def test_last_state_none(self):
        currentState = baboon.accumulate_state_changed(0, 1, self.orDict)
        self.assertEqual(currentState, 1)

    def test_from_stateA_to_stateA(self):
        self.assertEqual(self.orDict["stateAToA"], 0)
        currentState = baboon.accumulate_state_changed(1, 1, self.orDict)
        self.assertEqual(self.orDict["stateAToA"], 1)
        self.assertEqual(currentState, 1)

    def test_from_stateA_to_stateB(self):
        self.assertEqual(self.orDict["stateAToB"], 0)
        currentState = baboon.accumulate_state_changed(1, 2, self.orDict)
        self.assertEqual(self.orDict["stateAToB"], 1)
        self.assertEqual(currentState, 2)

    def test_from_stateA_to_stateC(self):
        self.assertEqual(self.orDict["stateAToC"], 0)
        currentState = baboon.accumulate_state_changed(1, 3, self.orDict)
        self.assertEqual(self.orDict["stateAToC"], 1)
        self.assertEqual(currentState, 3)

    def test_from_stateB_to_stateC(self):
        self.assertEqual(self.orDict["stateBToC"], 0)
        currentState = baboon.accumulate_state_changed(2, 3, self.orDict)
        self.assertEqual(self.orDict["stateBToC"], 1)
        self.assertEqual(currentState, 3)

    def test_from_stateC_to_stateB(self):
        self.assertEqual(self.orDict["stateCToB"], 0)
        currentState = baboon.accumulate_state_changed(3, 2, self.orDict)
        self.assertEqual(self.orDict["stateCToB"], 1)
        self.assertEqual(currentState, 2)

    def test_from_stateA_to_stateB_to_stateC(self):
        self.assertEqual(self.orDict["stateAToB"], 0)
        self.assertEqual(self.orDict["stateBToC"], 0)
        currentState = baboon.accumulate_state_changed(1, 2, self.orDict)
        self.assertEqual(self.orDict["stateAToB"], 1)
        self.assertEqual(currentState, 2)
        currentState = baboon.accumulate_state_changed(2, 3, self.orDict)
        self.assertEqual(self.orDict["stateBToC"], 1)
        self.assertEqual(currentState, 3)

if __name__ == "__main__":
    unittest.main()
