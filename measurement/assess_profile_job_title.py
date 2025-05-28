import base64
import json
import re
from dataclasses import dataclass
from pathlib import Path

import requests
import tqdm
from gliner import GLiNER
from tabulate import tabulate

PORT = "8001"
HOST = "10.0.0.105"
BASE_URL = f"http://{HOST}:{PORT}"


# BASE_URL = f"http://budgie.local:{PORT}"


@dataclass
class Endpoint:
    hello = f"{BASE_URL}/hello"
    static = f"{BASE_URL}/static"
    parse_resume_text = f"{BASE_URL}/parse_resume"
    parse_resume_doc = f"{BASE_URL}/parse_resume_doc"


def main(data_path):
    # dvt = DictVsText()
    nermodel = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")
    data = load_jsonlines(data_path)
    # data = data[50:100]

    score_dict = dict()
    for i, d in enumerate(data[:25]):
        theid = d["id"]
        score, label = check_profile_job_title(d, nermodel, verbose=True)
        score_dict[theid] = label
    print(json.dumps(score_dict, indent=2))

    # ids = [4736023, 233015]
    # data2 = [d for d in data if d["id"] in ids]
    # for d in data2:
    #     print(d["id"])
    #     score, label = check_profile_job_title(d, nermodel, verbose=True)
    #     print("\n\n")

    # check_for_regressions(data[:50], nermodel)


def check_for_regressions(data, nermodel):
    n = len(data)
    label_dict = {
        "218514": "Software Developer",
        "320773": "Assistant Manager and Visual Merchandising Manager",
        "4718483": "",
        "330549": "Senior Director, Customer Success",
        "1406198": "Software Engineer",
        "6877700": "Director Of Food And Beverage",
        "4787238": "Proposal Manager",
        "5471197": "Process Engineer In Tem",
        "3156732": "Business Operation Manager",
        "4642218": "UI/UX Designer, UX Writer, Web Developer",
        "4868071": "Credit Risk Data Specialist",
        "4926205": "",
        "4318155": "Bim Technician",
        "4705985": "QUALITY ASSURANCE & CONTROL LEADER",
        "4650514": "PhD-level Scientist",
        "4923328": "Growth Expert | Enterprise Builder | Team Catalyst",
        "620460": "Senior Product Manager",
        "224940": "Electrical Engineering",
        "4711896": "Financial Accountant",
        "4984690": "",
        "7753150": "Site Engineer",
        "636293": "Machine Learning Engineer",
        "7155098": "Chief Procurement Officer - Vp Procurement|Supply Chain",
        "5305545": "Strategy & Operations Program Manager",
        "4656905": "",
        "147107": "BSN, RN",
        "1199584": "Principal Consultant",
        "4840456": "Chartered Accountant",
        "4627636": "Senior Service and User Experience \nDesigner",
        "135260": "Senior Account Manager| Strategic Client Management | Revenue Growth | Team Leadership",
        "4694409": "Class G Driver",
        "4611626": "dedicated backend developer",
        "4663058": "",
        "425966": "",
        "268334": "Experienced business analyst",
        "4757886": "",
        "308250": "",
        "99114": "data engineer",
        "4834437": "Data Scientist",
        "1930911": "Hr Processes Manager / Hrbp",
        "1964043": "Msc In Engineering Management",
        "4616259": "Software Engineer",
        "143898": "Senior Trader, VP - Municipals",
        "477733": "Assistant Fashion Designer",
        "4708240": "",
        "4818547": "Web Developer",
        "4807050": "",
        "4800740": "HSE Management | Risk Management | HSEMS Management| Technical Leadership",
        "4878818": "Knowledgeable software engineering professional",
        "3363605": ""
    }
    regressions = []
    for d in tqdm.tqdm(data):
        theid = d["id"]
        score, label = check_profile_job_title(d, nermodel, verbose=False)
        ground_truth = label_dict[str(theid)]
        if not label == ground_truth:
            # print(f"Regression on id: {theid}")
            regressions.append(theid)
    print(f"Regressions on id: {regressions}")
    print("Done")


def load_jsonlines(path):
    return [json.loads(x) for x in open(path)]


# response = requests.get(Endpoint.hello)
def test_parse_resume_doc(path: Path):
    filename = path.name
    with open(path, "rb") as fo:
        encoded_string = base64.b64encode(fo.read())

    payload = {"filename": filename, "filedata": encoded_string}
    response = requests.post(url=Endpoint.parse_resume_doc, data=payload)
    return response


def test_parse_resume_txt(text):
    data = {"text": text}
    headers = {"Content-Type": "application/json"}
    response = requests.post(Endpoint.parse_resume_text, headers=headers, data=json.dumps(data))
    return response


def extract_education(text, pattern_dict):
    label = "Education"
    pattern_dict[label] == label
    education = pattern_dict[label]
    entities = []
    # pat1 = re.compile(fr"\n\s?({re.escape(term)})\b", re.IGNORECASE)
    # pat2 = re.compile(fr"\s?({re.escape(term)})\b", re.IGNORECASE)
    for term in education:
        m = re.search(fr"\n\s?({re.escape(term)})", text, re.IGNORECASE)
        if m:
            t = m.group(1)
            start, end = m.span()
            entities.append({
                'start': start,
                'end': end,
                'text': t,
                'labels': label
            }
            )
            break
    if not entities:
        for term in education:
            m = re.search(fr"\s?({re.escape(term)})\b", text, re.IGNORECASE)
            if m:
                t = m.group(1)
                start, end = m.span()
                entities.append({
                    'start': start,
                    'end': end,
                    'text': t,
                    'labels': label
                }
                )
    return entities


def get_profile_job_title(text, nermodel):
    label_threshold = 5
    lines = [x for x in text.split("\n") if x.strip()][:label_threshold]
    text2 = "\n".join(lines)
    labels = ["JobTitle"]
    NER_THRESHOLD = 0.57
    entities = nermodel.predict_entities(text2, labels, threshold=NER_THRESHOLD)
    positions = [e for e in entities if e["label"] == "JobTitle"]
    names = [e for e in entities if e["label"] == "Person"]
    job_title = "" if len(positions) == 0 else positions[0]["text"]
    ignore_list = ["JD"]
    if job_title in ignore_list:
        job_title = ""
    return job_title


def select_correct_job_title(label, ner, text):
    job_title = label
    label_threshold = 5
    lines = [x for x in text.split("\n") if x.strip()][:label_threshold]
    top_text = "\n".join(lines)
    m0 = None if not ner else re.search(re.escape(ner), top_text)
    m = re.search(re.escape(label), top_text)
    if label:
        # print("label not empty")
        # m = re.search(re.escape(label), top_text)
        if m:
            # print("label exists in top_text")
            m2 = re.search(re.escape(ner), label)
            if m2 or label.startswith(ner):
                # print("label starts with NER")
                job_title = label
            if m0 and m:
                if m0.span()[0] < m.span()[0]:
                    job_title = ner
                else:
                    job_title = label
            # else:
            #     print("label does not start with NER")
            #     job_title = ner
        else:
            # print("label does not exist in top_text")
            job_title = ner
    else:
        # print("label is empty")
        job_title = ner

    theline = ""
    for line in top_text.split("\n"):
        m3 = re.search(re.escape(job_title), line)
        if m3:
            theline = line
            # check for COMMA, PIPE
            m4 = re.search(r"^ ?[,|-]", theline[m3.span(0)[1]:])
            if m4:
                extract = theline[m3.span()[0]:]
                extract = re.sub("\s{3,}.*$", "", extract)
                if len(extract) < 100:
                    job_title = extract
            break

    return job_title.strip()


def check_profile_job_title(d, nermodel, verbose=False, predicted_score=None):
    text = d["text"]
    BASIC_THRESHOLD = 8
    lines = [x for x in text.split("\n") if x][:BASIC_THRESHOLD]

    work = re.search(r"\n\s*(work experience|education|professional experience|experience)\s*\n", "\n".join(lines[1:]),
                     re.IGNORECASE)
    if work:
        offset = len(lines[0]) + work.span(1)[0]
        text = text[:offset].strip()

    # lines = text.split("\n")
    basics = "\n".join(lines[:9])
    jr = d["jsonresume"]
    orig_label = jr["basics"]["label"]
    predicted_job_title = get_profile_job_title(text, nermodel)

    # if orig_label == "":
    #     m = None
    # else:
    #     term = re.escape(orig_label)
    #     m = re.search(term, basics)

    label = select_correct_job_title(orig_label, predicted_job_title, text)
    if label == "":
        m = None
    else:
        term = re.escape(label)
        m = re.search(term, basics)

    # TODO:
    # label = label.title()
    # label.replace("\n", "")
    if label and m:
        score = "tp"
    elif label and not m:
        score = "fp"
    elif not label and predicted_job_title != "":
        score = "fn"
    elif not label and not m and predicted_job_title == "":
        score = "tn"

    else:
        print("ERROR:")
        print(f"label:  {label}")
        print(f"m:  {m}")

    if predicted_score and score != predicted_score:
        verbose = True
    if verbose:
        # print(f"score:  {score.upper()} ")
        # print(f"\tlabel:  {label}    orig_label:  {orig_label}  NER: {predicted_job_title}")

        print(d["id"])
        data = [["Score", "Predicted Label", "Original Label", "Gliner Label"],
                [score.upper(), label, orig_label, predicted_job_title]]
        print(tabulate(data, headers="firstrow", tablefmt="grid"))
        print(basics)
        print("\n")
        print("-" * 80)
        print("\n")
    return score, label


if __name__ == "__main__":
    home = Path.home()
    dataset_dir = home.joinpath("Work/ResumeParser_RnD/Train/20250429/v3dataset")
    test_data_path = dataset_dir.joinpath("test.jsonl")  # 4968 records
    validation_data_path = dataset_dir.joinpath("validation.jsonl")  # 14774 records
    gold_data_path = dataset_dir.joinpath("gold.jsonl")  # 481 records

    main(test_data_path)
