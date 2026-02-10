"""
Agent definitions for the ProfileMatch multi-agent system.
"""

from crewai import Agent
from crewai_tools import DirectoryReadTool, FileReadTool, PDFSearchTool, DOCXSearchTool
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from typing import Optional, Union


class ProfileMatchAgents:
    """Factory class for creating specialized agents."""
    
    def __init__(
        self, 
        llm: Optional[Union[ChatOpenAI, ChatAnthropic]] = None, 
        profiles_dir: str = "profiles", 
        jd_dir: str = "job_descriptions"
    ):
        """Initialize the agents with optional LLM configuration."""
        self.llm = llm or ChatOpenAI(model="gpt-4-turbo-preview", temperature=0.7)
        
        # Initialize CrewAI tools
        self.profile_directory_tool = DirectoryReadTool(directory=profiles_dir)
        self.jd_directory_tool = DirectoryReadTool(directory=jd_dir)
        self.file_read_tool = FileReadTool()
        self.pdf_tool = PDFSearchTool()
        self.docx_tool = DOCXSearchTool()
    
    def profile_parser_agent(self) -> Agent:
        """
        Agent responsible for parsing profiles from various document formats.
        Extracts skills, experience, contact information, and other relevant details.
        """
        return Agent(
            role="Profile Parser Specialist",
            goal="Extract and structure all relevant information from candidate profiles including "
                 "name, contact details (email, phone, LinkedIn), skills, experience, education, "
                 "and qualifications from documents in various formats (PDF, DOCX, PPTX)",
            backstory="You are an expert in document analysis and information extraction with years "
                     "of experience in parsing resumes and profiles. You have a keen eye for detail "
                     "and can accurately identify and extract relevant information from unstructured "
                     "text. You understand various resume formats and can adapt to different styles.",
            verbose=True,
            allow_delegation=False,
            tools=[self.profile_directory_tool, self.file_read_tool, self.pdf_tool, self.docx_tool],
            llm=self.llm
        )
    
    def jd_parser_agent(self) -> Agent:
        """
        Agent responsible for parsing job descriptions.
        Extracts team names, required skills, experience requirements, and job details.
        """
        return Agent(
            role="Job Description Analyst",
            goal="Parse and understand job descriptions for different teams, extracting team names, "
                 "required skills, experience levels, qualifications, and key responsibilities. "
                 "Organize multiple JDs when they are in a single document.",
            backstory="You are a seasoned HR analyst and recruiter with deep expertise in understanding "
                     "job requirements. You excel at identifying the key skills and qualifications needed "
                     "for different roles. You can parse complex JD documents that contain multiple team "
                     "requirements and structure them clearly.",
            verbose=True,
            allow_delegation=False,
            tools=[self.jd_directory_tool, self.file_read_tool, self.pdf_tool, self.docx_tool],
            llm=self.llm
        )
    
    def profile_matcher_agent(self) -> Agent:
        """
        Agent responsible for matching profiles to job descriptions.
        Analyzes compatibility and provides match scores with reasoning.
        """
        return Agent(
            role="Profile Matching Expert",
            goal="Analyze candidate profiles against job descriptions and identify the best team matches "
                 "based on skills alignment, experience level, qualifications, and overall fit. "
                 "Provide detailed reasoning for each match with a compatibility score.",
            backstory="You are a senior talent acquisition specialist with exceptional analytical skills. "
                     "You have successfully matched thousands of candidates to positions by understanding "
                     "both technical requirements and cultural fit. You consider multiple dimensions including "
                     "skill match, experience relevance, career progression, and growth potential. "
                     "You provide clear, data-driven insights with your recommendations.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def report_generator_agent(self) -> Agent:
        """
        Agent responsible for generating final structured reports.
        Creates comprehensive matching reports with all relevant details.
        """
        return Agent(
            role="Reporting Specialist",
            goal="Generate comprehensive, well-structured reports that include candidate information "
                 "(name, email, phone, LinkedIn profile), matched team details, match scores, "
                 "and clear reasoning. Present information in an easy-to-read format.",
            backstory="You are a professional report writer with expertise in presenting complex "
                     "analytical results in clear, actionable formats. You ensure all critical "
                     "information is included and properly structured for decision-makers.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
