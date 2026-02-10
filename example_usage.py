"""
Example usage script for ProfileMatch system.
Demonstrates different ways to use the system.
"""

from main import ProfileMatchSystem
import os


def example_basic_usage():
    """Basic usage with default settings."""
    print("="*70)
    print("Example 1: Basic Usage")
    print("="*70)
    
    # Create system with default directories
    system = ProfileMatchSystem()
    
    # Run matching
    report_file = system.run()
    
    print(f"\nReport saved to: {report_file}")


def example_custom_directories():
    """Usage with custom directory paths."""
    print("\n" + "="*70)
    print("Example 2: Custom Directories")
    print("="*70)
    
    system = ProfileMatchSystem(
        profiles_dir="my_profiles",
        jd_dir="my_jds",
        output_dir="my_outputs"
    )
    
    report_file = system.run()
    print(f"\nReport saved to: {report_file}")


def example_with_api_key():
    """Usage with API key passed directly."""
    print("\n" + "="*70)
    print("Example 3: With API Key Parameter")
    print("="*70)
    
    api_key = os.getenv("OPENAI_API_KEY", "your_key_here")
    
    system = ProfileMatchSystem(api_key=api_key)
    report_file = system.run()
    
    print(f"\nReport saved to: {report_file}")


def example_step_by_step():
    """Step-by-step execution with intermediate access."""
    print("\n" + "="*70)
    print("Example 4: Step-by-Step Execution")
    print("="*70)
    
    # Initialize system
    system = ProfileMatchSystem()
    
    # Run matching (agents will read documents using their tools)
    print("Agents will automatically read files from directories using CrewAI tools...")
    report = system.run_matching()
    
    # Save report
    report_file = system.save_report(report)
    
    print(f"\nReport saved to: {report_file}")
    
    # You can also access the report content
    print(f"\nReport preview (first 500 chars):")
    print("-"*70)
    print(report[:500])
    print("...")


if __name__ == "__main__":
    # Uncomment the example you want to run
    
    # Example 1: Basic usage
    example_basic_usage()
    
    # Example 2: Custom directories
    # example_custom_directories()
    
    # Example 3: With API key
    # example_with_api_key()
    
    # Example 4: Step by step
    # example_step_by_step()
