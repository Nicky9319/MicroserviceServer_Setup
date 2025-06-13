import ipaddress
import os
import json
import random

class LanguageSetup():
    def __init__(self):
        self.languageNumberMapping = {
            "0" : "Exit",
            "1" : "Python"
        }
        self.languageNumber = None
        self.languageName = None

    def selectLanguage(self):
        print("Select the Language for the Service")
        print()
        for lang in self.languageNumberMapping.keys():
            print(f"{lang} : {self.languageNumberMapping[lang]}") 

        while True:
            print()
            language = input("Enter the Language Number: ")

            if language == "0":
                exit(0)
            
            if not language.isnumeric():
                print("Invalid Input. Please enter a valid number.")
                continue
        
            if language not in self.languageNumberMapping.keys():
                print("Invalid Language Number. Please try again.")
                continue

            print("\n\n--------------------------------------------------------------\n\n")

            self.languageNumber = int(language)
            self.languageName = self.languageNumberMapping[language]
            
            return language

class PythonTemplateSetup():
    def __init__(self):
        self.serviceName = None
        self.serviceHttpHost = None
        self.serviceHttpPort = None
        self.servicePrivilegedIpAddresses = []

    def getServiceName(self):
        print("Enter the Name of the Service")
        while True:
            print()
            serviceName = input("Enter the Service Name: ")
            serviceName = serviceName.strip()

            if " " in serviceName:
                print("Service Name should not contain spaces. Please enter a valid name without spaces.")
                continue
        
            if "-" in serviceName:
                print("Service Name should not contain dashes. Please enter a valid name without dashes.")
                continue

            if "/" in serviceName:
                print("Service Name should not contain slashes. Please enter a valid name without slashes.")
                continue

            if "," in serviceName:
                print("Service Name should not contain commas. Please enter a valid name without commas.")
                continue

            if serviceName == "":
                print("Service Name cannot be empty. Please enter a valid name.")
                continue

            print("\n\n--------------------------------------------------------------\n\n")
            return serviceName

    def getHostandPortForHttpServer(self):
        print("Enter the Host and Port for the HTTP Server")

        httpServerHost = None
        httpServerPort = None

        while True:
            print("Enter the Host for the HTTP Server (Default: localhost)")

            httpServerHost = input("Host: ")
            if httpServerHost == "":
                httpServerHost = "localhost"

            try:
                # Try to validate as an IP address
                ipaddress.ip_address(httpServerHost)
            except ValueError:
                if httpServerHost != "localhost":
                    print("Invalid host. Please enter a valid IP address or 'localhost'.")
                    continue
            
            print()
            break
    
        print("Enter the Port for the HTTP Server (Default: random)")
        while True:
            httpServerPort = input("Port: ")
            if httpServerPort == "":
                httpServerPort = random.randint(1024, 65535)
                break

            if not httpServerPort.isnumeric():
                print("Invalid port. Please enter a valid number.")
                print()
                continue
            
            httpServerPort = int(httpServerPort)
            if httpServerPort < 1024 or httpServerPort > 65535:
                print("Port number must be between 1024 and 65535. Please try again.")
                print()
                continue
            
            break

        print("\n\n--------------------------------------------------------------\n\n")
        return httpServerHost, httpServerPort

    def getPrivilegedIpAddresses(self):
        print("Enter Privileged IP Addresses (one per line, press Enter on empty line to finish)")
        print("Default: 127.0.0.1 will be added automatically")
        
        privilegedIps = ["127.0.0.1"]  # Default privileged IP
        
        while True:
            ipInput = input("Enter IP Address (or press Enter to finish): ").strip()
            
            if ipInput == "":
                break
                
            try:
                # Validate IP address
                ipaddress.ip_address(ipInput)
                if ipInput not in privilegedIps:
                    privilegedIps.append(ipInput)
                    print(f"Added: {ipInput}")
                else:
                    print(f"IP {ipInput} already in list")
            except ValueError:
                print("Invalid IP address. Please enter a valid IP address.")
                continue
        
        print("\n\n--------------------------------------------------------------\n\n")
        return privilegedIps

    def printServiceConfiguration(self):
        print("=== SERVICE CONFIGURATION ===")
        print(f"Service Name: {self.serviceName}")
        print(f"HTTP Host: {self.serviceHttpHost}")
        print(f"HTTP Port: {self.serviceHttpPort}")
        print(f"Privileged IP Addresses: {self.servicePrivilegedIpAddresses}")
        print("=============================")

    def createServiceDirectory(self):
        # Create service folder name
        serviceFolderName = f"service_{self.serviceName}Service"
        
        # Get parent directory (one level up from current script)
        currentDir = os.path.dirname(os.path.abspath(__file__))
        parentDir = os.path.dirname(currentDir)
        grandParentDir = os.path.dirname(parentDir)
        
        # Create full path for service directory
        serviceDirPath = os.path.join(grandParentDir, serviceFolderName)
        
        # Create directory if it doesn't exist
        os.makedirs(serviceDirPath, exist_ok=True)
        
        return serviceDirPath

    def generateServiceFile(self, serviceDirPath):
        # Create service file name
        serviceFileName = f"{self.serviceName.lower()}-service.py"
        serviceFilePath = os.path.join(serviceDirPath, serviceFileName)
        
        # Read the HTTP service template
        templatePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../ServiceTemplates/python/HTTP_SERVICE.txt")
        
        with open(templatePath, 'r') as templateFile:
            templateContent = templateFile.read()
        
        # Replace placeholders with actual values
        modifiedContent = self.replacePlaceholders(templateContent)
        
        # Write the modified content to the new service file
        with open(serviceFilePath, 'w') as serviceFile:
            serviceFile.write(modifiedContent)
        
        return serviceFilePath

    def replacePlaceholders(self, templateContent):
        # Replace port section
        templateContent = self.replaceSection(
            templateContent,
            "#<HTTP_SERVER_PORT_START>",
            "#<HTTP_SERVER_PORT_END>",
            f"    httpServerPort = {self.serviceHttpPort}"
        )
        
        # Replace host section
        templateContent = self.replaceSection(
            templateContent,
            "#<HTTP_SERVER_HOST_START>",
            "#<HTTP_SERVER_HOST_END>",
            f'    httpServerHost = "{self.serviceHttpHost}"'
        )
        
        # Replace privileged IP addresses section
        privilegedIpsStr = "{" + ", ".join([f'"{ip}"' for ip in self.servicePrivilegedIpAddresses]) + "}"
        templateContent = self.replaceSection(
            templateContent,
            "#<HTTP_SERVER_PRIVILEGED_IP_ADDRESS_START>",
            "#<HTTP_SERVER_PRIVILEGED_IP_ADDRESS_END>",
            f"    httpServerPrivilegedIpAddress = {privilegedIpsStr}"
        )
        
        return templateContent

    def replaceSection(self, content, startMarker, endMarker, newContent):
        startIndex = content.find(startMarker)
        if startIndex == -1:
            return content
        
        endIndex = content.find(endMarker)
        if endIndex == -1:
            return content
        
        # Find the start of the line containing the start marker to get indentation
        startLineBegin = content.rfind('\n', 0, startIndex) + 1
        startIndentation = content[startLineBegin:startIndex]
        
        # Find the start of the line containing the end marker to get its indentation
        endLineBegin = content.rfind('\n', 0, endIndex) + 1
        endIndentation = content[endLineBegin:endIndex]
        
        # Find the end of the end marker line
        endLineEnd = content.find('\n', endIndex)
        if endLineEnd == -1:
            endLineEnd = len(content)
        else:
            endLineEnd += 1  # Include the newline
        
        # Replace the section while preserving indentation
        before = content[:startIndex]
        after = content[endLineEnd:]
        
        return before + startMarker + '\n' + newContent + '\n' + endIndentation + endMarker + '\n' + after

    def startServiceSetup(self):
        self.serviceName = self.getServiceName()
        self.serviceHttpHost, self.serviceHttpPort = self.getHostandPortForHttpServer()
        self.servicePrivilegedIpAddresses = self.getPrivilegedIpAddresses()
        
        self.printServiceConfiguration()
        
        # Create service directory and file
        serviceDirPath = self.createServiceDirectory()
        serviceFilePath = self.generateServiceFile(serviceDirPath)
        
        print(f"\nService created successfully!")
        print(f"Service Directory: {serviceDirPath}")
        print(f"Service File: {serviceFilePath}")

langSetup = LanguageSetup()
langSetup.selectLanguage()

if langSetup.languageNumber == 1:
    pythonTemplateSetup = PythonTemplateSetup()
    pythonTemplateSetup.startServiceSetup()