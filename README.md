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
- **openai (1.55.0+)**: OpenAI API client for vulnerability analysis and classification
- **playwright (1.49.0+)**: Comprehensive browser automation framework
- **pandas (2.2.3+)**: Data processing and CSV handling
- **typer (0.13.1+)**: Modern CLI interface builder based on Python type hints

### Testing & Automation
- **playwright (1.49.0+)**: Headless browser automation
  - Used for XSS testing and exploitation
  - Interface vulnerability scanning
  - Screenshot capture
  - Network request monitoring
- **pyee (12.0.0+)**: Python EventEmitter implementation for automation events

### Data Processing & Validation
- **pandas (2.2.3+)**: CSV processing and data manipulation
- **numpy (2.1.3+)**: Numerical operations and data analysis support
- **python-dateutil (2.9.0+)**: Powerful extensions to datetime
- **pydantic (2.10.1+)**: Data validation using Python type annotations
- **pydantic-core (2.27.1+)**: Core functionality for Pydantic
- **annotated-types (0.7.0+)**: Type annotation support
- **typing-extensions (4.12.2+)**: Backported typing hints

### HTTP & Networking
- **httpx (0.27.2+)**: Modern HTTP client with async support
- **httpcore (1.0.7+)**: HTTP transport library
- **anyio (4.6.2+)**: Asynchronous I/O support
- **h11 (0.14.0+)**: HTTP/1.1 protocol implementation
- **sniffio (1.3.1+)**: Async library detection
- **requests (2.32.3+)**: HTTP library for synchronous requests
- **urllib3 (2.2.3+)**: HTTP client library
- **charset-normalizer (3.4.0+)**: Character encoding detection
- **certifi (2024.8.30+)**: Mozilla's SSL certificates

### UI & Formatting
- **rich (13.9.4+)**: Rich text and formatting in the terminal
- **tqdm (4.67.0+)**: Fast, extensible progress bars
- **click (8.1.7+)**: Command line interface creation kit
- **shellingham (1.5.4+)**: Shell detection for CLI tools
- **pygments (2.18.0+)**: Syntax highlighting
- **markdown-it-py (3.0.0+)**: Markdown parser
- **mdurl (0.1.2+)**: URL utilities for markdown processing

### Utility Libraries
- **pathlib (1.0.1+)**: Object-oriented filesystem paths
- **jiter (0.7.1+)**: Iterator utilities
- **greenlet (3.1.1+)**: Lightweight in-process concurrent programming
- **distro (1.9.0+)**: OS platform information
- **six (1.16.0+)**: Python 2 and 3 compatibility
- **pytz (2024.2+)**: Timezone calculations
- **tzdata (2024.2+)**: Timezone database
- **idna (3.10+)**: Internationalized Domain Names support

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
