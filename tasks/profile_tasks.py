"""
Task definitions for the ProfileMatch multi-agent system.
"""

from crewai import Task
from typing import List


class ProfileMatchTasks:
    """Tasks class for creating specialized tasks."""
    
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
            
            IMPORTANT - Use the correct tool for each file type:
            - For PDF files (.pdf): Use "Read PDF Document" tool with the full file path
            - For Word documents (.docx): Use "Read Word Document" tool with the full file path
            - For PowerPoint files (.pptx): Use "Read PowerPoint Presentation" tool with the full file path
            
            Steps:
            1. First, list all files in the directory
            2. For each file, identify its extension
            3. Use the appropriate reader tool with the full file path
            4. Extract all relevant information from the content
            
            For each profile document, extract:
            1. Candidate Name
            2. Email Address
            3. Phone Number
            4. LinkedIn Profile URL
            5. Key Skills (technical and soft skills)
            6. Years of Experience
            7. Education and Certifications
            8. Current/Previous Role and Company
            9. Notable Achievements
            
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
            
            CRITICAL INSTRUCTION - TEAM NAME EXTRACTION:
            The TEAM NAME comes from the JOB DESCRIPTION FILENAME (NOT from candidate profile filenames).
            You are working with files in the '{jd_dir}' directory ONLY for team name extraction.
            
            YOU MUST extract the team name from the ACTUAL JD FILENAME you are processing.
            DO NOT use candidate profile filenames for team names.
            DO NOT use example names like "Engineering_Team" or "Data_Science".
            
            Process for EACH job description file:
            1. Look at the actual filename of the JD document in '{jd_dir}' directory
            2. Remove the extension (.pdf, .docx, or .pptx)  
            3. The remaining text IS the team name
            4. Then read the document content to extract job requirements
            
            Examples (for illustration - use YOUR actual JD filenames from '{jd_dir}'):
            - JD file: '{jd_dir}/CloudOps.pdf' → Team Name: "CloudOps"
            - JD file: '{jd_dir}/Mobile_Development.docx' → Team Name: "Mobile_Development"
            - JD file: '{jd_dir}/QA_Testing.pptx' → Team Name: "QA_Testing"
            
            Remember: Team names come from JOB DESCRIPTION filenames, NOT candidate filenames.
            
            IMPORTANT - Use the correct tool for each file type:
            - For PDF files (.pdf): Use "Read PDF Document" tool with the full file path
            - For Word documents (.docx): Use "Read Word Document" tool with the full file path
            - For PowerPoint files (.pptx): Use "Read PowerPoint Presentation" tool with the full file path
            
            Steps:
            1. First, list all files in the directory
            2. For each file, extract the team name from the filename (remove extension)
            3. Use the appropriate reader tool with the full file path to read the document content
            4. Extract job requirements from the content
            
            For each file/team, extract:
            1. Team Name (from filename - DO NOT look for this in document content)
            2. Job Title/Position (from document content)
            3. Required Skills (from document content - technical and soft skills)
            4. Minimum Years of Experience (from document content)
            5. Educational Requirements (from document content)
            6. Key Responsibilities (from document content)
            7. Preferred Qualifications (from document content)
            8. Team/Role Description (from document content)
            
            Organize each team's requirements clearly and completely.
            """,
            agent=agent,
            expected_output="A structured list of all teams with their complete job requirements. "
                          "Each entry must include the team name (extracted from filename), required skills, "
                          "experience levels, and qualifications (extracted from document content)."
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
            2. Compare them against EVERY team's requirements
            3. Calculate a match score (0-100) for each candidate-team pairing
            4. A candidate can match with MULTIPLE teams - identify ALL teams where match score >= 60
            5. For each candidate-team match, provide:
               - Match score
               - Key matching skills
               - Experience alignment
               - Areas of strong fit
            
            IMPORTANT: 
            - Candidates can match with multiple teams simultaneously
            - Include ALL teams with match score >= 60 (good match threshold)
            - If no team scores >= 60, mark candidate as "No Match"
            - Rank teams by match score for each candidate
            
            Scoring criteria:
            - Technical skill alignment (40% weight)
            - Experience level match (30% weight)
            - Educational qualifications (15% weight)
            - Overall profile fit (15% weight)
            """,
            agent=agent,
            context=context,
            expected_output="A comprehensive matching analysis showing each candidate with ALL their matching "
                          "teams (score >= 60), including match scores and reasoning. Candidates may have multiple "
                          "team matches or no matches."
        )
    
    @staticmethod
    def generate_report_task(agent, context: List[Task]) -> Task:
        """
        Task for generating the final matching report in JSON format.
        
        Args:
            agent: The report generator agent
            context: List of all previous tasks
        """
        return Task(
            description="""
            Generate a matching report in VALID JSON FORMAT with the following structure:
            
            {
              "summary": {
                "total_candidates": <number>,
                "total_teams": <number>,
                "candidates_with_matches": <number>,
                "candidates_without_matches": <number>,
                "report_date": "<date string>"
              },
              "matches": [
                {
                  "candidate_name": "<name>",
                  "phone": "<phone or 'Not Available'>",
                  "email": "<email or 'Not Available'>",
                  "linkedin": "<linkedin URL or 'Not Available'>",
                  "matching_teams": [
                    {"team_name": "<team>", "score": <number>},
                    {"team_name": "<team>", "score": <number>}
                  ],
                  "highest_score": <number or null>
                }
              ]
            }
            
            Requirements:
            - Output ONLY valid JSON, no markdown formatting or extra text
            - For matching_teams array:
              * Include ALL teams with score >= 60
              * Sort by score (descending)
              * If no matches, use empty array []
            - highest_score: The maximum score, or null if no matches
            - Sort matches array:
              1. Candidates with matches first (by highest_score descending)
              2. Candidates without matches at the end
            - Use "Not Available" for missing contact information
            - Ensure all JSON is properly formatted and parseable
            """,
            agent=agent,
            context=context,
            expected_output="A valid JSON object containing summary statistics and an array of candidate matches "
                          "with their contact information and matching teams. Must be parseable JSON without any "
                          "markdown formatting or additional text."
        )
