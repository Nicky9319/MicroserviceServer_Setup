const fs = require('fs');
const path = require('path');
const readline = require('readline');

class LanguageSetup {
    constructor() {
        this.languageNumberMapping = {
            "0": "Exit",
            "1": "JavaScript"
        };
        this.languageNumber = null;
        this.languageName = null;
    }

    async selectLanguage() {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        console.log("Select the Language for the Service");
        console.log();
        
        Object.keys(this.languageNumberMapping).forEach(lang => {
            console.log(`${lang} : ${this.languageNumberMapping[lang]}`);
        });

        while (true) {
            console.log();
            const language = await this.question(rl, "Enter the Language Number: ");

            if (language === "0") {
                rl.close();
                process.exit(0);
            }

            if (!/^\d+$/.test(language)) {
                console.log("Invalid Input. Please enter a valid number.");
                continue;
            }

            if (!this.languageNumberMapping.hasOwnProperty(language)) {
                console.log("Invalid Language Number. Please try again.");
                continue;
            }

            console.log("\n\n--------------------------------------------------------------\n\n");

            this.languageNumber = parseInt(language);
            this.languageName = this.languageNumberMapping[language];
            
            rl.close();
            return language;
        }
    }

    question(rl, prompt) {
        return new Promise((resolve) => {
            rl.question(prompt, resolve);
        });
    }
}

class JavaScriptTemplateSetup {
    constructor() {
        this.serviceName = null;
        this.serviceHttpHost = null;
        this.serviceHttpPort = null;
        this.servicePrivilegedIpAddresses = [];
        this.enableCors = true; // Default: CORS enabled
    }

    async getServiceName() {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        console.log("Enter the Name of the Service");
        
        while (true) {
            console.log();
            const serviceName = (await this.question(rl, "Enter the Service Name: ")).trim();

            if (serviceName.includes(" ")) {
                console.log("Service Name should not contain spaces. Please enter a valid name without spaces.");
                continue;
            }

            if (serviceName.includes("-")) {
                console.log("Service Name should not contain dashes. Please enter a valid name without dashes.");
                continue;
            }

            if (serviceName.includes("/")) {
                console.log("Service Name should not contain slashes. Please enter a valid name without slashes.");
                continue;
            }

            if (serviceName.includes(",")) {
                console.log("Service Name should not contain commas. Please enter a valid name without commas.");
                continue;
            }

            if (serviceName === "") {
                console.log("Service Name cannot be empty. Please enter a valid name.");
                continue;
            }

            console.log("\n\n--------------------------------------------------------------\n\n");
            rl.close();
            return serviceName;
        }
    }

    async getHostAndPortForHttpServer() {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        console.log("Enter the Host and Port for the HTTP Server");

        let httpServerHost = null;
        let httpServerPort = null;

        while (true) {
            console.log("Enter the Host for the HTTP Server (Default: 127.0.0.1)");
            
            httpServerHost = await this.question(rl, "Host: ");
            if (httpServerHost === "") {
                httpServerHost = "127.0.0.1";
            }

            if (!this.isValidHost(httpServerHost)) {
                console.log("Invalid host. Please enter a valid IP address or 'localhost'.");
                continue;
            }

            console.log();
            break;
        }

        console.log("Enter the Port for the HTTP Server (Default: random)");
        while (true) {
            httpServerPort = await this.question(rl, "Port: ");
            if (httpServerPort === "") {
                httpServerPort = Math.floor(Math.random() * (65535 - 1024 + 1)) + 1024;
                break;
            }

            if (!/^\d+$/.test(httpServerPort)) {
                console.log("Invalid port. Please enter a valid number.");
                console.log();
                continue;
            }

            httpServerPort = parseInt(httpServerPort);
            if (httpServerPort < 1024 || httpServerPort > 65535) {
                console.log("Port number must be between 1024 and 65535. Please try again.");
                console.log();
                continue;
            }

            break;
        }

        console.log("\n\n--------------------------------------------------------------\n\n");
        rl.close();
        return [httpServerHost, httpServerPort];
    }

    async getPrivilegedIpAddresses() {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        console.log("Enter Privileged IP Addresses (one per line, press Enter on empty line to finish)");
        console.log("Default: 127.0.0.1 will be added automatically");

        const privilegedIps = ["127.0.0.1"]; // Default privileged IP

        while (true) {
            const ipInput = (await this.question(rl, "Enter IP Address (or press Enter to finish): ")).trim();

            if (ipInput === "") {
                break;
            }

            if (this.isValidIpAddress(ipInput)) {
                if (!privilegedIps.includes(ipInput)) {
                    privilegedIps.push(ipInput);
                    console.log(`Added: ${ipInput}`);
                } else {
                    console.log(`IP ${ipInput} already in list`);
                }
            } else {
                console.log("Invalid IP address. Please enter a valid IP address.");
                continue;
            }
        }

        console.log("\n\n--------------------------------------------------------------\n\n");
        rl.close();
        return privilegedIps;
    }

    printServiceConfiguration() {
        console.log("=== SERVICE CONFIGURATION ===");
        console.log(`Service Name: ${this.serviceName}`);
        console.log(`HTTP Host: ${this.serviceHttpHost}`);
        console.log(`HTTP Port: ${this.serviceHttpPort}`);
        console.log(`Privileged IP Addresses: ${JSON.stringify(this.servicePrivilegedIpAddresses)}`);
        console.log(`CORS Enabled: ${this.enableCors}`);
        console.log("=============================");
    }

    createServiceDirectory() {
        // Create service folder name
        const serviceFolderName = `service_${this.serviceName}Service`;
        
        // Get grandparent directory (two levels up from current script)
        const currentDir = __dirname;
        const parentDir = path.dirname(currentDir);
        const grandparentDir = path.dirname(parentDir);
        
        // Create full path for service directory
        const serviceDirPath = path.join(grandparentDir, serviceFolderName);
        
        // Create directory if it doesn't exist
        if (!fs.existsSync(serviceDirPath)) {
            fs.mkdirSync(serviceDirPath, { recursive: true });
        }

        // Create modular subdirectories
        const subDirs = ['DATA', 'HTTP_SERVER', 'SERVICE'];
        subDirs.forEach(dir => {
            const subDirPath = path.join(serviceDirPath, dir);
            if (!fs.existsSync(subDirPath)) {
                fs.mkdirSync(subDirPath, { recursive: true });
            }
        });
        
        return serviceDirPath;
    }

    generateServiceFile(serviceDirPath) {
        // Create service file name
        const serviceFileName = `${this.serviceName.toLowerCase()}-service.js`;
        const serviceFilePath = path.join(serviceDirPath, serviceFileName);
        
        // Read the HTTP service template from the correct location
        const currentDir = __dirname;
        const parentDir = path.dirname(currentDir);
        const templatePath = path.join(parentDir, "ServiceTemplates", "javascript", "HTTP_SERVICE.txt");
        
        const templateContent = fs.readFileSync(templatePath, 'utf8');
        
        // Replace placeholders with actual values
        const modifiedContent = this.replacePlaceholders(templateContent);
        
        // Write the modified content to the new service file
        fs.writeFileSync(serviceFilePath, modifiedContent);
        
        return serviceFilePath;
    }

    generateModularFiles(serviceDirPath) {
        const currentDir = __dirname;
        const parentDir = path.dirname(currentDir);
        const templatesDir = path.join(parentDir, "ServiceTemplates", "javascript");

        // Generate HTTP_SERVER files
        this.generateHttpServerFiles(serviceDirPath, templatesDir);
        
        // Generate DATA files
        this.generateDataFiles(serviceDirPath, templatesDir);
        
        // Generate SERVICE files
        this.generateServiceFiles(serviceDirPath, templatesDir);

        // Generate main functions.js
        this.generateMainFunctions(serviceDirPath, templatesDir);
    }

    generateHttpServerFiles(serviceDirPath, templatesDir) {
        const httpServerDir = path.join(serviceDirPath, 'HTTP_SERVER');
        
        // Generate http-server-class.js
        const httpServerClassTemplate = fs.readFileSync(path.join(templatesDir, 'http-server-class.txt'), 'utf8');
        const httpServerClassContent = this.replaceHttpServerPlaceholders(httpServerClassTemplate);
        fs.writeFileSync(path.join(httpServerDir, 'http-server-class.js'), httpServerClassContent);

        // Generate functions.js
        const httpServerFunctionsTemplate = fs.readFileSync(path.join(templatesDir, 'http-server-functions.txt'), 'utf8');
        const httpServerFunctionsContent = httpServerFunctionsTemplate.replace(
            /{SERVICE_NAME_LOWER_PLACEHOLDER}/g, 
            this.serviceName.toLowerCase()
        );
        fs.writeFileSync(path.join(httpServerDir, 'functions.js'), httpServerFunctionsContent);
    }

    generateDataFiles(serviceDirPath, templatesDir) {
        const dataDir = path.join(serviceDirPath, 'DATA');
        
        // Generate data-class.js
        const dataClassTemplate = fs.readFileSync(path.join(templatesDir, 'data-class.txt'), 'utf8');
        fs.writeFileSync(path.join(dataDir, 'data-class.js'), dataClassTemplate);

        // Generate functions.js
        const dataFunctionsTemplate = fs.readFileSync(path.join(templatesDir, 'data-functions.txt'), 'utf8');
        fs.writeFileSync(path.join(dataDir, 'functions.js'), dataFunctionsTemplate);
    }

    generateServiceFiles(serviceDirPath, templatesDir) {
        const serviceDir = path.join(serviceDirPath, 'SERVICE');
        
        // Generate service-class.js
        const serviceClassTemplate = fs.readFileSync(path.join(templatesDir, 'service-class.txt'), 'utf8');
        fs.writeFileSync(path.join(serviceDir, 'service-class.js'), serviceClassTemplate);
    }

    generateMainFunctions(serviceDirPath, templatesDir) {
        // Generate main functions.js
        const serviceFileName = `${this.serviceName.toLowerCase()}-service.js`;
        const functionsTemplate = fs.readFileSync(path.join(templatesDir, 'functions.txt'), 'utf8');
        const functionsContent = functionsTemplate
            .replace(/{SERVICE_NAME_PLACEHOLDER}/g, this.serviceName)
            .replace(/{SERVICE_FILE_NAME_PLACEHOLDER}/g, serviceFileName);
        fs.writeFileSync(path.join(serviceDirPath, 'functions.js'), functionsContent);
    }

    replacePlaceholders(templateContent) {
        // Replace the host
        templateContent = this.replaceSection(
            templateContent,
            "//<HTTP_SERVER_HOST_START>",
            "//<HTTP_SERVER_HOST_END>",
            `    const httpServerHost = "${this.serviceHttpHost}";`
        );
        
        // Replace the port
        templateContent = this.replaceSection(
            templateContent,
            "//<HTTP_SERVER_PORT_START>",
            "//<HTTP_SERVER_PORT_END>",
            `    const httpServerPort = ${this.serviceHttpPort};`
        );
        
        // Replace privileged IP addresses
        const privilegedIpsStr = "[" + this.servicePrivilegedIpAddresses.map(ip => `"${ip}"`).join(", ") + "]";
        templateContent = this.replaceSection(
            templateContent,
            "//<HTTP_SERVER_PRIVILEGED_IP_ADDRESS_START>",
            "//<HTTP_SERVER_PRIVILEGED_IP_ADDRESS_END>",
            `    const httpServerPrivilegedIpAddress = ${privilegedIpsStr};`
        );

        // Replace CORS setting
        templateContent = this.replaceSection(
            templateContent,
            "//<HTTP_SERVER_CORS_ENABLED_START>",
            "//<HTTP_SERVER_CORS_ENABLED_END>",
            `    const enableCors = ${this.enableCors};`
        );
        
        return templateContent;
    }

    replaceHttpServerPlaceholders(templateContent) {
        // Replace CORS middleware section
        const corsCode = `    // Conditionally add CORS middleware
    if (enableCors) {
      this.app.use(cors({
        origin: '*',
        credentials: true,
        methods: '*',
        allowedHeaders: '*'
      }));
      this.corsEnabled = true;
    }`;
        
        const corsReplacement = this.enableCors ? corsCode : `    // CORS is disabled\n    // ${corsCode.replace(/\n    /g, '\n    // ')}`;
        
        templateContent = this.replaceSection(
            templateContent,
            "//<HTTP_SERVER_CORS_ADDITION_START>",
            "//<HTTP_SERVER_CORS_ADDITION_END>",
            corsReplacement
        );
        
        return templateContent;
    }

    replaceSection(content, startMarker, endMarker, newContent) {
        const startIndex = content.indexOf(startMarker);
        if (startIndex === -1) {
            return content;
        }
        
        const endIndex = content.indexOf(endMarker);
        if (endIndex === -1) {
            return content;
        }
        
        // Find the start of the start marker line to get proper indentation
        const lineStart = content.lastIndexOf('\n', startIndex) + 1;
        const indentation = content.substring(lineStart, startIndex);
        
        // Find the end of the end marker line
        let endLineEnd = content.indexOf('\n', endIndex);
        if (endLineEnd === -1) {
            endLineEnd = content.length;
        } else {
            endLineEnd += 1; // Include the newline
        }
        
        // Replace the section with proper indentation for end marker
        const before = content.substring(0, startIndex);
        const after = content.substring(endLineEnd);
        
        return before + startMarker + '\n' + newContent + '\n' + indentation + endMarker + '\n' + after;
    }

    updateServicesJson() {
        // Get the path to services.json
        const currentDir = __dirname;
        const parentDir = path.dirname(path.dirname(currentDir)); // Go up two levels
        const servicesJsonPath = path.join(parentDir, "services.json");
        
        // Read existing services
        let services = [];
        if (fs.existsSync(servicesJsonPath)) {
            const fileContent = fs.readFileSync(servicesJsonPath, 'utf8');
            services = JSON.parse(fileContent);
        }
        
        // Create new service entry
        const newService = {
            "ServiceLanguage": "JavaScript",
            "ServiceName": this.serviceName,
            "ServiceFolderName": `service_${this.serviceName}Service`,
            "ServiceFileName": `${this.serviceName.toLowerCase()}-service.js`,
            "ServiceHttpHost": this.serviceHttpHost,
            "ServiceHttpPriviledgedIpAddress": this.servicePrivilegedIpAddresses,
            "ServiceHttpPort": this.serviceHttpPort,
            "ServiceType": "HTTP_SERVICE"
        };
        
        // Add new service to the list
        services.push(newService);
        
        // Write back to file
        fs.writeFileSync(servicesJsonPath, JSON.stringify(services, null, 4));
        
        console.log(`Updated services.json with new service: ${this.serviceName}`);
    }

    updateEnvFile() {
        // Get the path to .env file
        const currentDir = __dirname;
        const parentDir = path.dirname(path.dirname(currentDir)); // Go up two levels
        const envFilePath = path.join(parentDir, ".env");
        
        // Read existing .env content
        let envContent = "";
        if (fs.existsSync(envFilePath)) {
            envContent = fs.readFileSync(envFilePath, 'utf8');
        }
        
        // Prepare service entry
        const serviceEntry = `${this.serviceName.toUpperCase()}_SERVICE = "${this.serviceHttpHost}:${this.serviceHttpPort}"`;
        const commentedServiceEntry = `# ${this.serviceName.toUpperCase()}_SERVICE = "${this.serviceHttpHost}:${this.serviceHttpPort}"`;
        
        // Add to development section
        const devMarker = "#<ADD_DEVELOPMENT_SERVICES_ENVRIONMENT_VARIABLES>";
        if (envContent.includes(devMarker)) {
            envContent = envContent.replace(devMarker, `${devMarker}\n${serviceEntry}`);
        }
        
        // Add to production section (commented)
        const prodMarker = "#<ADD_PRODUCTION_SERVICES_ENVRIONMENT_VARIABLES>";
        if (envContent.includes(prodMarker)) {
            envContent = envContent.replace(prodMarker, `${prodMarker}\n${commentedServiceEntry}`);
        }
        
        // Write back to file
        fs.writeFileSync(envFilePath, envContent);
        
        console.log("Updated .env file with new service environment variables");
    }

    async askEnableCors() {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        console.log("Enable CORS middleware for this service? (Y/n) [Default: Y]");
        
        while (true) {
            const answer = (await this.question(rl, "Enable CORS? (Y/n): ")).trim().toLowerCase();
            
            if (answer === "" || answer === "y") {
                rl.close();
                return true;
            }
            if (answer === "n") {
                rl.close();
                return false;
            }
            console.log("Invalid input. Please enter 'Y' or 'n'.");
        }
    }

    async startServiceSetup() {
        this.serviceName = await this.getServiceName();
        [this.serviceHttpHost, this.serviceHttpPort] = await this.getHostAndPortForHttpServer();
        this.servicePrivilegedIpAddresses = await this.getPrivilegedIpAddresses();
        this.enableCors = await this.askEnableCors();
        
        this.printServiceConfiguration();
        
        // Create service directory and files
        const serviceDirPath = this.createServiceDirectory();
        const serviceFilePath = this.generateServiceFile(serviceDirPath);
        this.generateModularFiles(serviceDirPath);
        
        // Update services.json and .env files
        this.updateServicesJson();
        this.updateEnvFile();
        
        console.log("\nService created successfully!");
        console.log(`Service Directory: ${serviceDirPath}`);
        console.log(`Service File: ${serviceFilePath}`);
        console.log("Modular structure created:");
        console.log(`  - DATA/data-class.js & DATA/functions.js`);
        console.log(`  - HTTP_SERVER/http-server-class.js & HTTP_SERVER/functions.js`);
        console.log(`  - SERVICE/service-class.js`);
        console.log(`  - functions.js (main service functions)`);
        console.log("Updated configuration files: services.json and .env");
    }

    question(rl, prompt) {
        return new Promise((resolve) => {
            rl.question(prompt, resolve);
        });
    }

    isValidHost(host) {
        if (host === "localhost") return true;
        
        // Simple IP address validation
        const ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
        return ipRegex.test(host);
    }

    isValidIpAddress(ip) {
        const ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
        return ipRegex.test(ip);
    }
}

async function main() {
    const langSetup = new LanguageSetup();
    await langSetup.selectLanguage();

    if (langSetup.languageNumber === 1) {
        const jsTemplateSetup = new JavaScriptTemplateSetup();
        await jsTemplateSetup.startServiceSetup();
    }
}

// Run the main function if this script is executed directly
if (require.main === module) {
    main().catch(console.error);
}

module.exports = { LanguageSetup, JavaScriptTemplateSetup };
