// use with node.js
// install JSV:
// npm install JSV
var JSV = require("JSV").JSV;
var sys = require('sys');
var fs  = require('fs');

var target_file = process.argv[2]; 

if (!target_file){
 console.log("usage: node validate.js dataset.json")
}else{

fs.readFile('../OGPD_JSON_Schema.json',function(err,schema) {
  if(err) throw err;
  fs.readFile(target_file, function(err,data) {
    if(err) throw err;
    // Parse as JSON
    var packages = JSON.parse(data);
    if (!Array.isArray(packages)){packages=[packages]}
    var schemajs= JSON.parse(schema);
    // Validate
    var env = JSV.createEnvironment();
    var report;
    for (var p in packages){
      var dataset = packages[p];
      report = env.validate(dataset, schemajs);
      // Echo to command line
      console.log(dataset["name"] + ": " + report.errors.length + " error(s)");
      if (report.errors.length > 0) {
        console.log(report.errors);
      }
    }
  });
});

}


