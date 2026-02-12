"""
Agent definitions for the ProfileMatch multi-agent system.
"""

from crewai import Agent
from crewai_tools import DirectoryReadTool
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from typing import Optional, Union

from tools import PDFReaderTool, DOCXReaderTool, PPTXReaderTool


class ProfileMatchAgents:
    """Agents class for creating specialized agents."""
    
    def __init__(
        self, 
        llm: Optional[Union[ChatOpenAI, ChatAnthropic]] = None, 
        profiles_dir: str = "profiles", 
        jd_dir: str = "job_descriptions"
    ):
        """Initialize the agents with optional LLM configuration."""
        self.llm = llm or ChatOpenAI(model="gpt-4-turbo-preview", temperature=0.7)
        
        # Initialize CrewAI tools for different file types
        self.profile_directory_tool = DirectoryReadTool(directory=profiles_dir)
        self.jd_directory_tool = DirectoryReadTool(directory=jd_dir)
        
        # Custom document reading tools
        self.pdf_reader = PDFReaderTool()
        self.docx_reader = DOCXReaderTool()
        self.pptx_reader = PPTXReaderTool()
    
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
                     "text. You understand various resume formats and can adapt to different styles. "
                     "You use the Read PDF Document tool for PDFs, Read Word Document tool for DOCX files, "
                     "and Read PowerPoint Presentation tool for PPTX files.",
            verbose=True,
            allow_delegation=False,
            tools=[self.profile_directory_tool, self.pdf_reader, self.docx_reader, self.pptx_reader],
            llm=self.llm
        )
    
    def jd_parser_agent(self) -> Agent:
        """
        Agent responsible for parsing job descriptions.
        Extracts team names, required skills, experience requirements, and job details.
        """
        return Agent(
            role="Job Description Analyst",
            goal="Parse and understand job descriptions for different teams. "
                 "CRITICAL RULE: You MUST extract the team name from the JOB DESCRIPTION FILENAME (in the job_descriptions directory). "
                 "DO NOT use candidate filenames. DO NOT use example names. DO NOT invent team names. "
                 "Process: (1) List files in job_descriptions directory, (2) For EACH JD file, take its filename, "
                 "(3) Remove the extension (.pdf, .docx, .pptx), (4) That is the team name. "
                 "Then extract job requirements from that JD document's content.",
            backstory="You are a seasoned HR analyst and recruiter with deep expertise in understanding "
                     "job requirements. You excel at identifying the key skills and qualifications needed "
                     "for different roles. CRITICAL: You work specifically with JOB DESCRIPTION files in the "
                     "'job_descriptions' directory. You ALWAYS determine each team name from the JD filename itself - "
                     "simply remove the file extension. Examples: "
                     "If you read 'job_descriptions/DataScience.pdf' → team is 'DataScience'. "
                     "If you read 'job_descriptions/Backend_Engineering.docx' → team is 'Backend_Engineering'. "
                     "If you read 'job_descriptions/DevOps.pptx' → team is 'DevOps'. "
                     "You NEVER use candidate profile filenames for team names. You NEVER use placeholder names. "
                     "You use Read PDF Document for PDFs, Read Word Document for DOCX, Read PowerPoint Presentation for PPTX.",
            verbose=True,
            allow_delegation=False,
            tools=[self.jd_directory_tool, self.pdf_reader, self.docx_reader, self.pptx_reader],
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
