"use strict";
Object.defineProperty(exports, "__esModule", {value: true});const cmd = require("node-cmd");
var PythonShell = require('python-shell');
var path = require('path');
const cgp_core_1 = cgp_require("cgp-core");
const cgp_logger = cgp_require('cgp-logger');  //jshint ignore:line

//-----------------------------------------------------------------------------------------------
// 
class fmedge06 { //the name of the class needs to match the name of the js file
    constructor() {
        this.allInOne_Responses = [];
        this.options = { //options listed here must be created in the custom processor
            fileName: 'fmedge06.py',
            outputTag: 'NewTag',
            tags: [],
            passAll: true
        }
        this.sendData = [];
        this.appData = {};
        this.historicalData = new Map();
        this.vqtsOut = new Array();
        this.moduleName = __filename.replace(/^.*(\|\/|\:)/, '').slice(0, -3);
        this.logger = cgp_logger.loggerManager.getLogger(`cgp-${this.moduleName}`);
    }
    execute(appData, next) { 
    	//this function is what is executed by the Edge pipe.  appData is the payload
    	//from the previous processor.  next is what is passed to the next processor 
    	//in the Edge pipe.

        this.appData = appData;
        let dataIn = JSON.parse(this.appData.data[0].vqts[0].v);
        this.logger.warn('InJavascipt');
        this.logger.warn(dataIn);
		let that = this;
		var options = {
            scriptPath: '',
            //mode: 'json',
			args: JSON.stringify(dataIn) 
		};
        // args in options are used to pass data into the Python code.
        let shellpath =__dirname.substring(__dirname.indexOf("ShellApp")+9, __dirname.length);
        let filepath = path.join(shellpath, this.options.fileName);
        PythonShell.run(filepath , options, function (err, results) {
            if (err) throw err;
            //PythonShell invokes Python and then runs the custom script
            // results is what is returned from Python
            that.appData.data[0].vqts[0].v =  results
            next(null, that.appData)
        });
    }
}
exports.fmedge06 = fmedge06; //as with class, must match the name of the js file
