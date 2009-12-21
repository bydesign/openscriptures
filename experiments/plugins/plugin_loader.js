// Taken from http://ejohn.org/blog/simple-javascript-inheritance/
// Inspired by base2 and Prototype
(function(){
  var initializing = false, fnTest = /xyz/.test(function(){xyz;}) ? /\b_super\b/ : /.*/;

  // The base Class implementation (does nothing)
  this.Class = function(){};
 
  // Create a new Class that inherits from this class
  Class.extend = function(prop) {
    var _super = this.prototype;
   
    // Instantiate a base class (but only create the instance,
    // don't run the init constructor)
    initializing = true;
    var prototype = new this();
    initializing = false;
   
    // Copy the properties over onto the new prototype
    for (var name in prop) {
      // Check if we're overwriting an existing function
      prototype[name] = typeof prop[name] == "function" &&
        typeof _super[name] == "function" && fnTest.test(prop[name]) ?
        (function(name, fn){
          return function() {
            var tmp = this._super;
           
            // Add a new ._super() method that is the same method
            // but on the super-class
            this._super = _super[name];
           
            // The method only need to be bound temporarily, so we
            // remove it when we're done executing
            var ret = fn.apply(this, arguments);       
            this._super = tmp;
           
            return ret;
          };
        })(name, prop[name]) :
        prop[name];
    }
   
    // The dummy class constructor
    function Class() {
      // All construction is actually done in the init method
      if ( !initializing && this.init )
        this.init.apply(this, arguments);
    }
   
    // Populate our constructed prototype object
    Class.prototype = prototype;
   
    // Enforce the constructor to be what we expect
    Class.constructor = Class;

    // And make this class extendable
    Class.extend = arguments.callee;
   
    return Class;
  };
})();

OS = {};
OS.Plugin = Class.extend({
	  name: null
	, wordClickHandlers: []
	, wordMouseoverHandlers: []
	, wordMouseoutHandlers: []

	, handleEvents: function(e) {
		var os = openscriptures;
		var ob = jsonParse(e.data);
		if (ob.type == 'wordClick') {
			for (var i = 0; i < os.wordClickHandlers.length; i++) os.wordClickHandlers[i](ob);
		
		} else if (ob.type == 'wordMouseover') {
			for (var i = 0; i < os.wordMouseoverHandlers.length; i++) os.wordMouseoverHandlers[i](ob);
		
		} else if (ob.type == 'wordMouseout') {
			for (var i = 0; i < os.wordMouseoutHandlers.length; i++) os.wordMouseoutHandlers[i](ob);
		}
	}

	, init: function() {
		//if ( e.origin !== "http://bible.openscriptures.org" )
		//	return;
		window.addEventListener("message", this.handleEvents, false);
	}
	
	, name: function(name) {
		this.name = name;
	}
	
	, wordClick: function(f) {
		this.wordClickHandlers.push(f);
	}
	
	, wordHover: function(over, out) {
		this.wordMouseoverHandlers.push(over);
		this.wordMouseoutHandlers.push(out);
	}
	
	, wordMouseover: function(f) {
		this.wordMouseoverHandlers.push(f);
	}
	
	, wordMouseout: function(f) {
		this.wordMouseoutHandlers.push(f);
	}
});

var openscriptures = new OS.Plugin();

