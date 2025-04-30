import json
from pathlib import Path
# from compare_dict_to_text import compute_dict_v_text
# from compare_dicts import compute_dict_v_dict
from nlptk.jrmetrics.compare_dicts import compute_dict_v_dict
from nlptk.jrmetrics.compare_dict_to_text import compute_dict_v_text
# from nlptk import aggregate_similarity


class JRMetrics:

    def __init__(self, approach, threshold=0.8):
        self.approach = approach
        self.threshold = threshold

    def measure_dict_v_text(self, data: dict, colname, remainder:bool = False):
        text = data["text"]
        jsonresume = data[colname]
        return compute_dict_v_text(text, jsonresume, self.approach, remainder=remainder)

    def measure_dict_v_dict(self, data: dict, colname1, colname2):
        dict1 = data[colname1]
        dict2 = data[colname2]
        return compute_dict_v_dict(dict1, dict2, threshold=self.threshold)


# Example usage
if __name__ == "__main__":
    home = Path.home()
    sample_path = home.joinpath("Data/Jobscan/Resumes/v1.1model_analysis/data2/merged_sample.json")
    data = json.loads(open(sample_path).read())

    jrm = JRMetrics(approach="regex")
    dvt_1 = jrm.measure_dict_v_text(data, "jsonresume_rchilli")
    dvt_2 = jrm.measure_dict_v_text(data, "jsonresume_v1")
    dvt_3 = jrm.measure_dict_v_text(data, "jsonresume_v2")

    print("\n\nComparison: dict vs text")
    print("-" * 80)
    print("rchilli vs v1:")
    print(json.dumps(dvt_1["metrics"]))
    print("rchilli vs v2:")
    print(json.dumps(dvt_2["metrics"]))
    print("v1 vs v2:")
    print(json.dumps(dvt_3["metrics"]))

    dvd_1 = jrm.measure_dict_v_dict(data, "jsonresume_rchilli", "jsonresume_v1")
    dvd_2 = jrm.measure_dict_v_dict(data, "jsonresume_rchilli", "jsonresume_v2")
    dvd_3 = jrm.measure_dict_v_dict(data, "jsonresume_v1", "jsonresume_v2")

    print("\n\nComparison: dict vs dict")
    print("-" * 80)
    print("rchilli vs v1:")
    print(json.dumps(dvd_1["metrics"]))
    print("rchilli vs v2:")
    print(json.dumps(dvd_2["metrics"]))
    print("v1 vs v2:")
    print(json.dumps(dvd_3["metrics"]))
