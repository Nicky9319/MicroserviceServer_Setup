const fs = require('fs');
const path = require('path');
const readline = require('readline');
const os = require('os');

function askQuestion(query) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    return new Promise(resolve => rl.question(query, ans => {
        rl.close();
        resolve(ans);
    }));
}

async function getServiceName() {
    console.log("Enter the Name of the Service");
    while (true) {
        console.log();
        let serviceName = (await askQuestion("Enter the Service Name: ")).trim();
        if (!serviceName) {
            console.log("Service Name cannot be empty. Please enter a valid name.");
            continue;
        }
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
        console.log("\n\n--------------------------------------------------------------\n\n");
        return serviceName;
    }
}

function isValidIpAddress(ip) {
    const ipv4Regex = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    const ipv6Regex = /^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$/;
    
    return ipv4Regex.test(ip) || ipv6Regex.test(ip);
}

async function getHostAndPort() {
    console.log("Enter the Host and Port for the HTTP Server");
    
    let host;
    while (true) {
        console.log("Enter the Host for the HTTP Server (Default: 127.0.0.1)");
        host = await askQuestion("Host: ");
        if (!host) {
            host = "127.0.0.1";
            break;
        }
        if (isValidIpAddress(host) || host === "localhost") {
            break;
        }
        console.log("Invalid host. Please enter a valid IP address or 'localhost'.");
        console.log();
    }
    
    console.log();
    console.log("Enter the Port for the HTTP Server (Default: random)");
    let port;
    while (true) {
        let portStr = await askQuestion("Port: ");
        if (!portStr) {
            port = Math.floor(Math.random() * (65535 - 1024 + 1)) + 1024;
            break;
        }
        
        if (!/^\d+$/.test(portStr)) {
            console.log("Invalid port. Please enter a valid number.");
            console.log();
            continue;
        }
        
        port = parseInt(portStr);
        if (port < 1024 || port > 65535) {
            console.log("Port number must be between 1024 and 65535. Please try again.");
            console.log();
            continue;
        }
        
        break;
    }
    
    console.log("\n\n--------------------------------------------------------------\n\n");
    return { host, port };
}

async function getPrivilegedIps() {
    console.log("Enter Privileged IP Addresses (one per line, press Enter on empty line to finish)");
    console.log("Default: 127.0.0.1 will be added automatically");
    let ips = ["127.0.0.1"];
    while (true) {
        let ip = (await askQuestion("Enter IP Address (or press Enter to finish): ")).trim();
        if (!ip) break;
        
        if (!isValidIpAddress(ip)) {
            console.log("Invalid IP address. Please enter a valid IPv4 or IPv6 address.");
            continue;
        }
        
        if (!ips.includes(ip)) {
            ips.push(ip);
            console.log(`Added: ${ip}`);
        } else {
            console.log(`IP ${ip} already in list`);
        }
    }
    console.log("\n\n--------------------------------------------------------------\n\n");
    return ips;
}

async function askEnableCors() {
    console.log("Enable CORS middleware for this service? (Y/n) [Default: Y]");
    while (true) {
        let ans = (await askQuestion("Enable CORS? (Y/n): ")).trim().toLowerCase();
        if (ans === "" || ans === "y") {
            return true;
        }
        if (ans === "n") {
            return false;
        }
        console.log("Invalid input. Please enter 'Y' or 'n'.");
    }
}

function createServiceDirectory(serviceName) {
    const currentDir = __dirname;
    const grandparentDir = path.dirname(path.dirname(currentDir));
    const serviceFolderName = `service_${serviceName}Service`;
    const serviceDirPath = path.join(grandparentDir, serviceFolderName);
    if (!fs.existsSync(serviceDirPath)) fs.mkdirSync(serviceDirPath, { recursive: true });
    return serviceDirPath;
}

function generateServiceFile(serviceDirPath, serviceName, host, port, privilegedIps, enableCors) {
    const currentDir = __dirname;
    const templatePath = path.join(path.dirname(currentDir), "ServiceTemplates", "Js", "HTTP_SERVICE.txt");
    
    if (!fs.existsSync(templatePath)) {
        console.error(`Template file not found: ${templatePath}`);
        console.error("Please ensure the template exists at the correct location.");
        return null;
    }
    
    let templateContent = fs.readFileSync(templatePath, 'utf-8');

    // Replace placeholders in the template - more specific replacements
    templateContent = templateContent.replace(
        'const httpServerHost = "127.0.0.1";',
        `const httpServerHost = "${host}";`
    );
    
    templateContent = templateContent.replace(
        'const httpServerPort = 8080;',
        `const httpServerPort = ${port};`
    );
    
    templateContent = templateContent.replace(
        'const httpServerPrivilegedIpAddress = ["127.0.0.1"];',
        `const httpServerPrivilegedIpAddress = [${privilegedIps.map(ip => `"${ip}"`).join(", ")}];`
    );
    
    // Handle CORS configuration - replace the entire CORS middleware section
    if (!enableCors) {
        templateContent = templateContent.replace(
            /this\.app\.use\(cors\(\{[\s\S]*?\}\)\);/,
            '// CORS disabled by user choice\n        // this.app.use(cors({ origin: \'*\', credentials: true, methods: \'*\', allowedHeaders: \'*\' }));'
        );
    }

    const serviceFileName = `${serviceName.toLowerCase()}-service.js`;
    const serviceFilePath = path.join(serviceDirPath, serviceFileName);
    
    try {
        fs.writeFileSync(serviceFilePath, templateContent);
        console.log(`Service file created: ${serviceFilePath}`);
        return serviceFilePath;
    } catch (error) {
        console.error(`Error creating service file: ${error.message}`);
        return null;
    }
}

function updateServicesJson(serviceName, host, port, privilegedIps) {
    const currentDir = __dirname;
    const servicesJsonPath = path.join(path.dirname(path.dirname(currentDir)), "services.json");
    let services = [];
    if (fs.existsSync(servicesJsonPath)) {
        try {
            services = JSON.parse(fs.readFileSync(servicesJsonPath, 'utf-8'));
        } catch (error) {
            console.log("Error reading services.json, creating new array");
            services = [];
        }
    }
    
    const newService = {
        "ServiceLanguage": "JavaScript",
        "ServiceName": serviceName,
        "ServiceFolderName": `service_${serviceName}Service`,
        "ServiceFileName": `${serviceName.toLowerCase()}-service.js`,
        "ServiceHttpHost": host,
        "ServiceHttpPrivilegedIpAddress": privilegedIps,
        "ServiceHttpPort": port,
        "ServiceWsPort": null,
        "ServiceType": "HTTP_SERVICE"
    };
    
    services.push(newService);
    fs.writeFileSync(servicesJsonPath, JSON.stringify(services, null, 4));
    console.log(`Updated services.json with new service: ${serviceName}`);
}

function updateEnvFile(serviceName, host, port) {
    const currentDir = __dirname;
    const envFilePath = path.join(path.dirname(path.dirname(currentDir)), ".env");
    let envContent = "";
    if (fs.existsSync(envFilePath)) {
        envContent = fs.readFileSync(envFilePath, 'utf-8');
    }
    const serviceEntry = `${serviceName.toUpperCase()}_SERVICE = "${host}:${port}"`;
    const commentedServiceEntry = `# ${serviceName.toUpperCase()}_SERVICE = "${host}:${port}"`;
    const devMarker = "#<ADD_DEVELOPMENT_SERVICES_ENVRIONMENT_VARIABLES>";
    const prodMarker = "#<ADD_PRODUCTION_SERVICES_ENVRIONMENT_VARIABLES>";
    if (envContent.includes(devMarker)) {
        envContent = envContent.replace(devMarker, `${devMarker}\n${serviceEntry}`);
    }
    if (envContent.includes(prodMarker)) {
        envContent = envContent.replace(prodMarker, `${prodMarker}\n${commentedServiceEntry}`);
    }
    fs.writeFileSync(envFilePath, envContent);
    console.log(`Updated .env file with new service environment variables`);
}

async function main() {
    console.log("=== JavaScript HTTP Service Setup ===");
    const serviceName = await getServiceName();
    const { host, port } = await getHostAndPort();
    const privilegedIps = await getPrivilegedIps();
    const enableCors = await askEnableCors();

    console.log("=== SERVICE CONFIGURATION ===");
    console.log(`Service Name: ${serviceName}`);
    console.log(`HTTP Host: ${host}`);
    console.log(`HTTP Port: ${port}`);
    console.log(`Privileged IP Addresses: ${privilegedIps.join(", ")}`);
    console.log("=============================");

    const serviceDirPath = createServiceDirectory(serviceName);
    const serviceFilePath = generateServiceFile(serviceDirPath, serviceName, host, port, privilegedIps, enableCors);

    updateServicesJson(serviceName, host, port, privilegedIps);
    updateEnvFile(serviceName, host, port);

    console.log(`\nService created successfully!`);
    console.log(`Service Directory: ${serviceDirPath}`);
    console.log(`Service File: ${serviceFilePath}`);
    console.log(`Updated configuration files: services.json and .env`);
}

if (require.main === module) {
    main();
}
