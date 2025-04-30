import json
import unittest

from nlptk import PostProcess

import json
import unittest

from nlptk import JRValidate
from nlptk import JRMetrics
from pathlib import Path


class DemoJsonResumeAnalysis(unittest.TestCase):
    home = Path.home()
    data_dir = home.joinpath("Data/Jobscan/Resumes/v1.1model_analysis/data2")
    inpath = data_dir.joinpath("merged_data.jsonl")
    data = [json.loads(x) for x in open(inpath)]

    def test_dict_v_dict(self):
        idx = 0
        d = self.data[idx]
        jrm = JRMetrics(approach="regex")
        dvd_1 = jrm.measure_dict_v_dict(d, "jsonresume_rchilli", "jsonresume_v2")
        print(json.dumps(dvd_1, indent=2))

    def test_dict_v_text(self):
        idx = 0
        d = self.data[idx]

        jrm = JRMetrics(approach="regex")
        dvt_2, left_over = jrm.measure_dict_v_text(d, "jsonresume_v2", remainder=True)
        print(json.dumps(dvt_2, indent=2))
        print()
        print("-" * 80)
        print("Unextracted Text")
        print("-" * 80)
        print(left_over)


if __name__ == '__main__':
    unittest.main()
