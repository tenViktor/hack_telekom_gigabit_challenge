# Automated Vulnerability Scanner

A containerized CLI tool for automated vulnerability scanning and exploitation. The tool processes vulnerability scan results and automatically performs security testing using browser automation and specialized exploits.

## Quick Start

````bash
# Pull the image
docker pull yourusername/vuln-scanner:latest

# Run the scanner
docker run \
    -e OPENAI_API_KEY="your-api-key-here" \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/results:/app/results \
    vuln-scanner \
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

## Dependencies

Key dependencies used in this project:

### Core Dependencies
- **openai (1.55.0+)**: OpenAI API client for vulnerability analysis
- **playwright (1.49.0+)**: Browser automation for vulnerability testing
- **pandas (2.2.3+)**: Data processing and CSV handling
- **typer (0.13.1+)**: CLI interface management

### Testing & Automation
- **playwright**: Headless browser automation
  - Used for XSS testing
  - Interface vulnerability scanning
  - Screenshot capture
  - Network request monitoring

### Data Processing
- **pandas**: CSV processing and data manipulation
- **numpy (2.1.3+)**: Numerical operations support
- **python-dateutil (2.9.0+)**: Date handling utilities

### UI & Formatting
- **rich (13.9.4+)**: Terminal formatting and progress display
- **tqdm (4.67.0+)**: Progress bars for long-running operations

### API & Networking
- **httpx (0.27.2+)**: HTTP client for API interactions
- **anyio (4.6.2+)**: Asynchronous I/O support
- **pydantic (2.10.1+)**: Data validation and settings management

All dependencies are automatically handled by the Docker container. If running locally, install via:

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
docker run -v $(pwd)/results:/app/results vuln-scanner \
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
