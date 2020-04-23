dom.addPlugin("inline", function(params) {
	var element = this;
	params = params || {};
    
    var count = 0;
    
    
    var parent = this.closests(".inline-parent-container");
    
    if ( parent !== null ) {
        var btn_add = parent.findAll(".add-inline-item");
        btn_add.on("click", function(evt) {
           if ( params.hasOwnProperty("template") === true ) {
               var parent_template = parent.find(".subs-container");
               if ( parent_template !== null ) {
                   count = parent.findAll(".item-inline-block").length;
                   
                   var new_iniline_block = parent_template.appendTo(params.template);
                   var inputs = new_iniline_block.findAll(["name='*'"]);
                   
                   var l_inputs = inputs.length;
                   
                   for ( var i = 0; i < l_inputs; i++ ) {
                       var input = inputs.eq(i);
                       var j = count+1;
                       var name = input.getAttribute("name");
                       input.setAttr("name", name+"_"+j);
                   }
                   
               }
           }


        });
    }
    
    
    
    
    
    
}); 