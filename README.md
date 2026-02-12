# ProfileMatch - Multi-Agent Profile Matching System

A CrewAI-based multi-agent system that intelligently matches candidate profiles with job descriptions across multiple teams.

## 🎯 Features

- **Multi-Format Support**: Parse profiles and JDs from PDF, DOCX, and PPTX files
- **Custom Document Readers**: Lightweight, reliable tools for reading documents without vector database dependencies
- **Intelligent Agents**: Four specialized AI agents working together autonomously
- **Comprehensive Extraction**: Extracts name, email, phone, LinkedIn, skills, and experience
- **Multi-Team Matching**: Candidates can match with **multiple teams** simultaneously (score-based threshold)
- **Table Display**: Results displayed in a clean, formatted table in the console
- **Flexible LLM Support**: Works with OpenAI or Anthropic Claude

## 🏗️ System Architecture

The system uses **four specialized CrewAI agents**:

1. **Profile Parser Agent**: Extracts structured information from candidate profiles (PDF/DOCX/PPTX)
   - Tools: DirectoryReadTool, PDFReaderTool, DOCXReaderTool, PPTXReaderTool
   
2. **JD Parser Agent**: Parses job descriptions and extracts requirements
   - **Team name = JD filename** (without extension)
   - Tools: DirectoryReadTool, PDFReaderTool, DOCXReaderTool, PPTXReaderTool
   
3. **Profile Matcher Agent**: Matches candidates to ALL qualifying teams
   - Scores each candidate against every team
   - Includes all teams with score ≥ 60
   
4. **Report Generator Agent**: Creates JSON report displayed as formatted table
   - Columns: Matching Team(s) | Score | Candidate Name | Phone | Email | LinkedIn

### Custom Document Reading Tools

- **PDFReaderTool**: Extracts text from PDF files using PyPDF2
- **DOCXReaderTool**: Reads Word documents using python-docx
- **PPTXReaderTool**: Extracts text from PowerPoint presentations using python-pptx

**Why custom tools?**
✅ No vector database setup required  
✅ Lightweight and fast  
✅ Direct file reading without external services  
✅ Reliable text extraction  
✅ Simple error handling  

## 🤖 Supported LLM Providers

| Provider | Models | API Key Source |
|----------|--------|----------------|
| **Anthropic Claude** | claude-3-haiku-20240307 (verified), claude-3-sonnet, claude-3-opus | https://console.anthropic.com/ |
| **OpenAI** | gpt-4-turbo-preview, gpt-4, gpt-3.5-turbo | https://platform.openai.com/api-keys |

**Recommended:** Claude 3 Haiku (`claude-3-haiku-20240307`) - Fast, cost-effective, and verified working.

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
   - Add your API key and configure settings:
   
   **For Claude (Anthropic) - Recommended:**
   ```bash
   LLM_PROVIDER=claude
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   CLAUDE_MODEL=claude-3-haiku-20240307
   OTEL_SDK_DISABLED=true  # Disable telemetry to avoid connection errors
   ```
   
   **For OpenAI:**
   ```bash
   LLM_PROVIDER=openai
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4-turbo-preview
   OTEL_SDK_DISABLED=true  # Disable telemetry to avoid connection errors
   ```

## 📁 Project Structure

```
ProfileMatch/
├── agents/                  # Agent definitions
│   ├── __init__.py
│   └── profile_agents.py   # Four specialized agents
├── tasks/                   # Task definitions
│   ├── __init__.py
│   └── profile_tasks.py    # Task instructions for agents
├── tools/                   # Custom document reading tools
│   ├── __init__.py
│   └── document_readers.py # PDF, DOCX, PPTX readers
├── profiles/                # 👈 Place candidate profiles here
│   ├── candidate1.pdf
│   ├── candidate2.docx
│   └── candidate3.pptx
├── job_descriptions/        # 👈 Place JD files here (filename = team name!)
│   ├── Engineering.pdf      # Team name: "Engineering"
│   ├── DataScience.docx     # Team name: "DataScience"
│   └── DevOps.pptx          # Team name: "DevOps"
├── main.py                  # Main application
├── config.py                # Configuration settings
├── requirements.txt         # Dependencies
├── .env.example            # Environment template
└── README.md               # This file
```

**Important**: JD filenames become team names! If your JD file is `Backend_Engineering.pdf`, the team name will be "Backend_Engineering".

## 💼 Usage

### Step 1: Prepare Your Documents

1. **Add Candidate Profiles** to the `profiles/` directory:
   - Supported formats: `.pdf`, `.docx`, `.pptx`
   - Each file should contain candidate information (name, contact, skills, experience)

2. **Add Job Descriptions** to the `job_descriptions/` directory:
   - Supported formats: `.pdf`, `.docx`, `.pptx`
   - **IMPORTANT**: The filename (without extension) becomes the team name
   - Examples:
     - `Engineering.pdf` → Team: "Engineering"
     - `Data_Science.docx` → Team: "Data_Science"
     - `Product_Management.pptx` → Team: "Product_Management"
   - Each JD should contain job requirements, required skills, experience levels, etc.

### Step 2: Run the System

```powershell
python main.py
```

The system will:
1. ✅ Read all profiles from `profiles/` directory
2. ✅ Read all JDs from `job_descriptions/` directory (extracting team names from filenames)
3. ✅ Match each candidate against **ALL teams**
4. ✅ Display results in a formatted table in the console

### Step 3: Review Results

The matching report is displayed as a table in your console:

```
╔═══════════════════════════════════════╦═══════╦════════════════╦══════════════╦═══════════════════╦══════════════════╗
║ Matching Team(s)                      ║ Score ║ Candidate Name ║ Phone Number ║ Email             ║ LinkedIn Profile ║
╠═══════════════════════════════════════╬═══════╬════════════════╬══════════════╬═══════════════════╬══════════════════╣
║ Engineering (85), DevOps (72)         ║ 85    ║ John Doe       ║ +1-555-0123  ║ john@example.com  ║ linkedin.com/... ║
║ DataScience (78)                      ║ 78    ║ Jane Smith     ║ +1-555-0456  ║ jane@example.com  ║ linkedin.com/... ║
║ No suitable match found               ║ N/A   ║ Bob Johnson    ║ Not Available║ bob@example.com   ║ Not Available    ║
╚═══════════════════════════════════════╩═══════╩════════════════╩══════════════╩═══════════════════╩══════════════════╝
```

**Table Columns:**
- **Matching Team(s)**: All teams with score ≥ 60, sorted by score (or "No suitable match found")
- **Score**: Highest match score for that candidate
- **Candidate Name**: Full name from profile
- **Phone Number**: Contact phone
- **Email**: Email address
- **LinkedIn Profile**: LinkedIn URL

## 🔧 Customization

### Switching LLM Providers

Simply edit your `.env` file:

**Use Claude (Recommended):**
```bash
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=your_key_here
CLAUDE_MODEL=claude-3-haiku-20240307  # Fast and cost-effective
```

**Use OpenAI:**
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4-turbo-preview  # or gpt-4, gpt-3.5-turbo
```

### Using Different Directories

Edit `main.py`:

```python
from main import ProfileMatchSystem

system = ProfileMatchSystem(
    profiles_dir="custom/profiles/path",
    jd_dir="custom/jds/path"
)

report_data = system.run()
```

### Disabling Telemetry

To avoid CrewAI telemetry connection errors, add to `.env`:

```bash
OTEL_SDK_DISABLED=true
```

## 📊 Match Scoring

The system uses a weighted scoring algorithm for each candidate-team pair:

- **Technical Skills** (40%): Alignment with required technical skills
- **Experience Level** (30%): Years of experience match
- **Education** (15%): Educational qualifications
- **Overall Fit** (15%): General profile compatibility

**Matching Logic:**
- Candidates are matched against **ALL teams**
- A candidate can match with **multiple teams** simultaneously
- Only teams with score **≥ 60** are included in the match
- If no team scores ≥ 60, candidate is marked as "No suitable match found"

**Score Interpretation:**
- **80-100**: Excellent match (highly recommended)
- **60-79**: Good match (recommended)
- **40-59**: Moderate match (below threshold, not shown)
- **0-39**: Poor match (below threshold, not shown)

## 🐛 Troubleshooting

### Common Issues

1. **"No module named 'crewai'" or "'tabulate'"**
   - Solution: Run `pip install -r requirements.txt --upgrade`

2. **"API key not found"**
   - Create `.env` file from `.env.example`
   - For Claude: Set `ANTHROPIC_API_KEY=your_key`
   - For OpenAI: Set `OPENAI_API_KEY=your_key`
   - Or set environment variable: `$env:ANTHROPIC_API_KEY="your_key"` (PowerShell)

3. **"No profiles found" or "No JDs found"**
   - Ensure files are in the `profiles/` and `job_descriptions/` directories
   - Check file formats: `.pdf`, `.docx`, `.pptx` only
   - Verify files are not empty

4. **Telemetry connection errors** (`Connection aborted`, `Error 10054`)
   - This is harmless and doesn't affect functionality
   - To disable: Add `OTEL_SDK_DISABLED=true` to your `.env` file

5. **"Could not parse JSON from result"**
   - The LLM didn't return valid JSON
   - Try running again (occasional parsing issue)
   - Check if LLM API is working properly

6. **Document parsing errors**
   - Ensure files are not corrupted
   - Password-protected files are not supported
   - Very large files may cause memory issues

7. **"Module 'langchain_anthropic' not found"**
   - Run: `pip install langchain-anthropic anthropic`

8. **Team names are wrong**
   - Remember: Team name = JD filename (without extension)
   - Check your JD filenames in `job_descriptions/` folder
   - Rename files to reflect correct team names

## 📋 Requirements

Dependencies (from `requirements.txt`):
```
crewai>=0.28.0
crewai-tools>=0.1.0
PyPDF2>=3.0.0
python-docx>=1.0.0
python-pptx>=0.6.21
openai>=1.0.0
anthropic>=0.18.0
langchain>=0.1.0
langchain-openai>=0.0.5
langchain-anthropic>=0.1.0
python-dotenv>=1.0.0
tabulate>=0.9.0
```

## 📝 Example Documents

### Job Description Format

**Filename**: `Engineering.pdf` (will be read as team name "Engineering")

**Content**:
```
Position: Senior Software Engineer
Department: Engineering

Required Skills:
- Python, JavaScript, React, Node.js
- AWS, Docker, Kubernetes
- REST APIs, Microservices

Experience Required: 5+ years in software development
Education: Bachelor's in Computer Science or related field

Responsibilities:
- Design and develop scalable applications
- Lead technical discussions
- Mentor junior developers

Preferred Qualifications:
- Experience with CI/CD pipelines
- Cloud architecture certification
```

### Candidate Profile Format

**Filename**: `john_doe.pdf` (any name is fine)

**Content**:
```
John Doe
Email: john.doe@example.com
Phone: +1-555-123-4567
LinkedIn: linkedin.com/in/johndoe

Summary:
Senior Software Engineer with 7 years of experience...

Skills:
Python, JavaScript, React, Node.js, AWS, Docker, PostgreSQL

Experience:
Senior Developer at TechCorp (2020-Present)
- Built microservices architecture using Python and Node.js
- Deployed applications on AWS with Docker

Software Engineer at StartupXYZ (2018-2020)
- Developed React applications
- Worked with REST APIs

Education:
B.S. Computer Science, State University (2018)

Certifications:
AWS Solutions Architect
```

## 🎯 How The System Works

1. **Profile Parsing**: Agents read ALL candidate profiles and extract:
   - Name, email, phone, LinkedIn
   - Skills (technical & soft)
   - Years of experience
   - Education and certifications

2. **JD Parsing**: Agents read ALL job descriptions and extract:
   - **Team name** from filename (e.g., `Engineering.pdf` → "Engineering")
   - Required skills from document content
   - Experience requirements from document
   - Education requirements from document

3. **Matching**: For EACH candidate, the matcher agent:
   - Compares against EVERY team
   - Calculates a score (0-100) for each team
   - Includes all teams with score ≥ 60

4. **Reporting**: The report generator creates JSON output internally, which is displayed as a formatted table

## 🚀 Quick Start Example

```powershell
# 1. Setup
git clone <your-repo>
cd ProfileMatch
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY or OPENAI_API_KEY

# 3. Add documents
# Place resumes in profiles/
# Place JDs in job_descriptions/ (filename = team name!)

# 4. Run
python main.py

# 5. View results in console table
```

## 🔐 Security Notes

- Keep your `.env` file secure and **never commit it to version control**
- The `.env` file contains sensitive API keys
- Add `.env` to `.gitignore` if using Git
- Candidate profiles may contain PII (Personally Identifiable Information) - handle responsibly

## ⚙️ Configuration Options

All settings in `.env`:

| Variable | Options | Default | Description |
|----------|---------|---------|-------------|
| `LLM_PROVIDER` | `openai`, `claude` | `claude` | Which LLM to use |
| `ANTHROPIC_API_KEY` | Your API key | - | Claude API key |
| `CLAUDE_MODEL` | Model name | `claude-3-haiku-20240307` | Claude model to use |
| `OPENAI_API_KEY` | Your API key | - | OpenAI API key |
| `OPENAI_MODEL` | Model name | `gpt-4-turbo-preview` | OpenAI model to use |
| `OPENAI_TEMPERATURE` | 0.0 - 1.0 | `0.7` | Creativity level |
| `OTEL_SDK_DISABLED` | `true`, `false` | `true` | Disable telemetry |
| `PROFILES_DIR` | Directory path | `profiles` | Where to find profiles |
| `JD_DIR` | Directory path | `job_descriptions` | Where to find JDs |

## 🤝 Support & Resources

- **CrewAI Documentation**: https://docs.crewai.com
- **Anthropic API Docs**: https://docs.anthropic.com
- **OpenAI API Docs**: https://platform.openai.com/docs

## 💡 Tips for Best Results

1. **Name your JD files clearly**: The filename becomes the team name (e.g., `Backend_Engineering.pdf`)
2. **Consistent formatting**: Well-formatted profiles and JDs improve extraction accuracy
3. **Include key details**: Make sure profiles have contact info and skills clearly listed
4. **Specify requirements**: JDs should clearly state required skills and experience levels
5. **Use verified models**: `claude-3-haiku-20240307` is tested and works reliably

## 🎉 What's Different in This System?

✅ **Multi-team matching**: Candidates can match with multiple teams, not just one  
✅ **Console output**: Results displayed in a clean table, no file saving needed  
✅ **Filename = Team name**: Simple convention for team identification  
✅ **Custom readers**: Lightweight document parsing without complex dependencies  
✅ **Threshold-based**: Only shows matches with score ≥ 60  
✅ **Multiple formats**: Supports PDF, DOCX, and PPTX for both profiles and JDs  

## 📄 License

This project is for internal use. Modify as needed for your organization.

---

**Ready to match candidates?** Add your documents and run `python main.py`! 🚀
