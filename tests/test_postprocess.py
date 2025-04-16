import json
import unittest

from nlptk import PostProcess


class TestStringMethods(unittest.TestCase):
    raw_response = """
    {'basics': {'name': 'Janith Babaranda', 'label': 'MIE Aust | Project Engineer | Site Engineer | Civil Engineer', 'website': 'www.l
inkedin.com/in/janith-nipuna', 'email': 'janithnipunabg@outlook.com', 'phone': '0425 713 822', 'summary': 'I am a dedicated Civil Engineer and a member of Engineers Austr
alia. I have more than Six Years of extensive experience in construction, planning, and supervising diverse projects. My portfolio includes infrastructure and mixed-devel
opment projects, including commercial, residential buildings and utility services. Currently residing in Australia, I am eagerly seeking new opportunities to leverage my
expertise and drive innovation in the field.', 'url': 'www.linkedin.com/in/janith-nipuna', 'profiles': [], 'location': {'city': 'Graceville', 'address': '38 Frank Street'
, 'region': '4075', 'countrycode': 'AU', 'postalcode': '4075'}}, 'work': [{'position': 'Project Engineer-Monitoring and Evaluating', 'name': 'Asian Development Bank (ADB)
', 'location': 'Sri Lanka', 'description': 'Project- Science & Technology Human Resource Development Project (STHRD) - Sri Lanka- US$ 145 million', 'enddate': 'February 2
024', 'startdate': 'January 2023', 'summary': 'Monitored and reported on project progress, managed procurement processes, contributed to bid evaluations, assessed claim s
tatus, and verified project progress to ensure timely completion and compliance with project standards.', 'highlights': None, 'url': None}, {'position': 'Project Engineer
', 'name': 'Hayleys Unisyst Engineering PLC', 'location': 'Colombo, Sri Lanka', 'description': 'Project-Vallibel Mixed Development', 'enddate': 'January 2024', 'startdate
': 'August 2021', 'summary': 'Oversaw construction activities optimizing efficiencies and minimizing delays to adhere to budgets, scopes, and timelines. Managed procureme
nt, coordinated project phases, and maintained documentation ensuring project quality.', 'highlights': ['Reported weekly and monthly progress optimizing resource allocati
on through critical path analysis', 'Managed the overall procurement process ensuring timely delivery of materials', 'Coordinated construction lots for structural steel,
concrete, and building services', 'Maintained documentation including QCPs, ITPs, RFIs, and SWMS', 'Set and assigned KPIs increasing labour productivity up to 20%'], 'url
': None}, {'position': 'Site Engineer', 'name': 'John Keells Holdings PLC', 'location': 'Sri Lanka', 'description': 'Project-Hakka Tranz Hotel Renovation- Cinnamon Hotels
 & Resorts', 'enddate': 'August 2021', 'startdate': 'August 2020', 'summary': 'Supervised delivery of the entire hotel building and completed all civil works on time, col
laborated with subcontractors, maintained HSEQ standards, and achieved project milestones.', 'highlights': ['Supervised finishes and fit-out works', 'Collaborated with su
bcontractors and suppliers for timely delivery', 'Achieved zero lost time injuries', 'Utilized MS Project for tracking and reporting', 'Participated in project meetings t
o discuss site issues'], 'url': None}, {'position': 'Site Engineer', 'name': 'Darinton Construction (Pvt)Ltd', 'location': 'Colombo, Sri Lanka', 'description': 'Project-D
esign and Construction of the Roads & Pavillion at Henry Pedris Playground', 'enddate': 'July 2020', 'startdate': 'August 2019', 'summary': 'Monitored material procuremen
t, managed construction tasks, and conducted geotechnical investigations supporting the development of the internal road network.', 'highlights': ['Conducted material pro
curement and efficient resource utilization', 'Maintained budget control through precise forecasting', 'Oversaw tasks, excavation, backfilling, and installation of draina
ge systems', 'Conducted geotechnical investigations for soil conditions'], 'url': None}, {'position': 'Civil Engineer', 'name': 'Signet Consultants (Pvt) Ltd', 'location'
: 'Colombo, Sri Lanka', 'description': 'Structural Design and Construction', 'enddate': 'July 2019', 'startdate': 'January 2019', 'summary': 'Conducted structural analysi
s and designs, provided technical support, and conducted geotechnical investigations for project optimization.', 'highlights': ['Utilized ETABS, SAP2000, and Prokon for s
tructural analysis', 'Reviewed architectural plans for accuracy', 'Provided support for compiling BOQs and BOMs', 'Performed nondestructive testing and core testing'], 'u
rl': None}, {'position': 'Civil Engineer, Intern', 'name': 'NCD Consultants (Pvt) Ltd', 'location': 'Colombo, Sri Lanka', 'description': '447 Luna Tower Mixed Development
 Project', 'enddate': 'October 2018', 'startdate': 'November 2017', 'summary': 'Supervised construction of the pile raft foundation and oversaw various construction activ
ities ensuring structural integrity.', 'highlights': ['Supervised construction of pile raft foundation, diaphragm walls, and deep excavation', 'Estimated concrete volumes
 for structural members', 'Managed building fit-outs and interior designs for model apartments'], 'url': None}], 'education': [{'institution': 'University of Moratuwa Sri Lanka', 'area': 'Construction Project Management', 'studytype': 'Master of Science', 'startdate': 'August 2021', 'enddate': 'Present', 'url': None, 'score': None}, {'institution': 'University of Moratuwa, Sri Lanka', 'area': 'Civil Engineering', 'studytype': 'Bachelor of Engineering (Honours)', 'startdate': 'September 2014', 'enddate': 'December 2018', 'url': None, 'score': '2nd Class Division (Accredited by the Washington Accord)'}], 'projects': [{'name': 'Comprehensive Design Project -Yudaganawa Township Development Project', 'enddate': '2018', 'startdate': '2017', 'description': 'Served as Project Leader for the township development project, ensuring design excellence and achieving an A+ grade.', 'highlights': ['Designed resilient, sustainable infrastructure', 'Developed master plan for residential and commercial zones', 'Involved stakeholders in planning to gather feedback'], 'url': None}, {'name': 'Research Project – Mechanical Behavior of Cement Stabilized Mud Concrete Blocks', 'enddate': '2018', 'startdate': '2017', 'description': 'Completed project with final thesis, achieving an A+ grade.', 'highlights': None, 'url': None}], 'volunteer': [], 'skills': [{'name': 'Civil/Structural Engineering', 'level': 'Advanced', 'keywords': None}, {'name': 'Project Management', 'level': 'Advanced', 'keywords': None}, {'name': 'Construction', 'level': 'Advanced', 'keywords': None}, {'name': 'Procurement', 'level': 'Advanced', 'keywords': None}, {'name': 'Cost Controlling', 'level': 'Advanced', 'keywords': None}, {'name': 'Health, Safety, Environmental, Quality (HSEQ)', 'level': 'Advanced', 'keywords': None}, {'name': 'Contract Administration', 'level': 'Advanced', 'keywords': None}, {'name': 'Monitor Construction', 'level': 'Advanced', 'keywords': None}, {'name': 'Infrastructure Projects', 'level': 'Advanced', 'keywords': None}, {'name': 'Mixed-Development Projects', 'level': 'Advanced', 'keywords': None}, {'name': 'Buildings', 'level': 'Advanced', 'keywords': None}, {'name': 'Utility Services', 'level': 'Advanced', 'keywords': None}, {'name': 'Piling', 'level': 'Advanced', 'keywords': None}, {'name': 'Bulk-Earth Works',  'level': 'Advanced', 'keywords': None}, {'name': 'Geotechnical Engineering', 'level': 'Advanced', 'keywords': None}], 'publications': [], 'languages': [], 'awards': [], 'certificates': [], 'references': [{'name': 'Available upon request', 'reference': None}], 'interests': []}
    """

    def test_validation(self):
        pp = PostProcess()
        result, is_valid_json, is_valid_jsonresume = pp.postprocess(self.raw_response)
        print()
        print(f"is_valid_json:        {is_valid_json}")
        print(f"is_valid_jsonresume:  {is_valid_jsonresume}")
        print()
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    unittest.main()
