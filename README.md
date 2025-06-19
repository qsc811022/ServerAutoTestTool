# Server Auto Test Tool

This repository provides a simple Python script for performing automated health checks on servers.

## Features

- Ping connectivity test
- Disk usage and CPU usage retrieval via SSH
- CSV report generation

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Prepare a JSON configuration file describing your servers. See `servers_sample.json` for the expected format.

Run the health check script:

```bash
python healthcheck.py servers.json report.csv
```

The script will ping each server, gather disk and CPU usage via SSH, and write the results to `report.csv`.
