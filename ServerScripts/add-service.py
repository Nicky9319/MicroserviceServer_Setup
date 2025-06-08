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
            "2" : "MESSAGE_QUEUE",
            "3" : "WS_SERVER",
            "4" : "HTTP_QUEUE_MERGE",
            "5" : "HTTP_HTTP_QUEUE_MERGE",
            "6" : "WS_HTTP_HTTP_QUEUE_MERGE",
            "7" : "WS_HTTP_QUEUE_MERGE"
        }        

        self.templateNumber = None
        self.templateName = None

        self.serviceName = None

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

    def setupTemplate1(self):
        self.getServiceName()
        print(self.serviceName)
        pass

    def setupTemplate2(self):
        pass

    def setupTemplate3(self):
        pass

    def setupTemplate4(self):
        pass

    def setupTemplate5(self):
        pass

    def setupTemplate6(self):
        pass

    def setupTemplate7(self):
        pass

    def startTemplateSetup(self):
        if self.templateNumber == 1:
            self.setupTemplate1()
        elif self.templateNumber == 2:
            self.setupTemplate2()
        elif self.templateNumber == 3:
            self.setupTemplate3()
        elif self.templateNumber == 4:
            self.setupTemplate4()
        elif self.templateNumber == 5:
            self.setupTemplate5()
        elif self.templateNumber == 6:
            self.setupTemplate6()
        elif self.templateNumber == 7:
            self.setupTemplate7()
        else:
            print("Invalid Template Number. Please try again.")
# This script sets up the language and template for a service

langSetup = LanguageSetup()
langSetup.selectLanguage()

if langSetup.languageNumber == 1:
    pythonTemplateSetup = PythonTemplateSetup()
    pythonTemplateSetup.selectPythonTemplate()
    pythonTemplateSetup.startTemplateSetup()