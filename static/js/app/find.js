// Place third party dependencies in the lib folder
//
// Configure loading modules from the lib directory,
// except 'app' ones,
requirejs.config({
    "baseUrl": "/static/js",
    "paths": {
      "module": "module" ,
      "app": "app",
      "jquery": "lib/jquery-1.10.2"
    }
});

// Load the main app module to start the app
requirejs(["module/find"]);
