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
    var posts = JSON.parse(data);
    var schemajs= JSON.parse(schema);
    // Validate
    var env = JSV.createEnvironment();
    var report = env.validate(posts, schemajs);
    // Echo to command line
    console.log(target_file + ": " + report.errors.length + " error(s)");
    if (report.errors.length > 0) {
      console.log(report.errors);
    }
  });
});

}


