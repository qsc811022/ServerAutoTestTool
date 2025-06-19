import csv
import json
import subprocess
from dataclasses import dataclass
from typing import List

import paramiko


@dataclass
class Server:
    ip: str
    user: str
    password: str


class ServerHealthChecker:
    """Perform health checks on a list of servers."""

    def __init__(self, servers: List[Server]):
        self.servers = servers

    def ping(self, server: Server) -> bool:
        """Return True if the host responds to a ping request."""
        try:
            result = subprocess.run(
                ["ping", "-c", "1", "-W", "1", server.ip],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            return result.returncode == 0
        except Exception:
            return False

    def query_stats(self, server: Server):
        """Return disk usage and CPU usage via SSH."""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(
                server.ip,
                username=server.user,
                password=server.password,
                timeout=5,
            )
            stdin, stdout, _ = ssh.exec_command("df -P / | tail -1")
            disk_line = stdout.readline()
            disk_usage = disk_line.split()[4] if disk_line else ""

            stdin, stdout, _ = ssh.exec_command("top -bn1 | grep 'Cpu(s)'")
            cpu_line = stdout.readline()
            if cpu_line:
                cpu_usage = cpu_line.split("%")[0].split()[-1] + "%"
            else:
                cpu_usage = ""
            ssh.close()
            return disk_usage, cpu_usage
        finally:
            try:
                ssh.close()
            except Exception:
                pass

    def run(self, report_file: str):
        """Execute checks and write the result CSV."""
        with open(report_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                "IP",
                "Ping",
                "Disk Usage",
                "CPU Usage",
                "Status",
            ])
            for server in self.servers:
                status = "OK"
                ping_ok = self.ping(server)
                disk_usage = ""
                cpu_usage = ""
                if ping_ok:
                    try:
                        disk_usage, cpu_usage = self.query_stats(server)
                    except Exception as exc:  # pragma: no cover - network
                        status = f"Error: {exc}"
                else:
                    status = "Ping failed"
                writer.writerow(
                    [server.ip, ping_ok, disk_usage, cpu_usage, status]
                )


def load_servers(path: str) -> List[Server]:
    """Load server configuration from a JSON file."""
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return [Server(**item) for item in data.get("servers", [])]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Server health check tool")
    parser.add_argument("config", help="Path to server config JSON")
    parser.add_argument(
        "report", help="Output CSV path", nargs="?", default="report.csv"
    )
    args = parser.parse_args()

    servers = load_servers(args.config)
    checker = ServerHealthChecker(servers)
    checker.run(args.report)
