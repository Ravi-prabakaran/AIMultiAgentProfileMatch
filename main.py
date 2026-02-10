"""
ProfileMatch - Multi-Agent System for Profile-JD Matching
Uses CrewAI to coordinate multiple agents for intelligent profile matching.
"""

import os
from pathlib import Path
from datetime import datetime

from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

from agents import ProfileMatchAgents
from tasks import ProfileMatchTasks


class ProfileMatchSystem:
    """Main system for coordinating the multi-agent profile matching process."""
    
    def __init__(
        self,
        profiles_dir: str = "profiles",
        jd_dir: str = "job_descriptions",
        output_dir: str = "outputs",
        api_key: str = None
    ):
        """
        Initialize the ProfileMatch system.
        
        Args:
            profiles_dir: Directory containing candidate profiles
            jd_dir: Directory containing job descriptions
            output_dir: Directory for output reports
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
            
            model = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
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
        self.output_dir = Path(output_dir)
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)
        
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
        print(f"  📁 Output directory: {self.output_dir}")
    
    def run_matching(self) -> str:
        """
        Execute the multi-agent matching process.
        
        Returns:
            The final matching report as a string
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
        
        return result
    
    def save_report(self, report: str) -> str:
        """
        Save the matching report to a file.
        
        Args:
            report: The report content to save
            
        Returns:
            Path to the saved report file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.output_dir / f"matching_report_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n💾 Report saved to: {report_file}")
        return str(report_file)
    
    def run(self) -> str:
        """
        Run the complete matching process and save the report.
        
        Returns:
            Path to the saved report file
        """
        try:
            report = self.run_matching()
            report_file = self.save_report(report)
            
            print("\n" + "="*70)
            print("🎉 ProfileMatch completed successfully!")
            print("="*70)
            
            return report_file
            
        except Exception as e:
            error_msg = f"Error during execution: {str(e)}"
            print(f"\n❌ {error_msg}")
            raise


def main():
    """Main entry point for the ProfileMatch system."""
    # You can customize these paths
    system = ProfileMatchSystem(
        profiles_dir="profiles",
        jd_dir="job_descriptions",
        output_dir="outputs"
    )
    
    # Run the matching process
    report_file = system.run()
    
    # Display the report location
    print(f"\n📄 View your matching report at: {report_file}")


if __name__ == "__main__":
    main()
