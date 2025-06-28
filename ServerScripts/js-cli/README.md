# JavaScript CLI for Microservice Creation

This directory contains JavaScript-based command-line tools for managing microservices.

## add-new-service.js

A Node.js script that automates the creation of new JavaScript microservices with Express.js framework and modular architecture.

### Features

- Interactive CLI for service configuration
- **Modular folder structure** with separate components (DATA, HTTP_SERVER, SERVICE)
- **ES6 modules** with import/export syntax
- Express.js HTTP server template with configurable CORS
- Updates `services.json` and `.env` files automatically
- Input validation for service names, hosts, ports, and IP addresses
- **Utility functions** for each module (route management, data manipulation, etc.)

### Usage

```bash
cd ServerScripts/js-cli
node add-new-service.js
```

### What it creates

For a service named "MyAPI", the script will create:

```
service_MyAPIService/
├── myapi-service.js           # Main service entry point
├── functions.js               # Main service utility functions
├── DATA/
│   ├── data-class.js         # Data management class
│   └── functions.js          # Data manipulation utilities
├── HTTP_SERVER/
│   ├── http-server-class.js  # Express.js server class
│   └── functions.js          # API route management utilities
└── SERVICE/
    └── service-class.js      # Service orchestration class
```

### Modular Architecture

#### Main Service File (`myapi-service.js`)
- Uses ES6 imports to load modular components
- Configures and starts the service
- Contains placeholders for easy configuration updates

#### DATA Module
- **`data-class.js`**: Simple data management class
- **`functions.js`**: Utilities for adding/removing data properties with getters/setters

#### HTTP_SERVER Module
- **`http-server-class.js`**: Express.js server with CORS support and middleware
- **`functions.js`**: API route management (add, remove, update routes)

#### SERVICE Module
- **`service-class.js`**: Service orchestration and startup logic

#### Main Functions (`functions.js`)
- Service configuration management
- Host, port, IP, and CORS setting updates
- Integration with `services.json`

### Service Configuration

The script will prompt you for:

1. **Service Name**: Alphanumeric name without spaces, dashes, or special characters
2. **HTTP Host**: IP address or localhost (default: 127.0.0.1)
3. **HTTP Port**: Port number between 1024-65535 (default: random)
4. **Privileged IP Addresses**: List of IPs allowed to access the service
5. **CORS Configuration**: Enable/disable CORS middleware

### Generated Service Structure

The generated JavaScript service includes:

- **ES6 Module Support**: Full ES6 import/export syntax
- **HTTP_SERVER class**: Express.js server wrapper with middleware setup
- **Data class**: Simple data management with dynamic property support
- **Service class**: Service orchestration class
- **CORS support**: Configurable cross-origin resource sharing
- **Modular utilities**: Each component has its own utility functions
- **Sample API endpoint**: `/api/sample/` route for testing

### Dependencies

The generated services are designed to work with these NPM packages:

- `express`: Web framework
- `cors`: CORS middleware
- `dotenv`: Environment variable management

### After Creation

1. Navigate to the service directory
2. Install dependencies manually if needed
3. Start the service: `node {servicename}-service.js`

### Utility Functions Available

#### Main Service Functions
- `replaceHostInService(newHost)` - Update service host
- `replacePortInService(newPort)` - Update service port
- `replacePrivilegedIpsInService(newIpList)` - Update privileged IPs
- `replaceCorsInService(enableCors)` - Toggle CORS

#### DATA Functions
- `addNewVariable(variableName, defaultValue)` - Add data properties with getters/setters
- `removeVariable(variableName)` - Remove data properties

#### HTTP_SERVER Functions
- `addApiRoute(remainingUrl, method)` - Add new API endpoints
- `removeApiRoute(url)` - Remove existing API endpoints
- `getAllApiRoutes()` - List all API routes
- `updateApiRouteUrl(existingUrl, newUrl)` - Update route URLs
- `updateApiRouteMethod(url, newMethod)` - Update HTTP methods

### Integration

- Updates `services.json` with service metadata
- Updates `.env` file with service environment variables
- Compatible with the existing Python-based server management scripts
- Follows the same naming convention: `service_{serviceName}Service`

### Example Usage

After creating a service, you can use the utility functions:

```javascript
// In your service directory
import { addApiRoute } from './HTTP_SERVER/functions.js';
import { addNewVariable } from './DATA/functions.js';

// Add a new API route
addApiRoute('users', 'post');

// Add a new data property
addNewVariable('userCount', 0);
``` 