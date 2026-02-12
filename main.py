"""
ProfileMatch - Multi-Agent System for Profile-JD Matching
Uses CrewAI to coordinate multiple agents for intelligent profile matching.
"""

import os
import json
import re
from pathlib import Path

from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
from tabulate import tabulate

from agents import ProfileMatchAgents
from tasks import ProfileMatchTasks


class ProfileMatchSystem:
    """Main system for coordinating the multi-agent profile matching process."""
    
    def __init__(
        self,
        profiles_dir: str = "profiles",
        jd_dir: str = "job_descriptions",
        api_key: str = None
    ):
        """
        Initialize the ProfileMatch system.
        
        Args:
            profiles_dir: Directory containing candidate profiles
            jd_dir: Directory containing job descriptions
            api_key: API key for LLM provider (optional if set in environment)
        """
        # Load environment variables
        load_dotenv()
        
        # Determine LLM provider
        llm_provider = os.getenv("LLM_PROVIDER", "openai").lower()
        
        # Initialize LLM based on provider
        if llm_provider == "claude":
            # Configure Claude/Anthropic
            if api_key:
                os.environ["ANTHROPIC_API_KEY"] = api_key
            elif not os.getenv("ANTHROPIC_API_KEY"):
                raise ValueError("Anthropic API key not found. Set ANTHROPIC_API_KEY in .env or pass api_key parameter.")
            
            model = os.getenv("CLAUDE_MODEL", "claude-3-haiku-20240307")
            temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
            
            self.llm = ChatAnthropic(
                model=model,
                temperature=temperature,
                anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
            )
            print(f"🤖 Using Claude: {model}")
            
        else:  # Default to OpenAI
            # Configure OpenAI
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
            elif not os.getenv("OPENAI_API_KEY"):
                raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY in .env or pass api_key parameter.")
            
            model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
            temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
            
            self.llm = ChatOpenAI(
                model=model,
                temperature=temperature
            )
            print(f"🤖 Using OpenAI: {model}")
        
        self.profiles_dir = profiles_dir
        self.jd_dir = jd_dir
        
        # Ensure input directories exist
        Path(self.profiles_dir).mkdir(exist_ok=True)
        Path(self.jd_dir).mkdir(exist_ok=True)
        
        # Initialize agents with tools
        agent_factory = ProfileMatchAgents(
            llm=self.llm,
            profiles_dir=self.profiles_dir,
            jd_dir=self.jd_dir
        )
        self.profile_parser_agent = agent_factory.profile_parser_agent()
        self.jd_parser_agent = agent_factory.jd_parser_agent()
        self.matcher_agent = agent_factory.profile_matcher_agent()
        self.report_agent = agent_factory.report_generator_agent()
        
        print("✓ ProfileMatch system initialized")
        print(f"  📁 Profiles directory: {self.profiles_dir}")
        print(f"  📁 JD directory: {self.jd_dir}")
    
    def display_matching_report(self, report_data: dict):
        """
        Display the matching report in a formatted table.
        
        Args:
            report_data: Dictionary containing the matching report data
        """
        print("\n" + "="*80)
        print("📊 PROFILE MATCHING REPORT")
        print("="*80)
        
        # Display summary
        summary = report_data.get("summary", {})
        print(f"\n📅 Report Date: {summary.get('report_date', 'N/A')}")
        print(f"\n📈 Summary:")
        print(f"   • Total Candidates: {summary.get('total_candidates', 0)}")
        print(f"   • Total Teams: {summary.get('total_teams', 0)}")
        print(f"   • Candidates with Matches: {summary.get('candidates_with_matches', 0)}")
        print(f"   • Candidates without Matches: {summary.get('candidates_without_matches', 0)}")
        
        # Prepare table data
        matches = report_data.get("matches", [])
        table_data = []
        
        for match in matches:
            # Format matching teams
            teams = match.get("matching_teams", [])
            if teams:
                teams_str = ", ".join([f"{t['team_name']} ({t['score']})" for t in teams])
            else:
                teams_str = "No suitable match found"
            
            # Get highest score
            score = match.get("highest_score")
            score_str = str(score) if score is not None else "N/A"
            
            table_data.append([
                teams_str,
                score_str,
                match.get("candidate_name", "Unknown"),
                match.get("phone", "Not Available"),
                match.get("email", "Not Available"),
                match.get("linkedin", "Not Available")
            ])
        
        # Display table
        headers = ["Matching Team(s)", "Score", "Candidate Name", "Phone Number", "Email", "LinkedIn Profile"]
        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
        print("\n" + "="*80)
    
    def run_matching(self) -> dict:
        """
        Execute the multi-agent matching process.
        
        Returns:
            The final matching report as a dictionary
        """
        print("\n" + "="*70)
        print("🚀 Starting ProfileMatch Multi-Agent System")
        print("="*70)
        
        # Create tasks - agents will use their tools to read documents
        print("\n📋 Creating tasks for agents...")
        task_factory = ProfileMatchTasks()
        
        profile_parse_task = task_factory.parse_profiles_task(
            self.profile_parser_agent,
            profiles_dir=self.profiles_dir
        )
        
        jd_parse_task = task_factory.parse_jd_task(
            self.jd_parser_agent,
            jd_dir=self.jd_dir
        )
        
        matching_task = task_factory.match_profiles_task(
            self.matcher_agent,
            context=[profile_parse_task, jd_parse_task]
        )
        
        report_task = task_factory.generate_report_task(
            self.report_agent,
            context=[profile_parse_task, jd_parse_task, matching_task]
        )
        
        # Create crew
        print("👥 Assembling crew...")
        crew = Crew(
            agents=[
                self.profile_parser_agent,
                self.jd_parser_agent,
                self.matcher_agent,
                self.report_agent
            ],
            tasks=[
                profile_parse_task,
                jd_parse_task,
                matching_task,
                report_task
            ],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute
        print("\n🤖 Starting crew execution...")
        print("   Agents will read documents using their tools...")
        print("-"*70)
        result = crew.kickoff()
        
        print("\n" + "="*70)
        print("✅ Matching Complete!")
        print("="*70)
        
        # Parse JSON from result
        try:
            # Try to extract JSON from the result
            result_str = str(result)
            
            # Try to find JSON in the result (handle markdown code blocks)
            json_match = re.search(r'```(?:json)?\s*({.*?})\s*```', result_str, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Try to find raw JSON
                json_match = re.search(r'({\s*"summary".*})', result_str, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                else:
                    json_str = result_str
            
            report_data = json.loads(json_str)
            return report_data
            
        except json.JSONDecodeError as e:
            print(f"\n⚠️  Warning: Could not parse JSON from result. Error: {e}")
            print("\nRaw result:")
            print(result)
            return {"summary": {}, "matches": [], "raw_result": str(result)}
    
    def run(self) -> dict:
        """
        Run the complete matching process and display the report.
        
        Returns:
            Dictionary containing the matching report data
        """
        try:
            report_data = self.run_matching()
            
            # Display the report as a table
            self.display_matching_report(report_data)
            
            print("\n" + "="*70)
            print("🎉 ProfileMatch completed successfully!")
            print("="*70)
            
            return report_data
            
        except Exception as e:
            error_msg = f"Error during execution: {str(e)}"
            print(f"\n❌ {error_msg}")
            raise


def main():
    """Main entry point for the ProfileMatch system."""
    # You can customize these paths
    system = ProfileMatchSystem(
        profiles_dir="profiles",
        jd_dir="job_descriptions"
    )
    
    # Run the matching process and display table in console
    report_data = system.run()


if __name__ == "__main__":
    main()
