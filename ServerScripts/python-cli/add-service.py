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
        self.enableCors = True  # Default: CORS enabled

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
            print("Enter the Host for the HTTP Server (Default: 127.0.0.1)")

            httpServerHost = input("Host: ")
            if httpServerHost == "":
                httpServerHost = "127.0.0.1"

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
        
        # Get grandparent directory (two levels up from current script)
        currentDir = os.path.dirname(os.path.abspath(__file__))
        parentDir = os.path.dirname(currentDir)
        grandparentDir = os.path.dirname(parentDir)
        
        # Create full path for service directory
        serviceDirPath = os.path.join(grandparentDir, serviceFolderName)
        
        # Create directory if it doesn't exist
        os.makedirs(serviceDirPath, exist_ok=True)
        
        return serviceDirPath

    def generateServiceFile(self, serviceDirPath):
        # Create service file name
        serviceFileName = f"{self.serviceName.lower()}-service.py"
        serviceFilePath = os.path.join(serviceDirPath, serviceFileName)
        
        # Read the HTTP service template from the correct location
        currentDir = os.path.dirname(os.path.abspath(__file__))
        parentDir = os.path.dirname(currentDir)
        templatePath = os.path.join(parentDir, "ServiceTemplates", "python", "HTTP_SERVICE.txt")
        
        with open(templatePath, 'r') as templateFile:
            templateContent = templateFile.read()
        
        # Replace placeholders with actual values
        modifiedContent = self.replacePlaceholders(templateContent)
        
        # Write the modified content to the new service file
        with open(serviceFilePath, 'w') as serviceFile:
            serviceFile.write(modifiedContent)
        
        return serviceFilePath

    def replacePlaceholders(self, templateContent):
        # Replace the host
        templateContent = self.replaceSection(
            templateContent,
            "#<HTTP_SERVER_HOST_START>",
            "#<HTTP_SERVER_HOST_END>",
            f'    httpServerHost = "{self.serviceHttpHost}"'
        )
        
        # Replace the port
        templateContent = self.replaceSection(
            templateContent,
            "#<HTTP_SERVER_PORT_START>",
            "#<HTTP_SERVER_PORT_END>",
            f'    httpServerPort = {self.serviceHttpPort}'
        )
        
        # Replace privileged IP addresses
        privilegedIpsStr = "[" + ", ".join([f'"{ip}"' for ip in self.servicePrivilegedIpAddresses]) + "]"
        templateContent = self.replaceSection(
            templateContent,
            "#<HTTP_SERVER_PRIVILEGED_IP_ADDRESS_START>",
            "#<HTTP_SERVER_PRIVILEGED_IP_ADDRESS_END>",
            f'    httpServerPrivilegedIpAddress = {privilegedIpsStr}'
        )

        # Replace CORS middleware section
        cors_line = 'self.app.add_middleware(CORSMiddleware, allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)'
        if self.enableCors:
            cors_code = f'        {cors_line}'
        else:
            cors_code = f'        #{cors_line}'
        templateContent = self.replaceSection(
            templateContent,
            "#<HTTP_SERVER_CORS_ADDITION_START>",
            "#<HTTP_SERVER_CORS_ADDITION_END>",
            cors_code
        )
        
        return templateContent

    def replaceSection(self, content, startMarker, endMarker, newContent):
        startIndex = content.find(startMarker)
        if startIndex == -1:
            return content
        
        endIndex = content.find(endMarker)
        if endIndex == -1:
            return content
        
        # Find the start of the start marker line to get proper indentation
        lineStart = content.rfind('\n', 0, startIndex) + 1
        indentation = content[lineStart:startIndex]
        
        # Find the end of the end marker line
        endLineEnd = content.find('\n', endIndex)
        if endLineEnd == -1:
            endLineEnd = len(content)
        else:
            endLineEnd += 1  # Include the newline
        
        # Replace the section with proper indentation for end marker
        before = content[:startIndex]
        after = content[endLineEnd:]
        
        return before + startMarker + '\n' + newContent + '\n' + indentation + endMarker + '\n' + after

    def updateServicesJson(self):
        # Get the path to services.json
        currentDir = os.path.dirname(os.path.abspath(__file__))
        parentDir = os.path.dirname(os.path.dirname(currentDir))  # Go up two levels to reach /home/paarth/Test
        servicesJsonPath = os.path.join(parentDir, "services.json")
        
        # Read existing services
        services = []
        if os.path.exists(servicesJsonPath):
            with open(servicesJsonPath, 'r') as file:
                services = json.load(file)
        
        # Create new service entry
        newService = {
            "ServiceLanguage": "Python",
            "ServiceName": self.serviceName,
            "ServiceFolderName": f"service_{self.serviceName}Service",
            "ServiceFileName": f"{self.serviceName.lower()}-service.py",
            "ServiceHttpHost": self.serviceHttpHost,
            "ServiceHttpPriviledgedIpAddress": self.servicePrivilegedIpAddresses,
            "ServiceHttpPort": self.serviceHttpPort,
            "ServiceType": "HTTP_SERVICE"
        }
        
        # Add new service to the list
        services.append(newService)
        
        # Write back to file
        with open(servicesJsonPath, 'w') as file:
            json.dump(services, file, indent=4)
        
        print(f"Updated services.json with new service: {self.serviceName}")

    def updateEnvFile(self):
        # Get the path to .env file
        currentDir = os.path.dirname(os.path.abspath(__file__))
        parentDir = os.path.dirname(os.path.dirname(currentDir))  # Go up two levels to reach /home/paarth/Test
        envFilePath = os.path.join(parentDir, ".env")
        
        # Read existing .env content
        envContent = ""
        if os.path.exists(envFilePath):
            with open(envFilePath, 'r') as file:
                envContent = file.read()
        
        # Prepare service entry
        serviceEntry = f'{self.serviceName.upper()}_SERVICE = "{self.serviceHttpHost}:{self.serviceHttpPort}"'
        commentedServiceEntry = f'# {self.serviceName.upper()}_SERVICE = "{self.serviceHttpHost}:{self.serviceHttpPort}"'
        
        # Add to development section
        devMarker = "#<ADD_DEVELOPMENT_SERVICES_ENVRIONMENT_VARIABLES>"
        if devMarker in envContent:
            envContent = envContent.replace(devMarker, f"{devMarker}\n{serviceEntry}")
        
        # Add to production section (commented)
        prodMarker = "#<ADD_PRODUCTION_SERVICES_ENVRIONMENT_VARIABLES>"
        if prodMarker in envContent:
            envContent = envContent.replace(prodMarker, f"{prodMarker}\n{commentedServiceEntry}")
        
        # Write back to file
        with open(envFilePath, 'w') as file:
            file.write(envContent)
        
        print(f"Updated .env file with new service environment variables")

    def askEnableCors(self):
        print("Enable CORS middleware for this service? (Y/n) [Default: Y]")
        while True:
            answer = input("Enable CORS? (Y/n): ").strip().lower()
            if answer == "" or answer == "y":
                return True
            if answer == "n":
                return False
            print("Invalid input. Please enter 'Y' or 'n'.")

    def startServiceSetup(self):
        self.serviceName = self.getServiceName()
        self.serviceHttpHost, self.serviceHttpPort = self.getHostandPortForHttpServer()
        self.servicePrivilegedIpAddresses = self.getPrivilegedIpAddresses()
        self.enableCors = self.askEnableCors()
        
        self.printServiceConfiguration()
        
        # Create service directory and file
        serviceDirPath = self.createServiceDirectory()
        serviceFilePath = self.generateServiceFile(serviceDirPath)
        
        # Update services.json and .env files
        self.updateServicesJson()
        self.updateEnvFile()
        
        print(f"\nService created successfully!")
        print(f"Service Directory: {serviceDirPath}")
        print(f"Service File: {serviceFilePath}")
        print(f"Updated configuration files: services.json and .env")

langSetup = LanguageSetup()
langSetup.selectLanguage()

if langSetup.languageNumber == 1:
    pythonTemplateSetup = PythonTemplateSetup()
    pythonTemplateSetup.startServiceSetup()