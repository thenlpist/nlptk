import json
import unittest

from nlptk import PostProcess


class TestStringMethods(unittest.TestCase):
    raw_response = """{'basics': {'name': 'Janith Babaranda', 'label': 'MIE Aust | Project Engineer | Site Engineer | Civil Engineer', 'website': 'www.
linkedin.com/in/janith-nipuna', 'email': 'janithnipunabg@outlook.com', 'phone': '0425 713 822', 'summary': 'I am a dedicated Civil Engineer and a member of Engineers Aust
ralia. I have more than Six Years of extensive experience in construction, planning, and supervising diverse projects. My portfolio includes infrastructure and mixed-deve
lopment projects, including commercial, residential buildings and utility services. Currently residing in Australia, I am eagerly seeking new opportunities to leverage my
 expertise and drive innovation in the field.', 'url': 'www.linkedin.com/in/janith-nipuna', 'profiles': [], 'location': {'city': 'Graceville', 'address': '38 Frank Street
', 'region': 'Queensland', 'countrycode': 'AU', 'postalcode': '4075'}}, 'work': [{'position': 'Project Engineer-Monitoring and Evaluating', 'name': 'Asian Development Ban
k (ADB)', 'location': 'Sri Lanka', 'description': 'Science & Technology Human Resource Development Project (STHRD) -Sri Lanka- US$ 145 million', 'enddate': 'February 2024
', 'startdate': 'January 2023', 'summary': 'Monitored and reported on project progress, managed procurement processes, contributed to bid evaluations, assessed claim stat
us, and verified progress to ensure timely completion and compliance with project standards.', 'highlights': None, 'url': None}, {'position': 'Project Engineer', 'name':
'Hayleys Unisyst Engineering PLC', 'location': 'Colombo, Sri Lanka', 'description': 'Vallibel Mixed Development', 'enddate': 'January 2024', 'startdate': 'August 2021', '
summary': 'Managed and optimized construction efficiencies, minimized delays, coordinated construction lots, maintained documentation, and increased resource allocation e
ffectiveness.', 'highlights': ['Oversaw construction activities, optimised efficiencies, minimised delays, and resolved non-conformances.', 'Reported weekly and monthly p
rogress while identifying and anticipating potential delays.', 'Managed the overall procurement process of the project.', 'Successfully coordinated more than 10 construct
ion lots.', 'Maintained comprehensive documentation.', 'Assigned KPIs for team supervisors, significantly increasing labour productivity.'], 'url': None}, {'position': 'S
ite Engineer', 'name': 'John Keells Holdings PLC', 'location': 'Sri Lanka', 'description': 'Hikka Tranz Hotel Renovation- Cinnamon Hotels & Resorts', 'enddate': 'August 2
021', 'startdate': 'August 2020', 'summary': 'Delivered hotel renovation, supervised fit-out works, collaborated with subcontractors, achieved project milestones, managed
 demolition and strengthening works, participated in meetings.', 'highlights': ['Delivered all levels of the hotel building.', 'Supervised all aspects of finishes and fit
-out works.', 'Collaborated with subcontractors and suppliers.', 'Achieved project milestones using MS Project.', 'Supervised demolition and site work.', 'Participated in
 weekly and monthly project meetings.'], 'url': None}, {'position': 'Site Engineer', 'name': 'Darinton Construction (Pvt)Ltd', 'location': 'Colombo, Sri Lanka', 'descript
ion': 'Design and Construction of Roads & Pavilion at Henry Pedris Playground', 'enddate': 'July 2020', 'startdate': 'August 2019', 'summary': 'Monitored resource procure
ment, managed projects efficiently, reviewed finances, and directed construction utilities and structures.', 'highlights': ['Monitored material procurement, conducted qua
ntity takeoffs.', 'Maintained positive cash flow through budget management.', 'Reviewed subcontractor invoices, variation claims.', 'Supervised construction of buildings,
 structures, and bitumen pavement.', 'Conducted geotechnical investigations.'], 'url': None}, {'position': 'Civil Engineer', 'name': 'Signet Consultants (Pvt) Ltd', 'loca
tion': 'Colombo, Sri Lanka', 'description': 'Structural Design and Construction', 'enddate': 'July 2019', 'startdate': 'January 2019', 'summary': 'Conducted structural an
alyses, reviewed plans, provided technical support, and performed structural health monitoring.', 'highlights': ['Conducted structural analysis and detailed designs.', 'R
eviewed architectural plans, produced drawings.', 'Conducted geotechnical investigations.', 'Provided technical support to quantity surveyors.', 'Performed nondestructive
 testing.'], 'url': None}, {'position': 'Civil Engineer, Intern', 'name': 'NCD Consultants (Pvt) Ltd', 'location': 'Sri Lanka', 'description': '447 Luna Tower Mixed Devel
opment Project', 'enddate': 'October 2018', 'startdate': 'November 2017', 'summary': 'Supervised construction foundation activities, conducted detailed estimations, and o
versaw apartment construction.', 'highlights': ['Supervised construction of the pile raft foundation.', 'Oversaw construction of diaphragm walls and deep excavation.', 'E
stimated concrete volumes and prepared Bar Bending Schedules.', 'Supervised construction of model apartments.', 'Managed building fit-outs and finishes.'], 'url': None}],
 'education': [{'institution': 'University of Moratuwa, Sri Lanka', 'area': 'Construction Project Management', 'studytype': 'Master of Science', 'startdate': 'August 2021
', 'enddate': 'Present', 'url': None, 'score': None}, {'institution': 'University of Moratuwa, Sri Lanka',  'area': 'Civil Engineering (Honours)', 'studytype': 'Bachelor of Engineering', 'startdate': 'September 2014', 'enddate': 'December 2018', 'url': None, 'score': '2nd Class Division (Accredited by the Washington Accord)'}], 'projects': [{'name': 'Comprehensive Design Project - Yudaganawa Township Development Project', 'enddate': '2018', 'startdate': '2017', 'description': 'Project Leader, secured an A+ grade, honoured with the Comprehensive Design Project Award 2018 by the University of Moratuwa for outstanding project execution and design excellence.', 'highlights': ['Designed resilient, sustainable infrastructure.', 'Developed the master plan for harmonising residential and commercial zones.', 'Involved stakeholders and community in planning.'], 'url': None}, {'name': 'Research Project – Mechanical Behavior of Cement Stabilized Mud Concrete Blocks', 'enddate': '2018', 'startdate': '2017', 'description': 'Accomplished project with final thesis achieving an A+ grade.', 'highlights': None, 'url': None}], 'volunteer': [], 'skills': [{'name': 'Civil/Structural Engineering', 'level': 'Expert', 'keywords': None}, {'name': 'Project Management', 'level': 'Expert', 'keywords': None}, {'name': 'Construction', 'level': 'Expert', 'keywords': None}, {'name': 'Procurement', 'level': 'Expert', 'keywords': None}, {'name': 'Cost Controlling', 'level': 'Expert', 'keywords': None}, {'name': 'Health, Safety, Environmental, Quality', 'level': 'Expert', 'keywords': None}, {'name': 'Contract Administration', 'level': 'Expert', 'keywords': None}, {'name': 'Monitor Construction', 'level': 'Expert', 'keywords': None}, {'name': 'Infrastructure Projects', 'level': 'Expert', 'keywords': None}, {'name': 'Mixed- Development Projects', 'level': 'Expert', 'keywords': None}, {'name': 'Buildings', 'level': 'Expert', 'keywords': None}, {'name': 'Utility Services', 'level': 'Expert', 'keywords': None}, {'name': 'Piling', 'level': 'Expert', 'keywords': None}, {'name': 'Bulk-Earth Works', 'level': 'Expert', 'keywords': None}, {'name': 'Geotechnical Engineering', 'level': 'Expert', 'keywords': None}], 'publications': [], 'languages': [], 'awards': [{'title': 'Comprehensive Design Project Award 2018', 'date': None, 'awarder': 'University of Moratuwa', 'summary': 'Awarded for outstanding project execution and design excellence in the Comprehensive Design Project.'}], 'certificates': [], 'references': [], 'interests': []}}

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
