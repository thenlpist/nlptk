import unittest

from nlptk.jrmetrics.compare_dict_to_text import *


class TestPostProcessingListItems(unittest.TestCase):
    text = """
                Name: Ethan Carter 
                Email: [ethan.carter@fictionalmail.com](mailto:ethan.carter@fictionalmail.com)LinkedIn: linkedin.com/in/ethan-carter 
                Phone: +1 (555) 123-4567
                
                Professional Summary
                
                Highly skilled and detail-oriented software developer with expertise in multiple programming languages, databases, frameworks, and cloud technologies. Proven ability to design, develop, and deploy scalable applications and systems. Adept at collaborating with cross-functional teams to deliver innovative solutions.
                
                Languages: Java, Python, R, HTML, CSS, JavaScript, C, C++, SAP ABAP, MATLAB Databases: SQL, MySQL, Oracle DB, MongoDB, SAP HANA Frameworks: React.js, Node.js, Maven, Junit4, Mongoose, REST API Cloud Technologies: AWS (IAM, EC2, S3, EBS, RDS, DynamoDB VPC, Lambda), SAP HANA Cloud Platforms: Git, GitHub, IntelliJ, Eclipse, Visual Studio, Jupyter Notebook, RStudio.
                
                Professional Experience
                
                Software Developer 
                Tech Innovators Inc. – San Francisco, CA 
                June 2021 – Present
                
                - Developed and maintained scalable web applications using React.js and Node.js, ensuring high performance and responsiveness.
                - Designed and implemented RESTful APIs to facilitate seamless communication between front-end and back-end systems.
                - Utilized AWS services (EC2, S3, RDS, Lambda) to deploy and manage cloud-based applications, reducing infrastructure costs by 20%.
                - Collaborated with data scientists to build predictive models using Python and R, integrating them into production systems.
                - Optimized database queries and improved data retrieval times by 30% using SQL and MongoDB.
                
                Junior Developer 
                CodeCraft Solutions – Austin, TX 
                January 2019 – May 2021
                
                - Assisted in the development of enterprise-level applications using Java and SAP ABAP, ensuring compliance with client requirements.
                - Conducted unit testing using Junit4 and Maven, improving code quality and reducing bugs by 25%.
                - Worked with cross-functional teams to migrate legacy systems to SAP HANA Cloud, enhancing system performance and scalability.
                - Contributed to the development of data visualization tools using MATLAB and RStudio, enabling better decision-making for stakeholders.
                
                Intern – Software Development 
                InnovateTech Labs – Seattle, WA 
                May 2018 – December 2018
                
                - Supported senior developers in building and maintaining web applications using HTML, CSS, and JavaScript.
                - Gained hands-on experience with Git and GitHub for version control and collaborative development.
                - Assisted in the deployment of applications on AWS, gaining exposure to cloud infrastructure and services.
                - Participated in code reviews and debugging sessions, improving overall code quality and team efficiency.
                
                Education
                
                Bachelor of Science in Computer Science 
                University of California, Berkeley – Berkeley, CA 
                Graduated: May 2018
                
                Certifications
                
                - AWS Certified Solutions Architect – Associate
                - SAP Certified Development Associate – ABAP with SAP NetWeaver
                - Oracle Certified Professional: MySQL Database Administrator
                
                Projects
                
                E-Commerce Platform Development
                
                - Built a full-stack e-commerce platform using React.js, Node.js, and MongoDB.
                - Integrated AWS services (S3, EC2, RDS) for storage, hosting, and database management.
                - Implemented REST APIs for seamless communication between front-end and back-end systems.
                
                Data Analysis and Visualization Tool
                
                - Developed a data analysis tool using Python and R, enabling users to visualize complex datasets.
                - Integrated the tool with Jupyter Notebook and RStudio for interactive data exploration.
                - Deployed the application on AWS Lambda for scalable and cost-effective performance.
                
                SAP HANA Cloud Migration
                
                - Led a team to migrate a legacy SAP system to SAP HANA Cloud, improving system performance by 40%.
                - Optimized database queries and reduced data retrieval times by 25%.
                - Ensured seamless integration with existing systems and minimal downtime during migration.
                
                Interests
                
                - Open-source contributions
                - Machine learning and AI
                - Cloud computing and DevOps
                - Data science and analytics
                """

    def test_dvt_20250327(self):
        d = {
            "language": "en",
            "statuscode": 200,
            "parser": "foobar",
            "parser_version": "0.0.0",
            "generation_time": 286.1292917728424,
            "num_chars": 4003,
            "num_tokens": 1058,
            "jsonresume": {
                "basics": {
                    "name": "Ethan Carter",
                    "label": "Software Developer",
                    "email": "ethan.carter@fictionalmail.com",
                    "website": "",
                    "phone": "(555) 123-4567",
                    "url": "linkedin.com/in/ethan-carter",
                    "summary": "Highly skilled and detail-oriented software developer with expertise in multiple programming languages, databases, frameworks, and cloud technologies. Proven ability to design, develop, and deploy scalable applications and systems. Adept at collaborating with cross-functional teams to deliver innovative solutions.",
                    "location": {},
                    "profiles": [
                        {
                            "url": "https://linkedin.com/in/ethan-carter",
                            "network": "Linkedin",
                            "username": ""
                        },
                        {
                            "url": "React.js",
                            "network": "",
                            "username": ""
                        },
                        {
                            "url": "Node.js",
                            "network": "",
                            "username": ""
                        }
                    ]
                },
                "work": [
                    {
                        "name": "Tech Innovators Inc.",
                        "position": "Software Developer",
                        "url": "",
                        "location": "San Francisco",
                        "startDate": "2021-06-15",
                        "endDate": "",
                        "summary": "",
                        "highlights": [
                            "Developed and maintained scalable web applications using React.js and Node.js, ensuring high performance and responsiveness.",
                            "Designed and implemented RESTful APIs to facilitate seamless communication between front-end and back-end systems.",
                            "Utilized AWS services (EC2, S3, RDS, Lambda) to deploy and manage cloud-based applications, reducing infrastructure costs by 20%.",
                            "Collaborated with data scientists to build predictive models using Python and R, integrating them into production systems.",
                            "Optimized database queries and improved data retrieval times by 30% using SQL and MongoDB."
                        ]
                    },
                    {
                        "name": "CodeCraft Solutions",
                        "position": "Junior Developer",
                        "url": "",
                        "location": "Austin",
                        "startDate": "2019-01-15",
                        "endDate": "2021-05-15",
                        "summary": "",
                        "highlights": [
                            "Assisted in the development of enterprise-level applications using Java and SAP ABAP, ensuring compliance with client requirements.",
                            "Conducted unit testing using Junit4 and Maven, improving code quality and reducing bugs by 25%.",
                            "Worked with cross-functional teams to migrate legacy systems to SAP HANA Cloud, enhancing system performance and scalability.",
                            "Contributed to the development of data visualization tools using MATLAB and RStudio, enabling better decision-making for stakeholders."
                        ]
                    },
                    {
                        "name": "InnovateTech Labs",
                        "position": "Intern - Software Development",
                        "url": "",
                        "location": "Seattle",
                        "startDate": "2018-05-15",
                        "endDate": "2018-12-15",
                        "summary": "",
                        "highlights": [
                            "Supported senior developers in building and maintaining web applications using HTML, CSS, and JavaScript.",
                            "Gained hands-on experience with Git and GitHub for version control and collaborative development.",
                            "Assisted in the deployment of applications on AWS, gaining exposure to cloud infrastructure and services.",
                            "Participated in code reviews and debugging sessions, improving overall code quality and team efficiency."
                        ]
                    }
                ],
                "education": [
                    {
                        "institution": "University of California",
                        "url": "",
                        "area": "Computer Science",
                        "studyType": "Bachelor of Science",
                        "startDate": "",
                        "endDate": "2018-05-15",
                        "score": "",
                        "minors": [],
                        "courses": []
                    }
                ],
                "projects": [],
                "volunteer": [],
                "skills": [
                    {
                        "name": "Languages : Java",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "Python",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "R",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "HTML",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "CSS",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "JavaScript",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "C",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "C++",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "SAP ABAP",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "MATLAB",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "Databases : SQL",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "MySQL",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "Oracle DB",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "MongoDB",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "SAP HANA",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "React.js",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "Node.js",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "Maven",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "Junit4",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "Mongoose",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "REST API",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "Cloud Technologies : AWS (IAM",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "EC2",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "S3",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "EBS",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "RDS",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "DynamoDB VPC",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "Lambda)",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "SAP HANA Cloud Platforms : Git",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "GitHub",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "IntelliJ",
                        "level": "",
                        "keywords": []
                    }
                ],
                "publications": [],
                "languages": [],
                "awards": [],
                "certificates": [],
                "references": [],
                "interests": []
            },
            "is_valid_json": True,
            "is_valid_jsonresume": True,
            "confidence": {
                "basics": {
                    "name": 0.0,
                    "email": 0.0,
                    "label": 0.0,
                    "phone": 0.0,
                    "location": {
                        "city": 0.0,
                        "region": 0.0,
                        "address": 0.0,
                        "postalCode": 0.0,
                        "countryCode": 0.0
                    }
                },
                "work": [
                    {
                        "name": 1.0,
                        "location": 1.0,
                        "position": 1.0
                    },
                    {
                        "name": 1.0,
                        "location": 1.0,
                        "position": 1.0
                    },
                    {
                        "name": 1.0,
                        "location": 1.0,
                        "position": 0.0
                    }
                ],
                "education": [
                    {
                        "institution": 1.0,
                        "studyType": 1.0,
                        "area": 1.0
                    }
                ]
            },
            "text": "Name: Ethan Carter \nEmail: [ethan.carter@fictionalmail.com](mailto:ethan.carter@fictionalmail.com)LinkedIn: linkedin.com/in/ethan-carter \nPhone: +1 (555) 123-4567\n\nProfessional Summary\n\nHighly skilled and detail-oriented software developer with expertise in multiple programming languages, databases, frameworks, and cloud technologies. Proven ability to design, develop, and deploy scalable applications and systems. Adept at collaborating with cross-functional teams to deliver innovative solutions.\n\nLanguages: Java, Python, R, HTML, CSS, JavaScript, C, C++, SAP ABAP, MATLAB Databases: SQL, MySQL, Oracle DB, MongoDB, SAP HANA Frameworks: React.js, Node.js, Maven, Junit4, Mongoose, REST API Cloud Technologies: AWS (IAM, EC2, S3, EBS, RDS, DynamoDB VPC, Lambda), SAP HANA Cloud Platforms: Git, GitHub, IntelliJ, Eclipse, Visual Studio, Jupyter Notebook, RStudio.\n\nProfessional Experience\n\nSoftware Developer \nTech Innovators Inc. \u2013 San Francisco, CA \nJune 2021 \u2013 Present\n\n- Developed and maintained scalable web applications using React.js and Node.js, ensuring high performance and responsiveness.\n- Designed and implemented RESTful APIs to facilitate seamless communication between front-end and back-end systems.\n- Utilized AWS services (EC2, S3, RDS, Lambda) to deploy and manage cloud-based applications, reducing infrastructure costs by 20%.\n- Collaborated with data scientists to build predictive models using Python and R, integrating them into production systems.\n- Optimized database queries and improved data retrieval times by 30% using SQL and MongoDB.\n\nJunior Developer \nCodeCraft Solutions \u2013 Austin, TX \nJanuary 2019 \u2013 May 2021\n\n- Assisted in the development of enterprise-level applications using Java and SAP ABAP, ensuring compliance with client requirements.\n- Conducted unit testing using Junit4 and Maven, improving code quality and reducing bugs by 25%.\n- Worked with cross-functional teams to migrate legacy systems to SAP HANA Cloud, enhancing system performance and scalability.\n- Contributed to the development of data visualization tools using MATLAB and RStudio, enabling better decision-making for stakeholders.\n\nIntern \u2013 Software Development \nInnovateTech Labs \u2013 Seattle, WA \nMay 2018 \u2013 December 2018\n\n- Supported senior developers in building and maintaining web applications using HTML, CSS, and JavaScript.\n- Gained hands-on experience with Git and GitHub for version control and collaborative development.\n- Assisted in the deployment of applications on AWS, gaining exposure to cloud infrastructure and services.\n- Participated in code reviews and debugging sessions, improving overall code quality and team efficiency.\n\nEducation\n\nBachelor of Science in Computer Science \nUniversity of California, Berkeley \u2013 Berkeley, CA \nGraduated: May 2018\n\nCertifications\n\n- AWS Certified Solutions Architect \u2013 Associate\n- SAP Certified Development Associate \u2013 ABAP with SAP NetWeaver\n- Oracle Certified Professional: MySQL Database Administrator\n\nProjects\n\nE-Commerce Platform Development\n\n- Built a full-stack e-commerce platform using React.js, Node.js, and MongoDB.\n- Integrated AWS services (S3, EC2, RDS) for storage, hosting, and database management.\n- Implemented REST APIs for seamless communication between front-end and back-end systems.\n\nData Analysis and Visualization Tool\n\n- Developed a data analysis tool using Python and R, enabling users to visualize complex datasets.\n- Integrated the tool with Jupyter Notebook and RStudio for interactive data exploration.\n- Deployed the application on AWS Lambda for scalable and cost-effective performance.\n\nSAP HANA Cloud Migration\n\n- Led a team to migrate a legacy SAP system to SAP HANA Cloud, improving system performance by 40%.\n- Optimized database queries and reduced data retrieval times by 25%.\n- Ensured seamless integration with existing systems and minimal downtime during migration.\n\nInterests\n\n- Open-source contributions\n- Machine learning and AI\n- Cloud computing and DevOps\n- Data science and analytics"
        }

        d["text"] = self.text
        metrics = main(d)
        assert metrics["pct_extracted"] > 0.72
        print("\n\n")
        print(json.dumps(metrics, indent=2))
        """
          "metrics": {
              "aggregated_similarity": 0.806,
              "aggregated_match": false,
              "input_text_len": 5269,
              "extracted_text_len": 3814,
              "remainder_text_len": 1455,
              "pct_extracted": 0.7238565192636174
          }
        """

    def test_dvt_20250508(self):
        d = {
            "language": "en",
            "statuscode": 200,
            "parser": "foobar",
            "parser_version": "0.0.0",
            "generation_time": 127.91890096664429,
            "num_chars": 4003,
            "num_tokens": 1058,
            "jsonresume": {
                "basics": {
                    "name": "Ethan Carter",
                    "label": "Software Developer",
                    "email": "ethan.carter@fictionalmail.com",
                    "website": "",
                    "phone": "(555) 123-4567",
                    "url": "linkedin.com/in/ethan-carter",
                    "summary": "Highly skilled and detail-oriented software developer with expertise in multiple programming languages, databases, frameworks, and cloud technologies. Proven ability to design, develop, and deploy scalable applications and systems. Adept at collaborating with cross-functional teams to deliver innovative solutions.",
                    "location": {},
                    "profiles": [
                        {
                            "url": "",
                            "network": "Linkedin",
                            "username": ""
                        },
                        {
                            "url": "Node.js",
                            "network": "",
                            "username": ""
                        },
                        {
                            "url": "React.js",
                            "network": "",
                            "username": ""
                        }
                    ]
                },
                "work": [
                    {
                        "name": "Tech Innovators Inc.",
                        "position": "Software Developer",
                        "url": "",
                        "location": "San Francisco",
                        "startDate": "2021-06-15",
                        "endDate": "",
                        "summary": "",
                        "highlights": [
                            "Developed and maintained scalable web applications using React.js and Node.js, ensuring high performance and responsiveness.",
                            "Designed and implemented RESTful APIs to facilitate seamless communication between front-end and back-end systems.",
                            "Utilized AWS services (EC2, S3, RDS), Lambda to deploy and manage cloud-based applications, reducing infrastructure costs by 20%.",
                            "Collaborated with data scientists to build predictive models using Python and R, integrating them into production systems.",
                            "Optimized database queries and improved data retrieval times by 30% using SQL and MongoDB."
                        ]
                    },
                    {
                        "name": "CodeCraft Solutions",
                        "position": "Junior Developer",
                        "url": "",
                        "location": "Austin",
                        "startDate": "2019-01-15",
                        "endDate": "2021-05-15",
                        "summary": "",
                        "highlights": [
                            "Assisted in the development of enterprise-level applications using Java and SAP ABAP, ensuring compliance with client requirements.",
                            "Conducted unit testing using Junit4 and Maven, improving code quality and reducing bugs by 25%.",
                            "Worked with cross-functional teams to migrate legacy systems to SAP HANA Cloud, enhancing system performance and scalability.",
                            "Contributed to the development of data visualization tools using MATLAB and RStudio, enabling better decision-making for stakeholders."
                        ]
                    },
                    {
                        "name": "InnovateTech Labs",
                        "position": "Intern - Software Development",
                        "url": "",
                        "location": "Seattle",
                        "startDate": "2018-05-15",
                        "endDate": "2018-12-15",
                        "summary": "",
                        "highlights": [
                            "Supported senior developers in building and maintaining web applications using HTML, CSS, and JavaScript.",
                            "Gained hands-on experience with Git and GitHub for version control and collaborative development.",
                            "Assisted in the deployment of applications on AWS, gaining exposure to cloud infrastructure and services.",
                            "Participated in code reviews and debugging sessions, improving overall code quality and team efficiency."
                        ]
                    }
                ],
                "education": [
                    {
                        "institution": "University of California",
                        "url": "",
                        "area": "Computer Science",
                        "studyType": "Bachelor of Science",
                        "startDate": "",
                        "endDate": "2018-05-15",
                        "score": "",
                        "minors": [],
                        "courses": []
                    }
                ],
                "projects": [],
                "volunteer": [],
                "skills": [
                    {
                        "name": "Languages : Java",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "Python",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "R",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "HTML",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "CSS",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "JavaScript",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "C",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "C++",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "SAP ABAP",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "MATLAB",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "Databases : SQL",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "MySQL",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "Oracle DB",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "MongoDB",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "SAP HANA",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "React.js",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "Node.js",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "Maven",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "Junit4",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "Mongoose",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "REST API",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "Cloud Technologies : AWS (IAM",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "EC2",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "S3",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "EBS",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "RDS",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "DynamoDB VPC",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "Lambda)",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "SAP HANA Cloud Platforms : Git",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "GitHub",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "IntelliJ",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "Eclipse",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "Visual Studio",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "Jupyter Notebook",
                        "level": "",
                        "keywords": []
                    },
                    {
                        "name": "RStudio.",
                        "level": "",
                        "keywords": []
                    }
                ],
                "publications": [],
                "languages": [],
                "awards": [],
                "certificates": [],
                "references": [],
                "interests": []
            },
            "is_valid_json": True,
            "is_valid_jsonresume": True,
            "confidence": {
                "basics": {
                    "name": 0.0,
                    "email": 0.0,
                    "label": 0.0,
                    "phone": 0.0,
                    "location": {
                        "city": 0.0,
                        "region": 0.0,
                        "address": 0.0,
                        "postalCode": 0.0,
                        "countryCode": 0.0
                    }
                },
                "work": [
                    {
                        "name": 1.0,
                        "location": 1.0,
                        "position": 1.0
                    },
                    {
                        "name": 1.0,
                        "location": 1.0,
                        "position": 1.0
                    },
                    {
                        "name": 1.0,
                        "location": 1.0,
                        "position": 0.0
                    }
                ],
                "education": [
                    {
                        "institution": 1.0,
                        "studyType": 1.0,
                        "area": 1.0
                    }
                ]
            }
        }

        d["text"] = self.text
        metrics = main(d)
        assert metrics["pct_extracted"] > 0.73
        print("\n\n")
        print(json.dumps(metrics, indent=2))
        """
        {
          "aggregated_similarity": 0.8096,
          "aggregated_match": false,
          "input_text_len": 5269,
          "extracted_text_len": 3858,
          "remainder_text_len": 1411,
          "pct_extracted": 0.7322072499525527
        }
        """
