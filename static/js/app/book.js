// Place third party dependencies in the lib folder
//
// Configure loading modules from the lib directory,
// except 'app' ones,
requirejs.config({
    "baseUrl": "/static/js/lib",
    "paths": {
      "module": "../module" ,
      "app": "../app",
      "jquery": "jquery-1.10.2"
    }
});

// Load the main app module to start the app
requirejs(["jquery","module/book"]);
