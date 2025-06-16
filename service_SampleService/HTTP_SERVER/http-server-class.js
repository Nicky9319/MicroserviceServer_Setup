import express from 'express';
import cors from 'cors';

class HTTP_SERVER {
    constructor(httpServerHost, httpServerPort, httpServerPrivilegedIpAddress = ["127.0.0.1"], dataClassInstance = null, enableCors = true) {
        this.app = express();
        this.host = httpServerHost;
        this.port = httpServerPort;
        this.privilegedIpAddress = httpServerPrivilegedIpAddress;
        this.dataClass = dataClassInstance;
        this.corsEnabled = false;

        // Conditionally add CORS middleware
        if (enableCors) {
            this.app.use(cors({
                origin: '*',
                credentials: true,
                methods: '*',
                allowedHeaders: '*'
            }));
            this.corsEnabled = true;
        }
    }

    configureRoutes() {
        // /api/sample/ endpoint
        this.app.get('/api/sample/', (req, res) => {
            console.log("Running Through Someone Else");
            res.json({ message: "Hello World" });
        });

        // Add new APIs here if needed
    }

    runApp() {
        this.app.listen(this.port, this.host, () => {
            console.log(`Server running at http://${this.host}:${this.port}/`);
        });
    }
}

export default HTTP_SERVER;