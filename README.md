# Automated Vulnerability Scanner

A containerized CLI tool for automated vulnerability scanning and exploitation. The tool processes vulnerability scan results and automatically performs security testing using browser automation and specialized exploits.

## Quick Start

````bash
# Pull the image
docker pull yourusername/vuln-scanner:latest

# Run the scanner
docker run -v $(pwd)/results:/app/results yourusername/vuln-scanner \
    "http://target-url:3000" "/app/data/vulnerabilities.csv"

## Features

- Automated vulnerability classification based on OWASP Top 10
- Browser automation for XSS and interface-based vulnerabilities
- Specialized exploit runners for SQL Injection and XSS
- Automatic screenshot capture and result logging
- Support for standard security tool CSV outputs
- Rich CLI interface with progress tracking

## Prerequisites

- Docker
- Access to the target application
- Vulnerability scan results in CSV format

## Installation

### Using Pre-built Image

```bash
docker pull yourusername/vuln-scanner:latest
````

### Building Locally

```bash
git clone <repository-url>
cd automated-vulnerability-scanner
docker build -t vuln-scanner .
```

## Usage

### Directory Structure

Create the following directories in your working directory:

```bash
mkdir data results
```

### Running the Scanner

```bash
docker run -v $(pwd)/data:/app/data -v $(pwd)/results:/app/results vuln-scanner \
    "http://target-url:3000" "/app/data/vulnerabilities.csv"
```

### CSV Format

The tool expects a CSV file with the following headers:

```
Group Name,Project Name,Tool,Scanner Name,Status,Vulnerability,Details,Additional Info,Severity,CVE,CWE,Other Identifiers,Detected At,Location,Activity,Comments,Full Path,CVSS Vectors,Dismissal Reason
```

Required fields:

- `Vulnerability`: The type/name of the vulnerability
- `Details`: Description or additional information
- `Severity`: Vulnerability severity level

Other fields are optional but will be included in the results if present.

### Output

Results are stored in the mounted `results` directory:

```
results/
├── YYYYMMDD_HHMMSS_vulnerability_name.png    # Screenshots
├── YYYYMMDD_HHMMSS_vulnerability_name.json   # Test results
└── YYYYMMDD_HHMMSS_vulnerability_name.txt    # Test details
```

## Supported Vulnerability Types

Currently supports automated testing for:

- SQL Injection
- Cross-Site Scripting (XSS)
- Authentication Testing
- Basic Security Misconfigurations

Other vulnerability types will be logged but may require manual verification.

## Network Configuration

When testing local applications, use appropriate Docker networking:

```bash
# For host network
docker run --network host ...

# For Docker Compose networks
docker run --network your_network_name ...
```

## Security Notice

This tool is for educational and authorized testing purposes only. Always obtain proper authorization before testing any systems or applications. The authors are not responsible for any misuse or damage caused by this tool.
