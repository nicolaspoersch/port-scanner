# Port Scanner 💠

## Description 📖

The Port Scanner is a simple tool for port analysis on a specific domain. Developed for ethical and educational use, it allows users to identify which ports are open or closed and even send messages to open ports.

## Features ⚙️

### 1. Domain Information Retrieval ⛓️

- Uses the `socket` library to retrieve information about the domain, including associated IP addresses and registrar details.
- Integrates WHOIS query functionality using the `whois` library.

### 2. Port Scanning 🔮

- Offers three scanning options:
  - Common port scan.
  - Port scan from a custom list.
  - Scan a custom range of ports.

### 3. Sending Messages to Open Ports 🗝️

- Allows users to send messages to open ports.
- Utilizes the `socket` library to establish connections and send/receive messages.

## Installation 📜

### Prerequisites

- Ensure you have Python 3.x installed on your system.

### Installation Steps 🔍

1. **Run the Installation Script (Windows):**
   - Open the terminal in the project folder.
   - Run the `install_dependencies.bat` script.
     ```bash
     install_dependencies.bat or just open the archive
     ```

2. **Run the Program:**
   - After installation is complete, run the following command:
     ```bash
     python port_scanner.py or just open the archive
     ```

## Usage 🧷

1. **Initial Execution:**
   - Upon starting the program, you will be asked to agree to using the tool ethically.

2. **Domain Information Retrieval:**
   - Enter the target domain when prompted.

3. **Choose a Scanning Option:**
   - Select from common scanning, scanning from a list, or a custom range scan.

4. **Scan Customization:**
   - Depending on the chosen option, you will be prompted to provide additional information, such as timeout and, for a range scan, the starting and ending ports.

5. **Results and Additional Actions:**
   - The scan results will be displayed, indicating open and closed ports.
   - If there are open ports, you will have the option to send messages to these ports.

6. **Program Closure:**
   - You can choose to perform new scans or exit the program.

## Important Notes 📑

- This project is intended for ethical and educational purposes only. Unauthorized or malicious use is strictly prohibited.

- Make sure to agree with ethical policies before using the tool.

- If you encounter issues or have improvement suggestions, feel free to contribute to the GitHub repository.

**Note:** The program has been tested and developed until October 1, 2023. Future changes to the Python environment or the used libraries may affect the program's functionality. Suggestions and requests for updates are welcome.

## Updates 🔄

1. **Domain Change Option (Oct 2, 2023):**
   - Added the option to change the domain at the beginning of the program for user convenience.

2. **Domain Change After Port Scan (Oct 2, 2023):**
   - Implemented the option to change the domain after the port scan, providing flexibility to the user.

3. **New Scan Option Without Open Ports (Oct 2, 2023):**
   - Users now have the option to perform a new scan if no open ports are detected, enhancing the tool's usability.

4. **New Scan After Rejecting Message Sending (Oct 2, 2023):**
   - Added the option to perform a new scan after rejecting the sending of messages to open ports.

5. **Message Sending Without Prior Scan (Oct 2, 2023):**
   - Implemented the option to send messages to ports without the need for a prior port scan.

**Temporary Update (Oct 2, 2023):**
- The color feature has been temporarily removed for refinement.

Feel free to reach out if you need anything else! 💖
