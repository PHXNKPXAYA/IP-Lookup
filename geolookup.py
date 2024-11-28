import sys
import socket
import requests
import geocoder
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit
from PyQt5.QtCore import Qt
from datetime import datetime

# Function to scan ports
def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            return True
        else:
            return False
    except socket.error:
        return False

# Function to scan the target IP for open ports
def port_scanner(target, output_area):
    output_area.clear()
    output_area.append(f"Scanning Target: {target}")
    output_area.append(f"Scan started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Scanning ports 1 to 1024
    for port in range(1, 1025):
        if scan_port(target, port):
            output_area.append(f"Port {port} is OPEN")
        else:
            output_area.append(f"Port {port} is CLOSED")

    output_area.append(f"Scan completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Function to get IP information
def get_ip_info(output_area):
    ip_info = requests.get("https://ipinfo.io").json()
    output_area.append(f"IP Information: {ip_info}")

# Function to get geolocation information
def get_geolocation(ip, output_area):
    g = geocoder.ip(ip)
    output_area.append(f"Geolocation for IP {ip}: {g.latlng}, {g.city}, {g.country}")

# Function to perform DNS lookup using socket
def dns_lookup(website, output_area):
    try:
        result = socket.gethostbyname(website)
        output_area.append(f"DNS Lookup for {website}: {result}")
    except socket.gaierror:
        output_area.append(f"DNS Lookup failed for {website}")

# Main UI Class
class PortScannerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Network Tools")
        self.setGeometry(100, 100, 600, 600)
        self.setStyleSheet("background-color: #f0f0f0; font-size: 14px;")

        # Create layout and widgets
        self.layout = QVBoxLayout()

        # Target IP input
        self.target_input = QLineEdit(self)
        self.target_input.setPlaceholderText("Enter Target IP or Domain")
        self.layout.addWidget(self.target_input)

        # Port Scan button
        self.scan_button = QPushButton("Start Port Scan", self)
        self.scan_button.clicked.connect(self.start_port_scan)
        self.layout.addWidget(self.scan_button)

        # IP Info button
        self.ip_info_button = QPushButton("Get IP Information", self)
        self.ip_info_button.clicked.connect(self.show_ip_info)
        self.layout.addWidget(self.ip_info_button)

        # Geolocation button
        self.geo_button = QPushButton("Get Geolocation", self)
        self.geo_button.clicked.connect(self.show_geolocation)
        self.layout.addWidget(self.geo_button)

        # DNS Lookup button
        self.dns_button = QPushButton("DNS Lookup", self)
        self.dns_button.clicked.connect(self.show_dns_lookup)
        self.layout.addWidget(self.dns_button)

        # Output Text Area
        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        self.layout.addWidget(self.output_area)

        # Set layout
        self.setLayout(self.layout)

    # Start port scan
    def start_port_scan(self):
        target = self.target_input.text()
        if target:
            port_scanner(target, self.output_area)
        else:
            self.output_area.append("Please enter a valid target IP or Domain.")

    # Show IP information
    def show_ip_info(self):
        get_ip_info(self.output_area)

    # Show geolocation information
    def show_geolocation(self):
        ip = self.target_input.text()
        if ip:
            get_geolocation(ip, self.output_area)
        else:
            self.output_area.append("Please enter a valid IP to get geolocation.")

    # Show DNS lookup results
    def show_dns_lookup(self):
        website = self.target_input.text()
        if website:
            dns_lookup(website, self.output_area)
        else:
            self.output_area.append("Please enter a website for DNS lookup.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PortScannerApp()
    window.show()
    sys.exit(app.exec_())
