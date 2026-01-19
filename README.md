# Analisis-Forense-Tools
![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Index

- [Description](#description)
- [NFTS Tools](#ntfs)
## Description
Tools developed for the Forensic Analysis module of the professional training master's degree in cybersecurity
- __First steps__
```powershell
    # Download repository or clone
    git clone https://github.com/Sysop81/Analisis-Forense-Tools.git

    # Navigate to the folder app
    cd MFTExtractor

    # Finally into the folder app create a virtual environment and install dependencies
```
<!--
All tools with command-line output use color coding. Development and testing were performed using __PowerShell 5.1.26100.7462__. By default, color coding is disabled (ANSI support) in the console with administrator privileges.

**To activate it run:**
```powershell
    # Enable ANSI support in PowerShell
    Set-ItemProperty HKCU:\Console VirtualTerminalLevel -Type DWORD 1

    # Close and reopen PowerShell (as Administrator).
    
```
-->

## NTFS
- __MFTExtractor__. It is a tool for reading and extracting the Master File Table __(MFT)__ in an NTFS file system.
    - __Program installation__
    ```powershell
    # [IMPORTANT] Go inside the root directory of MFTExtractor

    # we create a virtual environment where we will install the necessary libraries. 
    python -m venv venv

    # Windows powershell
    venv\Scripts\activate

    # Install dependencies
    pip install -r requirements.txt

    ```
    - __Usage:__

    ```powershell
    # Launch app with default values
    python MFTExtractor.py

    # Show help
    python MFTExtractor.py -h

    # Use personalized values
    # -i D . [Input value] To use the volume D . By default is C
    # -o MyMFT.bin . [Output value] To build output binary with the file name "MyMFT.bin"
    python MFTExtractor.py -i D -o MyMFT.bin
    ```
    When the program finishes, we will obtain the output binary in the __output__ folder located in the root directory of MFTExtractor.

    Inside, we will find: 
        
    |File| Description|
    |----|------------|
    |__file_name.bin__| File containing the extracted MFT content|
    |__file_name.txt__| File containing the program description, date, time, and MD5 and SHA 256 hashes|    

- __MFTParser__. This tool parses MFT attributes data from a binary MFT file and exports it to Excel or CSV.
    - __Program installation__
    ```powershell
    # [IMPORTANT] Go inside the root directory of MFTParser

    # we create a virtual environment where we will install the necessary libraries. 
    python -m venv venv

    # Windows powershell
    venv\Scripts\activate

    # Install dependencies
    pip install -r requirements.txt

    ```
    - __Usage:__

    ```powershell
    # Launch app with default values
    python MFTParser.py

    # Show help
    python MFTParser.py -h

    # Use personalized values
    # -i MY_MFT.bin . [Input value] To use a file named MY_MFT.bin . By default uses MFT.bin
    # -filename . File name output. By default uses MFT_parser
    # -filetype . File type extensión [Only xlsx or csv]. By default uses xlsx
    python MFTParser.py -i MY_MFT.bin -filename my_parsed_mft -filetype csv
    ```

- __MFTReader__. This tool show the content of the attributes of a record stored in the MFT.