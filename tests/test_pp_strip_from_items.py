import json
import unittest

from nlptk import PostProcess


class TestPostProcessingListItems(unittest.TestCase):

    def test_highlights(self):
        pp = PostProcess()
        d = {
            "basics": {
                "name": "Maria Caracci",
                "label": "Founder, Mindset Coach, Menopause Advocate",
                "email": "mcaracci73@gmail.com",
                "website": "",
                "phone": "(516) 319-1321",
                "url": "http://www.linkedin.com/in/mariacaracci",
                "summary": "Director of Content Marketing and Corporate Communications Dynamic and award-winning marketing executive with a passion for ideas, strategy, and storytelling. Creative team leader who loves to push the boundaries of the consumer experience with deep insight into developing cross-channel content that connects with audiences, drives engagement, and exceeds expectations. Player-coach with 20+ years of experience who continuously raises the bar across teams, individuals, and produced work by instilling curiosity, cross-functional collaboration, and workflow nimbleness. Operations,Brand & Sales Marketing Leadership,Go to Market Strategy,Omni Channel Content Creation, Internal Communications,Business Development,Creative Ideation,Talent Development & Mentoring,Data Analytics & Trendspotting,Project Management",
                "location": {},
                "profiles": [
                    {
                        "url": "",
                        "network": "Linkedin",
                        "username": ""
                    }
                ]
            },
            "work": [
                {
                    "name": "WELLSPRING COACHING NY, tapyourwellspring.com",
                    "position": "Founder, Mindset Coach, Menopause Advocate",
                    "url": "",
                    "location": "Babylon",
                    "startDate": "2024-01-15",
                    "endDate": "",
                    "summary": "",
                    "highlights": [
                        "Run boutique coaching practice focused on performance-driven, midlife career women looking to reclaim their spark when suffering from workplace burnout and the menopause transition",
                        "- Used C and C languages",
                        "- Leveraged creative and content management systems (Adobe, Kit) and SEO analytics (Google) to cultivate customer pipeline and execute a comprehensive content strategy inclusive of social media, newsletter, email, and direct marketing",
                        "- Write, design, and edit bi-weekly digital newsletter, Menopaussible-an energy boost in an email-for high performance midlife women looking to reclaim their energy and control of their menopause experience, achieving 36% growth over the past through effective content planning and digital publishing strategies."
                    ]
                },
                {
                    "name": "DOTDASH MEREDITH, New York, NY Formerly Meredith Corporation",
                    "position": "Senior Vice President, Food Drink Revenue Marketing",
                    "url": "",
                    "location": "",
                    "startDate": "2022-02-15",
                    "endDate": "2023-09-15",
                    "summary": "",
                    "highlights": [
                        "Oversaw team of 19 to drive all revenue-producing efforts for Food Drink advertising vertical -$60MM revenue, as well as brand marketing and business development opportunities for 7 leading consumer Food Drink brands, inclusive of the #1 US food site, Allrecipes; EatingWell; Food & Wine; Liquor.com; Serious Eats; Simply Recipes; and Spruce Eats",
                        "- Transformed go to market story and suite of advertising opportunities to showcase the power and leadership of the newly combined Dotdash Meredith, ensuring a consistent, compelling narrative for DDM's portfolio of sites that resonated with DDM's target audience, and securing a new strategic partnership with leading Food CPG advertiser $4.5MM in revenue, a 250% YOY increase",
                        "- Identified distinct white space opportunity to drive business growth among pharmaceutical and healthcare brands looking to reach new audiences by creating condition-based eating content, capturing $1MM in revenue from leading pharma brand and $250K in single-month sponsorship dollars with new digital issue format."
                    ]
                },
                {
                    "name": "MEREDITH CORPORATION",
                    "position": "Vice President, Sales Marketing",
                    "url": "",
                    "location": "New York",
                    "startDate": "2018-08-15",
                    "endDate": "2022-01-15",
                    "summary": "",
                    "highlights": [
                        "Hired, cultivated, and mobilized 40-person team to develop integrated marketing programs across 9 advertising verticals $200MM revenue, including pharmaceutical/health, food and beverage, fashion and retail, finance, auto, tech, travel, beauty and home, which connected brands with 90% of US women",
                        "- Created and instituted organization-wide best practices for ideation, content creation, and visual storytelling, rooted in human insights, driving purpose, and highlighting value in asset offerings to achieve 15% RFP pipeline growth over and 11% growth in RFPs representing $1MM deal size",
                        "- Advanced internal communications and improved speed to market through creation of news-style meeting programming that fostered connective team culture across various business divisions, while serving to educate and arm 300 participants on marketplace efforts",
                        "Maria Caracci Ciccolella mcaracci73 @ gmail.com Page Two",
                        "- Architected vertical expertise strategy by elevating role of sales marketing teams to company-wide industry experts and driving focus on consultative"
                    ]
                }
            ],
            "education": [],
            "projects": [],
            "volunteer": [],
            "skills": [
                {
                    "name": "- AI-Driven Process Optimization",
                    "level": "",
                    "keywords": []
                },
                {
                    "name": "- IoT & Blockchain Integration",
                    "level": "",
                    "keywords": []
                },
                {
                    "name": "\\ SAP S/4HANA & Kinaxis RapidResponse",
                    "level": "",
                    "keywords": []
                },
                {
                    "name": "\\ \\ tESG Compliance",
                    "level": "",
                    "keywords": []
                },
                {
                    "name": "P&L Accountability $15M+ Budgets)",
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
        }
        d2, is_valid_json, is_valid_jsonresume = pp.postprocess(d)
        assert is_valid_json == True
        assert is_valid_jsonresume == True
        print(json.dumps(d2, indent=2))

        # Confirm leading hyphen has been stripped from work experiences
        work = d2["work"]
        for w in work:
            for h in w["highlights"]:
                assert h.startswith("-") != True
        # Confirm leading hyphen and \\ has been stripped from skills
        skills = d2["skills"]
        for s in skills:
            assert s["name"].startswith("-") != True
            assert s["name"].startswith("\\") != True

if __name__ == '__main__':
    unittest.main()
