import ipaddress
import os
import json

class LanguageSetup():
    def __init__(self):
        self.languageNumberMapping = {
            "0" : "Exit",
            "1" : "Python"
        }
        self.languageNumber = None
        self.languageName = None

    def selectLanguage(self):
        while True:
            print("Select the Language for the Service")

            print()
            for lang in self.languageNumberMapping.keys():
                print(f"{lang} : {self.languageNumberMapping[lang]}") 
            print()

            language = input("Enter the Language Number: ")

            if language == "0":
                exit(0)
            
            if not language.isnumeric():
                print("Invalid Input. Please enter a valid number.")
                print("\n\n--------------------------------------------------------------\n\n")
                continue
        
            if language not in self.languageNumberMapping.keys():
                print("Invalid Language Number. Please try again.")
                print("\n\n--------------------------------------------------------------\n\n")
                continue

            print("\n\n--------------------------------------------------------------\n\n")

            self.languageNumber = int(language)
            self.languageName = self.languageNumberMapping[language]
            
            return language

class PythonTemplateSetup():
    def __init__(self):
        self.pythonTemplateNumberMapping = {
            "0" : "Exit",
            "1" : "HTTP_SERVER",
            "2" : "WS_SERVER",
            "3" : "HTTP_QUEUE_MERGE",
            "4" : "WS_HTTP_QUEUE_MERGE"
        }        

        self.templateNumber = None
        self.templateName = None

        self.serviceName = None
        self.currDirectory = os.getcwd()

    def selectPythonTemplate(self):
        while True:
            print("Select the Python Template for the Service")

            print()
            for template in self.pythonTemplateNumberMapping.keys():
                print(f"{template} : {self.pythonTemplateNumberMapping[template]}") 
            print()

            template = input("Enter the Template Number: ")

            if template == "0":
                exit(0)
            
            if not template.isnumeric():
                print("Invalid Input. Please enter a valid number.")
                print("\n\n--------------------------------------------------------------\n\n")
                continue

            if template not in self.pythonTemplateNumberMapping.keys():
                print("Invalid Template Number. Please try again.")
                print("\n\n--------------------------------------------------------------\n\n")

                continue

            self.templateNumber = int(template)
            self.templateName = self.pythonTemplateNumberMapping[template]

            print("\n\n--------------------------------------------------------------\n\n")
            return template


    def getServiceName(self):
        while True:
            print("Enter the Name of the Service, and Remember the Service would be named as service_<ServiceName>Service")
            print("For Example, if you enter 'Main' then, the folder Name would be service_MainService and the py file inside it would be named main-service.py")

            print()
            serviceName = input("Enter the Service Name: ")
            serviceName = serviceName.strip()

            if " " in serviceName:
                print("Service Name should not contain spaces. Please enter a valid name without spaces.")
                print("\n\n--------------------------------------------------------------\n\n")
                continue
        
            if "-" in serviceName:
                print("Service Name should not contain dashes. Please enter a valid name without dashes.")
                print("\n\n--------------------------------------------------------------\n\n")
                continue

            if "/" in serviceName:
                print("Service Name should not contain slashes. Please enter a valid name without slashes.")
                print("\n\n--------------------------------------------------------------\n\n")
                continue

            if "," in serviceName:
                print("Service Name should not contain commas. Please enter a valid name without commas.")
                print("\n\n--------------------------------------------------------------\n\n")
                continue

            self.serviceName = serviceName

            print("\n\n--------------------------------------------------------------\n\n")
            return self.serviceName

    def getPortsAndHostForHttpServer(self):
        print("Enter the Host and Port for the HTTP Server")
        serverHost = None
        serverPort = None
        while True:
            print("Enter the Host for the HTTP Server (Default: localhost)")

            serverHost = input("Host: ")
            if serverHost == "":
                serverHost = "localhost"

            try:
                # Try to validate as an IP address
                ipaddress.ip_address(serverHost)
            except ValueError:
                if serverHost != "localhost":
                    print("Invalid host. Please enter a valid IP address or 'localhost'.")
                    print("\n\n--------------------------------------------------------------\n\n")
                    continue
            
            break
    
        while True:
            print("Enter the Port for the HTTP Server (Default: 8000)")

            serverPort = input("Port: ")
            if serverPort == "":
                serverPort = 8000
            
            if not serverPort.isnumeric():
                print("Invalid port. Please enter a valid number.")
                print("\n\n--------------------------------------------------------------\n\n")
                continue
            
            serverPort = int(serverPort)
            if serverPort < 1 or serverPort > 65535:
                print("Port number must be between 1 and 65535. Please try again.")
                print("\n\n--------------------------------------------------------------\n\n")
                continue
            
            break

        return serverHost, serverPort

    def getPortsAndHostForWsServer(self):
        print("Enter the Host and Port for the WebSocket Server")
        serverHost = None
        serverPort = None
        while True:
            print("Enter the Host for the WebSocket Server (Default: localhost)")

            serverHost = input("Host: ")
            if serverHost == "":
                serverHost = "localhost"

            try:
                # Try to validate as an IP address
                ipaddress.ip_address(serverHost)
            except ValueError:
                if serverHost != "localhost":
                    print("Invalid host. Please enter a valid IP address or 'localhost'.")
                    print("\n\n--------------------------------------------------------------\n\n")
                    continue
            
            break
    
        while True:
            print("Enter the Port for the WebSocket Server (Default: 6000)")

            serverPort = input("Port: ")
            if serverPort == "":
                serverPort = 6000
            
            if not serverPort.isnumeric():
                print("Invalid port. Please enter a valid number.")
                print("\n\n--------------------------------------------------------------\n\n")
                continue
            
            serverPort = int(serverPort)
            if serverPort < 1 or serverPort > 65535:
                print("Port number must be between 1 and 65535. Please try again.")
                print("\n\n--------------------------------------------------------------\n\n")
                continue
            
            break

        return serverHost, serverPort



    def addServiceInfoToServiceURLMapping(self, serverHost, serverPort, wsServerHost=None, wsServerPort=None):
        if(serverHost == "localhost"):
            serverHost = "127.0.0.1"

        # Go one directory back from current directory
        script_path = os.path.abspath(__file__)
        parent_dir = os.path.dirname(os.path.dirname(script_path))
        json_file_path = os.path.join(parent_dir, "ServiceURLMapping.json")

        print(json_file_path)

        # Read existing data if file exists, else start with empty list
        if os.path.exists(json_file_path):
            with open(json_file_path, "r") as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []


        # Append new data

        # existing_data.append(data)
        existing_data[f"{self.serviceName.upper()}_SERVICE"] = f"{serverHost}:{serverPort}"


        # Write back to the file
        with open(json_file_path, "w") as f:
            json.dump(existing_data, f, indent=4)

        print(f"Service information for {self.serviceName} added to ServiceURLMapping.json")




    def setupTemplate1(self):
        self.getServiceName()
        print(self.serviceName)
        serverHost, serverPort = self.getPortsAndHostForHttpServer()
        print(f"HTTP Server will run on {serverHost}:{serverPort}")
        return serverHost, serverPort

    def setupTemplate2(self):
        self.getServiceName()
        print(self.serviceName)
        wsServerHost, wsServerPort = self.getPortsAndHostForWsServer()
        print(f"WebSocket Server will run on {wsServerHost}:{wsServerPort}")

    def setupTemplate3(self):
        self.getServiceName()
        print(self.serviceName)
        serverHost, serverPort = self.getPortsAndHostForHttpServer()
        print(f"HTTP Server will run on {serverHost}:{serverPort}")
        return serverHost, serverPort

    def setupTemplate4(self):
        self.getServiceName()
        print(self.serviceName)

        serverHost, serverPort = self.getPortsAndHostForHttpServer()
        print(f"HTTP Server will run on {serverHost}:{serverPort}")

        wsServerHost, wsServerPort = self.getPortsAndHostForWsServer()
        print(f"WebSocket Server will run on {wsServerHost}:{wsServerPort}")

        return serverHost, serverPort, wsServerHost, wsServerPort


    def startTemplateSetup(self):
        if self.templateNumber == 1:
            serverHost, serverPort = self.setupTemplate1()
            self.addServiceInfoToServiceURLMapping(serverHost , serverPort)
        elif self.templateNumber == 2:
            self.setupTemplate2()
        elif self.templateNumber == 3:
            serverHost, serverPort = self.setupTemplate3()
            self.addServiceInfoToServiceURLMapping(serverHost , serverPort)
        elif self.templateNumber == 4:
            serverHost, serverPort, wsServerHost, wsServerPort =self.setupTemplate4()
        else:
            print("Invalid Template Number. Please try again.")
            print("\n\n--------------------------------------------------------------\n\n")
            return


langSetup = LanguageSetup()
langSetup.selectLanguage()

if langSetup.languageNumber == 1:
    pythonTemplateSetup = PythonTemplateSetup()
    pythonTemplateSetup.selectPythonTemplate()
    pythonTemplateSetup.startTemplateSetup()