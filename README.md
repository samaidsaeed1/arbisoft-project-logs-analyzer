# Project Log Analyzer

A Python script that analyzes project time logs stored in CSV format to identify compliance violations and generate detailed PDF reports.

## Features

- **Automated Log Analysis**: Parses CSV files containing project time logs
- **Violation Detection**: Identifies three types of compliance violations:
  - Missing ticket numbers in coding/testing/debugging tasks
  - Tasks exceeding 3-hour time limits
  - PR reviews without proper references
- **PDF Report Generation**: Creates professional PDF reports with detailed findings
- **Customizable Patterns**: Allows custom regular expressions for ticket and PR number formats
- **Command Line Support**: Can be run with file path as argument or interactively

## Requirements

### Dependencies

Install the required Python packages:

```bash
pip install reportlab
```

### Python Version

- Python 3.6 or higher

## Installation

1. Download the `analyze_logs.py` script
2. Install dependencies:
   ```bash
   pip install reportlab
   ```
3. Make the script executable (optional):
   ```bash
   chmod +x analyze_logs.py
   ```

## Usage

### Command Line Usage

```bash
python analyze_logs.py [csv_file_path]
```

### Interactive Usage

```bash
python analyze_logs.py
```

The script will prompt you for:
1. CSV file path (if not provided as argument)
2. Regular expression pattern for ticket numbers (default: `\[PF\d+-\d+\]`)
3. Regular expression pattern for PR numbers (default: `\bPR-\d+\b`)
4. Output PDF file path (default: `[csv_filename]_report.pdf`)

## CSV File Format

The script expects a CSV file with the following columns:
- **Date**: Date of the log entry
- **Description**: Task descriptions in the format: `[Category] - Details (Hours)`

### Example CSV Content

```csv
Date,Description
2023-10-01,"[Coding] - Implemented user authentication [PF123-45] (2.5) [Testing] - Unit tests for auth module [PF123-45] (1.0)"
2023-10-02,"[Debug] - Fixed login issue (4.0) [Review] - Code review for PR-789 (0.5)"
```

## Task Format

Tasks within the Description field should follow this pattern:
```
[Category] - Task details with optional ticket/PR references (Hours)
```

### Categories

The script recognizes these categories for specific validations:
- **Coding/Testing/Debug**: Requires ticket numbers
- **Review/PR**: Requires PR or ticket references

## Validation Rules

### 1. Missing Ticket Numbers
- **Applies to**: Coding, Testing, Debug, Debugging tasks
- **Rule**: These tasks must contain ticket numbers matching the specified pattern
- **Default Pattern**: `\[PF\d+-\d+\]` (e.g., [PF123-45])

### 2. Time Limit Violations
- **Applies to**: All tasks
- **Rule**: No single task should exceed 3 hours
- **Rationale**: Encourages task breakdown and better time management

### 3. Missing PR References
- **Applies to**: Review and PR-related tasks
- **Rule**: Must contain either PR numbers or ticket references
- **Default PR Pattern**: `\bPR-\d+\b` (e.g., PR-789)

## Output

### Console Output
- Summary statistics
- Violation counts and percentages
- Progress indicators

### PDF Report
The generated PDF report includes:
- **Header**: Total entries analyzed
- **Section 1**: Missing ticket numbers in coding/testing/debugging tasks
- **Section 2**: Tasks exceeding 3-hour time limit
- **Section 3**: PR reviews without proper references

Each violation entry shows:
- Date of occurrence
- Task category
- Task details
- Hours logged

## Examples

### Basic Usage
```bash
python analyze_logs.py project_logs.csv
```

### Custom Patterns
When prompted, you can specify custom regex patterns:
- Ticket pattern: `\[JIRA-\d+\]`
- PR pattern: `\bGH-\d+\b`

### Sample Output
```
Project Log Analyzer
-------------------
Analyzing: project_logs.csv
Enter the regular expression for ticket numbers (default: \[PF\d+-\d+\]):
> 
Enter the regular expression for PR numbers (default: \bPR-\d+\b):
> 
Enter output PDF file path (default: project_logs_report.pdf):
> 

PDF report generated: project_logs_report.pdf
Analysis complete! Press Enter to exit...
```

## Error Handling

The script handles various error conditions:
- **File not found**: Exits with error message
- **Invalid CSV format**: Continues with warning
- **Non-CSV files**: Prompts for confirmation
- **Malformed data**: Skips problematic entries and continues

## Customization

### Modifying Validation Rules

To change the 3-hour time limit:
```python
if hours > 3:  # Change this value
```

To add new categories requiring tickets:
```python
if category.lower() in ["coding", "testing", "debug", "debugging", "new_category"]:
```

### Adding New Violation Types

The script can be extended to check for additional violations by:
1. Adding new violation types to the `violations` dictionary
2. Implementing detection logic in the main analysis loop
3. Adding corresponding sections to the PDF report generator

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'reportlab'**
   - Solution: `pip install reportlab`

2. **File encoding issues**
   - Ensure CSV file is UTF-8 encoded
   - Try opening the CSV in a text editor and re-saving

3. **Regex pattern not matching**
   - Test your patterns using online regex tools
   - Remember to escape special characters

4. **PDF generation fails**
   - Check write permissions in the output directory
   - Ensure sufficient disk space
