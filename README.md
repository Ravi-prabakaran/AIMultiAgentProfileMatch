# ProfileMatch - Multi-Agent Profile Matching System

A CrewAI-based multi-agent system that intelligently matches candidate profiles with job descriptions across multiple teams.

## 🎯 Features

- **Multi-Format Support**: Parse profiles from PDF, DOCX, and PPTX files using CrewAI's built-in tools
- **Intelligent Agents**: AI-powered agents that autonomously read and process documents
- **Comprehensive Extraction**: Extracts name, email, phone, LinkedIn, skills, and experience
- **Team Matching**: Matches candidates to best-fit teams from JD documents
- **Detailed Reports**: Generates comprehensive matching reports with scores and reasoning

## 🏗️ System Architecture

The system uses **four specialized CrewAI agents**, each equipped with document reading tools:

1. **Profile Parser Agent**: Uses FileReadTool, PDFSearchTool, and DOCXSearchTool to extract structured information from candidate profiles
2. **JD Parser Agent**: Uses the same tools to parse job descriptions and extract team requirements
3. **Profile Matcher Agent**: Analyzes and matches profiles to teams with scoring
4. **Report Generator Agent**: Creates comprehensive matching reports

### CrewAI Tools Used
- **DirectoryReadTool**: Lists files in directories
- **FileReadTool**: Reads general file content
- **PDFSearchTool**: Searches and extracts from PDF documents
- **DOCXSearchTool**: Searches and extracts from Word documents

### Why CrewAI Tools?
✅ **Autonomous agents** - Agents discover and read files themselves  
✅ **Less code** - No custom parsing logic needed  
✅ **Better integration** - Built for CrewAI's agent framework  
✅ **Smart context** - Optimized for LLM processing  
✅ **Fewer dependencies** - Reduced package requirements  

## 🤖 Supported LLM Providers

Choose your preferred AI provider:

| Provider | Models | API Key Source |
|----------|--------|----------------|
| **Anthropic Claude** | claude-3-5-sonnet, claude-3-opus, claude-3-sonnet | https://console.anthropic.com/ |
| **OpenAI** | gpt-4-turbo, gpt-4, gpt-3.5-turbo | https://platform.openai.com/api-keys |

**Recommended:** Claude 3.5 Sonnet for best performance on document analysis tasks.

## 📋 Prerequisites

- Python 3.8 or higher
- API key from OpenAI **OR** Anthropic (Claude)
- Windows/Linux/macOS

## 🚀 Installation

1. **Clone or navigate to the project directory**:
   ```powershell
   cd C:\Users\C152766\source\AI\ProfileMatch
   ```

2. **Create a virtual environment** (recommended):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   - Copy `.env.example` to `.env`
   - Choose your LLM provider and add the appropriate API key:
   
   **For Claude (Anthropic):**
   ```bash
   LLM_PROVIDER=claude
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   CLAUDE_MODEL=claude-3-5-sonnet-20241022
   ```
   
   **For OpenAI:**
   ```bash
   LLM_PROVIDER=openai
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4-turbo-preview
   ```

## 📁 Project Structure

```
ProfileMatch/
├── agents/                  # Agent definitions with CrewAI tools
│   ├── __init__.py
│   └── profile_agents.py   # Agents equipped with document reading tools
├── tasks/                   # Task definitions
│   ├── __init__.py
│   └── profile_tasks.py
├── profiles/                # Place candidate profiles here
│   ├── candidate1.pdf
│   ├── candidate2.docx
│   └── candidate3.pptx
├── job_descriptions/        # Place JD files here
│   └── team_jds.pdf
├── outputs/                 # Generated reports
├── main.py                  # Main application
├── config.py                # Configuration settings
├── example_usage.py         # Usage examples
├── requirements.txt         # Dependencies (simplified)
├── .env.example            # Environment template
└── README.md               # This file
```

**Note**: The system uses CrewAI's native tools (DirectoryReadTool, FileReadTool, PDFSearchTool, DOCXSearchTool) for document reading. No custom parsers needed!

## 💼 Usage

### Step 1: Prepare Your Documents

1. **Add Candidate Profiles** to the `profiles/` directory:
   - Supported formats: PDF, DOCX, PPTX
   - Each file should contain candidate information

2. **Add Job Descriptions** to the `job_descriptions/` directory:
   - Can have single or multiple team JDs in one file
   - Each team JD should include team name and requirements

### Step 2: Run the System

```powershell
python main.py
```

The system will:
1. Initialize agents with their document reading tools
2. Agents will automatically discover and read all profiles from the `profiles/` directory
3. Agents will automatically discover and read all JDs from the `job_descriptions/` directory
4. Use AI agents to analyze and match profiles with teams
5. Generate a comprehensive report in the `outputs/` directory

### Step 3: Review Results

Check the `outputs/` directory for the matching report:
- Report name format: `matching_report_YYYYMMDD_HHMMSS.txt`
- Contains detailed matches with scores and reasoning

## 🔧 Customization

### Switching LLM Providers

Simply edit your `.env` file:

**Use Claude:**
```bash
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=your_key_here
CLAUDE_MODEL=claude-3-5-sonnet-20241022  # or claude-3-opus-20240229
```

**Use OpenAI:**
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4-turbo-preview  # or gpt-4, gpt-3.5-turbo
```

### Using Different Directories

```python
from main import ProfileMatchSystem

system = ProfileMatchSystem(
    profiles_dir="path/to/profiles",
    jd_dir="path/to/jds",
    output_dir="path/to/outputs"
)

report_file = system.run()
```

## 📊 Match Scoring

The system uses a weighted scoring algorithm:
- **Technical Skills** (40%): Alignment with required technical skills
- **Experience Level** (30%): Years of experience match
- **Education** (15%): Educational qualifications
- **Overall Fit** (15%): General profile compatibility

Match scores range from 0-100, with:
- **80-100**: Excellent match (highly recommended)
- **60-79**: Good match (recommended)
- **40-59**: Moderate match (consider with caution)
- **0-39**: Poor match (not recommended)

## 🐛 Troubleshooting

### Common Issues

1. **"No module named 'crewai'"**
   - Run: `pip install -r requirements.txt --upgrade`

2. **"API key not found"**
   - Create `.env` file from `.env.example`
   - For Claude: Set `ANTHROPIC_API_KEY=your_key`
   - For OpenAI: Set `OPENAI_API_KEY=your_key`
   - Or set environment variable: `$env:ANTHROPIC_API_KEY="your_key"`

3. **"No profiles found"**
   - Ensure profiles are in the `profiles/` directory
   - Check file formats (PDF, DOCX, PPTX, TXT supported)

4. **Document parsing errors**
   - Ensure files are not corrupted
   - Check if files are password-protected (not supported)

5. **"Module 'langchain_anthropic' not found"**
   - Run: `pip install langchain-anthropic anthropic`

## 📝 Example JD Format

Your JD document can contain multiple teams:

```
Team: Engineering
Position: Senior Software Engineer
Required Skills: Python, JavaScript, React, Node.js, AWS
Experience: 5+ years
Education: Bachelor's in Computer Science or related field

Team: Data Science
Position: Data Scientist
Required Skills: Python, Machine Learning, SQL, TensorFlow, Statistics
Experience: 3+ years
Education: Master's in Data Science or related field
```

## 🔐 Security Notes

- Keep your `.env` file secure and never commit it to version control
- The `.env` file contains sensitive API keys
- Add `.env` to `.gitignore` if using Git

## 📄 License

This project is for internal use. Modify as needed for your organization.

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the CrewAI documentation: https://docs.crewai.com
3. Check OpenAI API status: https://status.openai.com

## 🎉 Getting Started Quickly

1. Add your OpenAI API key to `.env`
2. Place resumes in `profiles/` folder
3. Place JDs in `job_descriptions/` folder
4. Run `python main.py`
5. Check `outputs/` for results!
