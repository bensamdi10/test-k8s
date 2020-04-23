
module.exports = function(grunt) {
  require("load-grunt-tasks")(grunt);
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    cssmin: {
          target: {
              files: {
                  '../css/style.css': [ '../css/src/font-face.css', '../css/src/ui.css', '../css/src/form.css',
                                          '../css/src/table_listing.css', '../css/src/calendar.css', '../css/src/style.css',
                                         
                                         ]
                }
          }
    },
	  watch: {
		  scripts: {
		    files: ['../css/src/*.css'],
		    tasks: ['cssmin'],
		    options: {
		      spawn: false,
		    },
		 },
	},
	
	
	
  }); 
  grunt.loadNpmTasks('grunt-contrib-watch');
  
  //grunt.registerTask('default', ['jasmine']);
  grunt.registerTask('default', ['watch']);
  grunt.registerTask('dev', ['concat']);

};
/*
pivotal : {
            files: ['js/*.js', 'components/*.js', 'index.js', 'tests/specs/*.js'],
            tasks: 'jasmine:pivotal:build'
          },*/