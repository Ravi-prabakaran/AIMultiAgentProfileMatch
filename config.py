"""
Configuration settings for ProfileMatch system.
"""

# LLM Configuration
LLM_CONFIG = {
    "model": "gpt-4-turbo-preview",  # Options: gpt-4, gpt-4-turbo-preview, gpt-3.5-turbo
    "temperature": 0.7,  # 0.0 = deterministic, 1.0 = creative
}

# Directory Configuration
DIRECTORIES = {
    "profiles": "profiles",
    "job_descriptions": "job_descriptions",
    "outputs": "outputs",
}

# Supported File Formats
SUPPORTED_FORMATS = ['.pdf', '.docx', '.doc', '.pptx', '.ppt']

# Matching Weights (should sum to 100)
MATCHING_WEIGHTS = {
    "technical_skills": 40,
    "experience": 30,
    "education": 15,
    "overall_fit": 15,
}

# Match Score Thresholds
MATCH_THRESHOLDS = {
    "excellent": 80,  # 80-100: Excellent match
    "good": 60,       # 60-79: Good match
    "moderate": 40,   # 40-59: Moderate match
    # 0-39: Poor match
}

# Agent Configuration
AGENT_CONFIG = {
    "verbose": True,
    "allow_delegation": False,
}

# Crew Configuration
CREW_CONFIG = {
    "verbose": True,
}

# Report Configuration
REPORT_CONFIG = {
    "include_summary": True,
    "include_contact_info": True,
    "include_alternative_matches": True,
    "top_matches_per_candidate": 3,
}
