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
        self.serviceFolderName = None
        self.serviceFileName = None
        self.serviceHttpHost = None
        self.serviceHttpPort = None
        self.serviceWsHost = None
        self.serviceWsPort = None
        self.serviceMessageQueue = None
        self.serviceType = None

        self.currDirectory = os.path.dirname(os.path.abspath(__file__))
        self.parentDirectory = os.path.dirname(self.currDirectory)

        self.serviceInformation = {
            "ServiceLanguage" : "Python",
            "ServiceName" : None,
            "ServiceFolderName" : None,
            "ServiceFileName" : None,
            "ServiceHttpHost" : None,
            "ServiceHttpPort" : None,
            "ServiceWsHost" : None,
            "ServiceWsPort" : None,
            "ServiceMessageQueue" : None,
            "ServiceType" : None
        }


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

    def servicePopulateInformation(self):
        self.serviceInformation["ServiceName"] = self.serviceName
        self.serviceInformation["ServiceFolderName"] = self.serviceFolderName
        self.serviceInformation["ServiceFileName"] = self.serviceFileName
        self.serviceInformation["ServiceHttpHost"] = self.serviceHttpHost
        self.serviceInformation["ServiceHttpPort"] = self.serviceHttpPort
        self.serviceInformation["ServiceWsHost"] = self.serviceWsHost
        self.serviceInformation["ServiceWsPort"] = self.serviceWsPort
        self.serviceInformation["ServiceMessageQueue"] = self.serviceMessageQueue
        self.serviceInformation["ServiceType"] = self.serviceType

    def inferServiceType(self):
        httpServerIncluded = self.serviceHttpHost is not None
        wsServerIncluded = self.serviceWsHost is not None
        messageQueueIncluded = self.serviceMessageQueue

        if httpServerIncluded and wsServerIncluded and messageQueueIncluded:
            return "WS_HTTP_QUEUE_MERGE"
        
        if httpServerIncluded and wsServerIncluded:
            # return "WS_SERVER_MERGE"
            return "NONE"
    
        if httpServerIncluded and messageQueueIncluded:
            return "HTTP_QUEUE_MERGE"
        
        if wsServerIncluded and messageQueueIncluded:
            # return "WS_QUEUE_MERGE"
            return "NONE"
        
        if httpServerIncluded:
            return "HTTP_SERVER"
        
        if wsServerIncluded:
            return "WS_SERVER"
    
        return "NONE"

    def pushServiceToServer(self):
        if(self.serviceType == "NONE"):
            print("No Service Available for the Following Type")
            return
        
        self.addServiceInfoToServiceURLMapping(self.serviceHttpHost, self.serviceHttpPort)

        service_folder_path , self.serviceFolderName = self.addServiceFolder()
        service_file_path, self.serviceFileName = self.addServiceFile(service_folder_path)

        self.addServiceInfoToStartShellScript()
        self.addServiceInfoToRestartShellScript()

        self.addServiceInfoToServiceJsonFile()

        self.addServiceInfoToServiceFile(service_file_path)





    def getServiceName(self):
        print("Enter the Name of the Service, and Remember the Service would be named as service_<ServiceName>Service")
        print("For Example, if you enter 'Main' then, the folder Name would be service_MainService and the py file inside it would be named main-service.py")
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
        while True:
            needHttpServer = input("Do you want to add an HTTP Server? (yes/no) [Default = no]: ").strip().lower()
            if needHttpServer in ["yes", "y"]:
                print()
                break
            elif needHttpServer in ["no", "n",""]:
                print("Skipping HTTP Server setup.")
                print()
                return None, None
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
                continue
            
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

    def getHostandPortForWsServer(self):
        while True:
            needWsServer = input("Do you want to add an WS Server? (yes/no) [Default = no]: ").strip().lower()
            if needWsServer in ["yes", "y"]:
                print()
                break
            elif needWsServer in ["no", "n",""]:
                print("Skipping WS Server setup.")
                print()
                return None, None
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
                continue


        print("Enter the Host and Port for the WS Server")

        wsServerHost = None
        wsServerPort = None

        while True:
            print("Enter the Host for the WS Server (Default: localhost)")

            wsServerHost = input("Host: ")
            if wsServerHost == "":
                wsServerHost = "localhost"

            try:
                # Try to validate as an IP address
                ipaddress.ip_address(wsServerHost)
            except ValueError:
                if wsServerHost != "localhost":
                    print("Invalid host. Please enter a valid IP address or 'localhost'.")
                    continue
            
            print()
            break
    
        print("Enter the Port for the WS Server (Default: random)")
        while True:
            wsServerPort = input("Port: ")
            if wsServerPort == "":
                wsServerPort = random.randint(1024, 65535)
                break

            if not wsServerPort.isnumeric():
                print("Invalid port. Please enter a valid number.")
                print()
                continue
            
            wsServerPort = int(wsServerPort)
            if wsServerPort < 1024 or wsServerPort > 65535:
                print("Port number must be between 1024 and 65535. Please try again.")
                print()
                continue
            
            
            break

        print("\n\n--------------------------------------------------------------\n\n")
        return wsServerHost, wsServerPort

    def getMessageQueue(Self):
        while True:
            needMessageQueue = input("Do you want to add an Message Queue? (yes/no) [Default = no]: ").strip().lower()
            if needMessageQueue in ["yes", "y"]:
                print()
                break
            elif needMessageQueue in ["no", "n",""]:
                print("Skipping Message Queue setup.")
                return False
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
                continue
        
        return True
        
    def getServiceFolderName(self):
        # The folder name is service_<ServiceName>Service
        self.serviceFolderName = f"service_{self.serviceName}Service"
        return self.serviceFolderName

    def getServiceFileName(self):
        # The file name is <ServiceName>-service.py
        self.serviceFileName = f"{self.serviceName.lower()}-service.py"
        return self.serviceFileName

    


    def addServiceFile(self, folder_path):
        # Create a file named main-service.py in the service folder
        file_name = self.serviceFileName
        file_path = os.path.join(folder_path, file_name)
        try:
            with open(file_path, "w") as f:
                pass
            print(f"Created file: {file_path}")
        except Exception as e:
            print(f"Error creating file {file_path}: {e}")
        return file_path, file_name

    def addServiceFolder(self):
        # Create a folder named service_<ServiceName>Service in the parent directory
        folder_name = self.serviceFolderName
        folder_path = os.path.join(self.parentDirectory, folder_name)
        try:
            os.makedirs(folder_path, exist_ok=True)
            print(f"Created folder: {folder_path}")
        except Exception as e:
            print(f"Error creating folder {folder_path}: {e}")
        return folder_path , folder_name

    def addServiceInfoToServiceURLMapping(self, serverHost, serverPort):
        if(serverHost == "localhost"):
            serverHost = "127.0.0.1"

        # Go one Parent Directory Relative to the Current File
        json_file_path = os.path.join(self.parentDirectory, "ServiceURLMapping.json")

        print(json_file_path)

        # Read existing data if file exists, else start with empty list
        if os.path.exists(json_file_path):
            with open(json_file_path, "r") as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = {}
        else:
            existing_data = {}


        # Append new data

        # existing_data.append(data)
        existing_data[f"{self.serviceName.upper()}_SERVICE"] = f"{serverHost}:{serverPort}"


        # Write back to the file
        with open(json_file_path, "w") as f:
            json.dump(existing_data, f, indent=4)

        print(f"Service information for {self.serviceName} added to ServiceURLMapping.json")

    def addServiceInfoToStartShellScript(self):
        start_sh_path = os.path.join(self.currDirectory, "start-server.sh")
        try:
            with open(start_sh_path, "r") as f:
                content = f.read()
            new_content = content.replace(
                "#<ADD_SERVICE_START_HERE>",
                f".venv/bin/python3.12 {self.serviceFolderName}/{self.serviceFileName} & \n#<ADD_SERVICE_START_HERE>"
            )
            with open(start_sh_path, "w") as f:
                f.write(new_content)
            print(f"Updated {start_sh_path} with new service start command.")
        except Exception as e:
            print(f"Error updating {start_sh_path}: {e}")
        pass

    def addServiceInfoToRestartShellScript(self):
        restart_sh_path = os.path.join(self.currDirectory, "restart-server.sh")
        try:
            with open(restart_sh_path, "r") as f:
                content = f.read()
            new_content = content.replace(
                "#<ADD_SERVICE_START_HERE>",
                f".venv/bin/python3.12 {self.serviceFolderName}/{self.serviceFileName} & \n#<ADD_SERVICE_START_HERE>"
            )
            with open(restart_sh_path, "w") as f:
                f.write(new_content)
            print(f"Updated {restart_sh_path} with new service start command.")
        except Exception as e:
            print(f"Error updating {restart_sh_path}: {e}")
        pass

    def addServiceInfoToServiceJsonFile(self):
        json_file_path = os.path.join(self.parentDirectory, "services.json")
        print(json_file_path)

        if os.path.exists(json_file_path):
            with open(json_file_path, "r") as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []
        
        existing_data.append(self.serviceInformation)

        with open(json_file_path, "w") as f:
            json.dump(existing_data, f, indent=4)

        print(f"Service Information Stored in the services.json File !!!")

    def addServiceInfoToServiceFile(self, file_path):
        templateType = self.serviceType
        templatePath = os.path.join(self.currDirectory, "ServiceTemplates", "python", f"{templateType}.txt")
        
        try:
            with open(templatePath, "r") as template_file:
                template_content = template_file.read()

            print(template_content)
            
            # Replace placeholders in the template with actual values
            service_content = template_content.replace("{HTTP_SERVER_HOST}", f"'{self.serviceHttpHost}'")
            service_content = service_content.replace("{HTTP_SERVER_PORT}", f"{self.serviceHttpPort}")
            service_content = service_content.replace("{WS_SERVER_HOST}", f"'{self.serviceWsHost}'")
            service_content = service_content.replace("{WS_SERVER_PORT}", f"{self.serviceWsPort}")
            
            with open(file_path, "w") as service_file:
                service_file.write(service_content)
            
            print(f"Service file created at {file_path}")
        except FileNotFoundError:
            print(f"Template file {templatePath} not found. Please ensure the template exists.")

    


    def startServiceSetup(self):
        self.serviceName = self.getServiceName()
        self.serviceFolderName = self.getServiceFolderName()
        self.serviceFileName = self.getServiceFileName()

        self.serviceHttpHost, self.serviceHttpPort = self.getHostandPortForHttpServer()
        self.serviceWsHost, self.serviceWsPort = self.getHostandPortForWsServer()

        self.serviceMessageQueue = self.getMessageQueue()

        self.serviceType = self.inferServiceType()

        print(self.serviceName)
        print(self.serviceFolderName)
        print(self.serviceFileName)
        print(self.serviceHttpHost, self.serviceHttpPort)
        print(self.serviceWsHost, self.serviceWsPort)
        print(self.serviceMessageQueue)
        print(self.serviceType)
        
        self.servicePopulateInformation()

        self.pushServiceToServer()




langSetup = LanguageSetup()
langSetup.selectLanguage()

if langSetup.languageNumber == 1:
    pythonTemplateSetup = PythonTemplateSetup()
    pythonTemplateSetup.startServiceSetup()