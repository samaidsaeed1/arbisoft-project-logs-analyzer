import csv
import re
import sys
import os
from collections import defaultdict
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def get_file_path():
    """Get CSV file path from command line args or user input"""
    # Check if file provided as command line argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.isfile(file_path) and file_path.endswith('.csv'):
            return file_path
    
    # Otherwise, ask for file path input
    print("\nPlease enter the path to your CSV file:")
    file_path = input("> ")
    
    if not os.path.isfile(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
        
    if not file_path.endswith('.csv'):
        print("Warning: File does not have .csv extension")
        confirm = input("Continue anyway? (y/n): ")
        if confirm.lower() != 'y':
            sys.exit(0)
    
    return file_path

def get_patterns():
    print("Enter the regular expression for ticket numbers (default: \\[PF\\d+-\\d+\]):")
    ticket_pattern = input("> ").strip()
    if not ticket_pattern:
        ticket_pattern = r'\[PF\d+-\d+\]'
    print("Enter the regular expression for PR numbers (default: \\bPR-\\d+\\b):")
    pr_pattern = input("> ").strip()
    if not pr_pattern:
        pr_pattern = r'\bPR-\d+\b'
    return ticket_pattern, pr_pattern

def analyze_project_logs(csv_file, ticket_pattern, pr_pattern):
    # Initialize counters
    total_entries = 0
    violations = {
        "missing_ticket": [],
        "exceeds_time_limit": [],
        "missing_pr_reference": []
    }
    
    # Read CSV file
    try:
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                description = row.get("Description", "")
                date = row.get("Date", "Unknown date")
                
                # Extract individual task entries using regex
                # Format: [Category] - Optional[Ticket] - Description (Hours)
                tasks = re.findall(r'\[([\w\s-]+)\](.*?)(\d+\.\d+|\d+)', description)
                
                for category, details, hours in tasks:
                    total_entries += 1
                    hours = float(hours)
                    category = category.strip()
                    details = details.strip()
                    
                    # Check for ticket numbers in coding/testing/debugging tasks
                    if category.lower() in ["coding", "testing", "debug", "debugging"]:
                        if not re.search(ticket_pattern, details):
                            violations["missing_ticket"].append({
                                "date": date,
                                "category": category,
                                "details": details,
                                "hours": hours
                            })
                    
                    # Check for tasks exceeding 3 hours
                    if hours > 3:
                        violations["exceeds_time_limit"].append({
                            "date": date,
                            "category": category,
                            "details": details,
                            "hours": hours
                        })
                    
                    # Check PR reviews for references
                    if "review" in category.lower() or "pr" in category.lower():
                        has_pr_number = bool(re.search(pr_pattern, details))
                        has_ticket = bool(re.search(ticket_pattern, details))
                        
                        if not (has_pr_number or has_ticket):
                            violations["missing_pr_reference"].append({
                                "date": date,
                                "category": category,
                                "details": details,
                                "hours": hours
                            })
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)
    
    # Calculate statistics
    stats = {
        "total_entries": total_entries,
        "missing_ticket_count": len(violations["missing_ticket"]),
        "missing_ticket_percent": (len(violations["missing_ticket"]) / total_entries) * 100 if total_entries else 0,
        "exceeds_time_limit_count": len(violations["exceeds_time_limit"]),
        "exceeds_time_limit_percent": (len(violations["exceeds_time_limit"]) / total_entries) * 100 if total_entries else 0,
        "missing_pr_reference_count": len(violations["missing_pr_reference"]),
        "missing_pr_reference_percent": (len(violations["missing_pr_reference"]) / total_entries) * 100 if total_entries else 0
    }
    
    return stats, violations

def generate_pdf_report(stats, violations, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    y = height - 50
    line_height = 16

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "PROJECT LOG ANALYSIS REPORT")
    y -= 30
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Total entries analyzed: {stats['total_entries']}")
    y -= 30

    def draw_section(title, count, percent, items):
        nonlocal y
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, title)
        y -= line_height
        c.setFont("Helvetica", 11)
        c.drawString(60, y, f"Violations: {count} ({percent:.1f}%)")
        y -= line_height
        for v in items:
            text = f"- {v['date']}: [{v['category']}] {v['details']} ({v['hours']})"
            c.drawString(70, y, text[:100])  # Truncate if too long
            y -= line_height
            if y < 60:
                c.showPage()
                y = height - 50
        y -= 10

    draw_section(
        "1. MISSING TICKET NUMBERS IN CODING/TESTING/DEBUGGING:",
        stats['missing_ticket_count'],
        stats['missing_ticket_percent'],
        violations["missing_ticket"]
    )
    draw_section(
        "2. TASKS EXCEEDING 3 HOURS:",
        stats['exceeds_time_limit_count'],
        stats['exceeds_time_limit_percent'],
        violations["exceeds_time_limit"]
    )
    draw_section(
        "3. PR REVIEWS WITHOUT REFERENCES:",
        stats['missing_pr_reference_count'],
        stats['missing_pr_reference_percent'],
        violations["missing_pr_reference"]
    )
    c.save()

if __name__ == "__main__":
    print("Project Log Analyzer")
    print("-------------------")
    
    # Get file path from command line or prompt
    csv_file = get_file_path()
    print(f"Analyzing: {csv_file}")
    
    # Get regex patterns for ticket and PR numbers
    ticket_pattern, pr_pattern = get_patterns()
    
    # Analyze the selected file
    stats, violations = analyze_project_logs(csv_file, ticket_pattern, pr_pattern)
    
    # Get PDF output path
    default_pdf = os.path.splitext(csv_file)[0] + "_report.pdf"
    print(f"Enter output PDF file path (default: {default_pdf}):")
    pdf_path = input("> ").strip()
    if not pdf_path:
        pdf_path = default_pdf
    
    generate_pdf_report(stats, violations, pdf_path)
    print(f"\nPDF report generated: {pdf_path}\nAnalysis complete! Press Enter to exit...")
    input()
