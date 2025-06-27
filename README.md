# QUIZR - Command-Line Quiz Tool with Spaced Repetition

QUIZR is a powerful command-line interface (CLI) tool designed to help you learn and retain information through spaced repetition. It supports both text-based and image-based questions, organized in a flexible folder structure.

## Features

- **Spaced Repetition**: Intelligent scheduling based on your performance
- **Multiple Quiz Modes**: 
  - `spaced` - Focuses on questions due for review
  - `shuffle` - Randomizes question order
  - `quick` - Practice with a random subset of questions
- **Image Support**: Display images alongside questions
- **Progress Tracking**: Detailed statistics and performance metrics
- **Flexible Organization**: Folder-based quiz organization
- **Fuzzy Matching**: Configurable answer matching with 90% similarity threshold

## Installation

### **Method 1: One-Click Installer (Recommended for Users)**

**Windows:**
```bash
# Double-click the installer or run in terminal:
.\install.bat
```

**Mac/Linux:**
```bash
# Run the installer script:
./install.sh
```

### **Method 2: Manual Installation (For Developers)**

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install QUIZR:
```bash
pip install -e .
```

### **Method 3: From PyPI (Future)**
Once published to PyPI:
```bash
pip install quizr
quizr list  # Direct command available
```

### **Cross-Platform Compatibility**

| Platform | Installer | Command |
|----------|-----------|---------|
| Windows | `install.bat` | Double-click or `.\install.bat` |
| Mac | `install.sh` | `./install.sh` |
| Linux | `install.sh` | `./install.sh` |

**Note:** The one-click installers provide the same functionality across all platforms:
- ✅ Check Python/pip installation
- ✅ Install dependencies automatically  
- ✅ Install QUIZR package
- ✅ Test installation
- ✅ Provide usage instructions

## Quick Start

1. **Create your first quiz**: Create a YAML file with questions
2. **List available quizzes**: `python -m quizr list`
3. **Start a quiz session**: `python -m quizr start <quiz_name>`
4. **View progress**: `python -m quizr progress`

## Quiz Format

Create quiz files in YAML format with the following structure:

```yaml
# Example: Network_Basics.yaml
q_001:
  prompt: "What is the default port number for HTTP?"
  answer: "80"
  strict: true  # Optional: disable fuzzy matching

q_002:
  prompt: "What protocol uses port 443?"
  answer: "HTTPS"

q_003:
  image: "network_diagram.png"  # Image in /images folder
  prompt: "What port does SSH use in this diagram?"
  answer: "22"
```

## Directory Structure

Organize your quizzes in folders for better management:

```
your_quiz_directory/
├── images/                    # All images go here
│   ├── diagram1.png
│   └── exercise2_q1.png
├── CompTIA/
│   ├── Network+/
│   │   ├── Port_Numbers.yaml
│   │   ├── Protocols.yaml
│   │   └── Network_Definitions.yaml
│   └── Security+/
│       ├── Threats.yaml
│       └── Cryptography.yaml
└── progress.yaml              # Auto-generated progress tracking
```

## Commands

### List Quizzes
```bash
python -m quizr list
```
Shows all available quizzes in a hierarchical view with question counts.

### Start Quiz Session
```bash
python -m quizr start <target> [mode]
```

Examples:
- `python -m quizr start network+` - Start all Network+ quizzes in spaced mode
- `python -m quizr start comptia quick` - Quick mode with random questions from CompTIA folder
- `python -m quizr start port_numbers shuffle` - Shuffle mode for specific quiz

**Modes:**
- `spaced` (default) - Spaced repetition based on due dates and performance
- `shuffle` - All questions in random order
- `quick` - Random subset of 10 questions

### View Progress
```bash
python -m quizr progress [target]
```

Examples:
- `python -m quizr progress` or `python -m quizr progress global` - Global statistics
- `python -m quizr progress network+` - Folder-level statistics
- `python -m quizr progress port_numbers` - Specific quiz statistics

### Quit Session
During a quiz session, type `!quit` or `!abort` to end early and see results.

## Features in Detail

### Spaced Repetition Algorithm
QUIZR uses an intelligent algorithm that:
- Prioritizes never-seen questions
- Schedules reviews based on your performance history
- Increases intervals for questions you answer correctly
- Brings back recently failed questions sooner

### Answer Evaluation
- **Exact matching**: Case-insensitive exact matches
- **Fuzzy matching**: 90% similarity threshold (configurable)
- **Strict mode**: Disable fuzzy matching per question with `strict: true`

### Image Support
- Place images in the `/images` folder
- Reference them by filename in your YAML files
- Images open automatically with your system's default viewer
- Use non-descriptive filenames to avoid giving away answers

### Progress Tracking
- Per-question statistics (attempts, accuracy, last review)
- Folder and global aggregation
- Session tracking with duration and results
- Daily activity logs

## Example Session

```bash
$ python -m quizr start network+ spaced

============================================================
Starting spaced mode session with 15 questions
Target: network+
============================================================

What is the default port number for HTTP?

Your answer: 80
✓ Correct!

What protocol uses port 443?

Your answer: https
✓ Correct!

[Session continues...]

============================================================
Exercise Complete: Network+
============================================================
Mode                  : spaced
Questions Attempted   : 15
Correct Answers       : 13
Correct Answers %     : 86.7%
Session Duration      : 00:05:42
============================================================
```

## Tips for Creating Good Quizzes

1. **Use clear, unambiguous questions**
2. **Keep answers concise**
3. **Use non-descriptive image filenames** (e.g., `ex1_q3.png` instead of `http_port_diagram.png`)
4. **Group related questions in folders**
5. **Use strict mode for exact terminology**
6. **Include both easy and challenging questions**

## Troubleshooting

### Installation Issues

**Windows installer won't run**: Right-click `install.bat` → "Run as administrator" if you get permission errors.

**Mac/Linux installer won't run**: Make the script executable first:
```bash
chmod +x install.sh
./install.sh
```

**Python not found**: Install Python from [python.org](https://python.org) or your system's package manager.

**Permission errors during installation**: Try installing with user privileges:
```bash
pip install --user -r requirements.txt
pip install --user -e .
```

### Usage Issues

**No quizzes found**: Ensure you have `.yaml` files in your current directory or subdirectories.

**Image won't open**: Check that the image exists in the `/images` folder and your system has a default image viewer.

**Progress not saving**: Ensure the directory is writable and you have permissions to create files.

## Development

This project is built with Python and uses:
- **Click** for CLI interface
- **PyYAML** for data storage
- **FuzzyWuzzy** for intelligent answer matching
- **Python-Levenshtein** for fast string matching

## License

MIT License - see LICENSE file for details.