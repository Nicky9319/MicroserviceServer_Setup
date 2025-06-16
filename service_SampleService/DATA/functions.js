import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DATA_CLASS_PATH = path.join(__dirname, 'data-class.js');

export function addNewVariable(variableName, defaultValue = null) {
    // Read the current data-class.js file
    let sourceCode = fs.readFileSync(DATA_CLASS_PATH, 'utf8');
    
    // Check if variable already exists in constructor
    const constructorPropertyRegex = new RegExp(`this\\.${variableName}\\s*=`);
    if (constructorPropertyRegex.test(sourceCode)) {
        console.log(`Variable '${variableName}' already exists in the Data class`);
        return;
    }
    
    // Check if getter method already exists
    const getterMethodRegex = new RegExp(`get_${variableName}\\(\\)`);
    if (getterMethodRegex.test(sourceCode)) {
        console.log(`Getter method 'get_${variableName}' already exists in the Data class`);
        return;
    }
    
    // Check if setter method already exists
    const setterMethodRegex = new RegExp(`set_${variableName}\\(`);
    if (setterMethodRegex.test(sourceCode)) {
        console.log(`Setter method 'set_${variableName}' already exists in the Data class`);
        return;
    }
    
    // Format the default value
    let formattedDefaultValue;
    if (defaultValue === null) {
        formattedDefaultValue = 'null';
    } else if (typeof defaultValue === 'string') {
        formattedDefaultValue = `'${defaultValue}'`;
    } else {
        formattedDefaultValue = String(defaultValue);
    }
    
    // Add property to constructor
    const constructorProperty = `        this.${variableName} = ${formattedDefaultValue};`;
    
    // Find the constructor and add the new property
    sourceCode = sourceCode.replace(
        /(constructor\(\) {[\s\S]*?)(    })/,
        `$1${constructorProperty}\n$2`
    );
    
    // Create getter method
    const getterMethod = `    get_${variableName}() {
        return this.${variableName};
    }`;
    
    // Create setter method
    const setterMethod = `    set_${variableName}(value) {
        this.${variableName} = value;
    }`;
    
    // Add methods before the closing brace of the class
    sourceCode = sourceCode.replace(
        /(\n})(\n\nexport default Data;)/,
        `${getterMethod}\n${setterMethod}\n$1$2`
    );
    
    // Write the modified code back to the file
    fs.writeFileSync(DATA_CLASS_PATH, sourceCode);
    
    console.log(`Added variable '${variableName}' with getter/setter methods to Data class`);
}

addNewVariable('taxesPaids', false); // Example usage with boolean instead of string