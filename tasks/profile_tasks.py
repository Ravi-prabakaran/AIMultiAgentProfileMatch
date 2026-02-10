"""
Task definitions for the ProfileMatch multi-agent system.
"""

from crewai import Task
from typing import List


class ProfileMatchTasks:
    """Factory class for creating specialized tasks."""
    
    @staticmethod
    def parse_profiles_task(agent, profiles_dir: str = "profiles") -> Task:
        """
        Task for parsing candidate profiles and extracting structured information.
        
        Args:
            agent: The profile parser agent
            profiles_dir: Directory containing profile documents
        """
        return Task(
            description=f"""
            Read all candidate profile documents from the '{profiles_dir}' directory and extract structured information.
            
            For each profile document you find, extract:
            1. Candidate Name
            2. Email Address
            3. Phone Number
            4. LinkedIn Profile URL
            5. Key Skills (technical and soft skills)
            6. Years of Experience
            7. Education and Certifications
            8. Current/Previous Role and Company
            9. Notable Achievements
            
            Use your tools to:
            - List all files in the profiles directory
            - Read each document (PDF, DOCX, PPTX)
            - Extract the information systematically
            
            Organize the information in a clear, structured format for each candidate.
            If any information is not available, mark it as "Not Found".
            """,
            agent=agent,
            expected_output="A structured list of all candidates with their complete profile information "
                          "including contact details, skills, experience, and qualifications."
        )
    
    @staticmethod
    def parse_jd_task(agent, jd_dir: str = "job_descriptions") -> Task:
        """
        Task for parsing job descriptions and extracting team requirements.
        
        Args:
            agent: The JD parser agent
            jd_dir: Directory containing job description documents
        """
        return Task(
            description=f"""
            Read all job description documents from the '{jd_dir}' directory.
            These documents may contain multiple team JDs in a single file.
            
            Use your tools to:
            - List all files in the job descriptions directory
            - Read each document carefully
            - Identify all teams/positions mentioned
            
            For each team/position, extract:
            1. Team Name
            2. Job Title/Position
            3. Required Skills (technical and soft skills)
            4. Minimum Years of Experience
            5. Educational Requirements
            6. Key Responsibilities
            7. Preferred Qualifications
            8. Team Description
            
            Organize each team's requirements clearly and completely.
            """,
            agent=agent,
            expected_output="A structured list of all teams with their complete job requirements, "
                          "including team names, required skills, experience levels, and qualifications."
        )
    
    @staticmethod
    def match_profiles_task(agent, context: List[Task]) -> Task:
        """
        Task for matching candidates to teams based on their profiles and JD requirements.
        
        Args:
            agent: The profile matcher agent
            context: List of previous tasks (profile parsing and JD parsing)
        """
        return Task(
            description="""
            Based on the parsed candidate profiles and job descriptions:
            
            1. Analyze each candidate's skills, experience, and qualifications
            2. Compare them against each team's requirements
            3. Calculate a match score (0-100) for each candidate-team pairing
            4. Identify the best matching team for each candidate
            5. Provide detailed reasoning for each match including:
               - Matching skills
               - Experience alignment
               - Areas of strong fit
               - Potential gaps or concerns
            
            Consider:
            - Technical skill alignment (40% weight)
            - Experience level match (30% weight)
            - Educational qualifications (15% weight)
            - Overall profile fit (15% weight)
            
            Rank matches by score and provide top 3 team matches per candidate if applicable.
            """,
            agent=agent,
            context=context,
            expected_output="A comprehensive matching analysis with each candidate matched to their best-fit "
                          "team(s), including match scores, detailed reasoning, and ranked alternatives."
        )
    
    @staticmethod
    def generate_report_task(agent, context: List[Task]) -> Task:
        """
        Task for generating the final matching report.
        
        Args:
            agent: The report generator agent
            context: List of all previous tasks
        """
        return Task(
            description="""
            Generate a comprehensive matching report with the following structure:
            
            For each candidate:
            - Candidate Name
            - Email Address
            - Phone Number
            - LinkedIn Profile Link
            - Best Matched Team Name
            - Match Score (0-100)
            - Key Matching Skills
            - Match Reasoning (2-3 sentences)
            - Alternative Team Matches (if any, with scores)
            
            Format the report clearly with sections for each candidate.
            Include a summary at the top with:
            - Total candidates processed
            - Total teams available
            - Average match score
            - Number of high-confidence matches (score >= 80)
            
            Ensure all contact information is accurate and properly formatted.
            """,
            agent=agent,
            context=context,
            expected_output="A complete, well-formatted matching report with all candidate details, "
                          "contact information, matched teams, scores, and detailed reasoning for each match. "
                          "This should be ready to present to stakeholders."
        )
