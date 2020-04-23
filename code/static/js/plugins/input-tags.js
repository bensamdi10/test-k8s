import invock, {Http} from "invock-js";


dom.addPlugin("input-tags", function(params) {
	var element = this;
	params = params || {};
    
    if ( params.hasOwnProperty("accept_enter") === false ) {
        params.accept_enter = false;
    }
    
    var drag = false;
    var doc = document.documentElement;
    var scroll_value = doc.scrollTop;
    var move = params.move = true;
    
    var listing_container = element.closests(".input-listing-container");
    if (listing_container !== null) {
        if ( listing_container.data("drag") === true || listing_container.data("drag") === "true" ) {
            drag = true;
        }
    }
    
    if (params.hasOwnProperty("type") === false) {
        params.type = "normal";
    }
    var http = null;
    if (params.type === "ajax") {
        var http = new Http();
    }
    
    function generateID(l) {
        if(typeof l === "undefined") {
			l = 36;
		}
		return Math.random().toString(l).substr(2, 10);
    }
    
    function renderResult(data, parent) {
        parent.html("<ul></ul>");
        var ul = parent.find("ul");
        var l = data.length;
        for (var i = 0; i < l; i++) {
            var item = data[i];
            var value_input_exist = listing_container.find("input.input-tags-container").val();
            var ids_exist = value_input_exist.split(",");
            var l_ids_exist = ids_exist.length;
            var not_exist = false;
            
            if ( value_input_exist !== "" && value_input_exist !== null ) {
                for ( var j = 0; j < l_ids_exist; j++ ) {
                    if (ids_exist[j] !== item.id.toString()) {
                        not_exist = false;
                    }
                    else {
                        not_exist = true;
                    }
                }
            }
            if ( not_exist === false ) {
                    ul.appendTo("<li class='animate' data-id='"+item.id+"' data-name='"+item.name+"'>"+item.name+"</li>");
            }
            
        }
        
        
        ul.findAll("li").on("click",function(evt) {
            var name = this.data("name");
            var id = this.data("id");
            var parent_listing = parent.getParent().find(".input-tags-parent");
            addItemListing(name, parent_listing, id);
            element.val("");
            element.removeClass("autorize");
            parent.fadeOut();
        })
    }
    
    
    
    
    function getDataAjax(url, callback) {
        http.url = url;
        http.fetch(function(response) {
            var data = response.data;
            var parent = element.getParent().find(".result-input-listing");
            if (data.length > 0) {
                renderResult(data, parent);
                parent.fadeIn();
            }
            if (data.length === 0) {
                parent.fadeOut();
            }
            
            
            if ( typeof callback === "function" && callback !== null ) {
                callback.call(this, parent);
            }
        });
    }
    
    
    function applyListingItems(parent) {
        var items = parent.findAll(".sub-element");
        var string_values = "";
        var l = items.length;
        if (l > 0) {
            for (var i = 0; i < l; i++) {
                var item = items.eq(i);
                if (item !== null) {
                    string_values +=  item.data("value")+",";
                }

            }
            if (string_values.length > 1) {
                string_values = string_values.substring(0, string_values.length-1);
            }
        }
        parent.find("input.input-tags-container").val(string_values);
    }
    
    
    function removeItemListing(element, evt, self) {
        var parent = element.closests(".input-listing-container");
        element.getParent().remove();
        applyListingItems(parent);
    }
    
    
    function addItemListing(value, parent, id, ) {
        
        var element_object = true;
        if (params.hasOwnProperty("attr") === true) {
            element_object = false;
        }
        
        var id_element = 'remove-item-'+id;
        if (element_object === true) {
            parent.appendTo('<span class="sub-element relative no-active" data-value="'+id+'" data-name="'+value+'"><span class="span-name">'+value+' </span><span id="remove-item-'+id+'" class="close-btn hover-fade"></span></span>');
        }
        else {
            parent.appendTo('<span class="sub-element relative no-active" data-value="'+value+'"><span class="span-name">'+value+' </span><span id="remove-item-'+id+'" class="close-btn hover-fade"></span></span>');
        }
        
        var self = this;
        parent.find("#"+id_element).on("click", function(evt) {
            removeItemListing(this, evt, self);
        });
        applyListingItems(parent.closests(".input-listing-container"));
        
        //dragDrop();
    }
    element.on("focus", function(evt) {
        var value = this.val();
        if (value !== "" && value !== " ") {
            var parent = element.closests('.input-listing-container').find(".result-input-listing");
            var li_listing = parent.findAll("li");
            if (li_listing.length > 0) {
                parent.fadeIn();
            }
            
            getDataAjax("/api/backend"+params.url+"?q="+value);
        }
    });
    
    var count = -1;
    element.on("keyup", function(evt) {
        var type = this.data("type");
        var value = this.val();
        var key_code = evt.keyCode;
        
        
        
        if ( key_code === 27 ) {
            element.getParent().find(".result-input-listing").fadeOut();
        }
        
        if ( key_code === 13 && params.accept_enter === true ) {
            var parent_listing = this.getParent().find(".input-tags-parent");
            addItemListing(value, parent_listing, generateID());
            element.val("");
            element.removeClass("autorize");
        }
        else {
            if (type === "url" && value.indexOf("http") > -1 && value.length > 10) {
                this.addClass("autorize");
            }

            if (type === "text" && value.length > 2) {
                this.addClass("autorize");
            }
            
            if (  key_code !== 38 && key_code !== 40 ) {
                getDataAjax("/api/backend"+params.url+"?q="+value, function(element_parent) {
                    element_parent.closests(".input-listing-container").on("keyup", function(evt) {
                        var key_code_ = evt.keyCode
                        var lis = element_parent.findAll("li");
                        var l_li = lis.length;
                        if (  l_li > 0 ) {
                            if (  key_code_ === 38 && count > 0 ) {
                                count = count-1;
                            }
                            if (  key_code_ === 40 && count < l_li-1 ) {
                                count = count+1;
                            }

                            var selected_li = element_parent.find("li.selected");

                            if ( selected_li !== null && key_code_ === 13) {
                                var name = selected_li.data("name");
                                var id = selected_li.data("id");
                                var parent_listing = element_parent.getParent().find(".input-tags-parent");
                                addItemListing(name, parent_listing, id);
                                element.val("");
                                element.removeClass("autorize");
                                element_parent.fadeOut();
                            }
                            else if( selected_li !== null ){
                                selected_li.removeClass("selected");
                            }
                            
                            var li_target = lis.eq(count);
                            if ( li_target !== null && typeof li_target !== "undefined") {
                                li_target.addClass("selected");
                                var offset_li_selected = li_target.offset();
                                if ( count >= 5 ) {
                                    var step = (li_target.height())* (count - 4);
           
                                    element_parent.scrollTop =  step;
                                    
                                }

                            }
                        }

                        
                    });
                    


                });
            
            
            }
            
            
            
            
            if (evt.keyCode === 13 && element.hasClass("autorize") === true && params.type !== "ajax") {
                
                var parent_listing = this.getParent().find(".input-tags-parent");
                addItemListing(value, parent_listing, generateID());
                element.val("");
                element.removeClass("autorize");
            }
        }
        
        
        
    });
    
    
    /*DRAG FUNCTIONS*/
    
    //dragDrop();
    
    var coordonnes_elements = [];
    var test = "";
    var sub_elements = listing_container.findAll(".span-name");
    var sub_elements_parent = listing_container.findAll(".sub-element");
    
    function dragDrop() {
        var height_element = 35;
        var current_element = null;
        if (drag === true) {
            sub_elements = listing_container.findAll(".span-name");
            sub_elements_parent = listing_container.findAll(".sub-element");
            var count = sub_elements_parent.length;
            if ( count > 0 ) {
                coordonnes_elements = [];
                for (var c = 0; c < count; c++) {
                    var item = sub_elements_parent.eq(c);
                    height_element = item.height();
                    var offset_item = item.offset();
                    coordonnes_elements.push( offset_item );
                    test = "test";
                    if (item.hasClass("dragging") === false) {
                        dragComponent(item, coordonnes_elements, test);
                    }
                }
                
                
            }
        
        }
        
        
        
    }
    
    function dragComponent(component, coordonnes_elements, test) {
        
        var height_element = 35;
        var current_element = null;
        var count = sub_elements.length;
        component.addClass("dragging");
        component.find(".span-name").on("mousedown", function(evt) {         
            var composant = this;
            
            
            current_element  = this.getParent();
            current_element.addClass("down");
            var index_element = this.getParent().index(".sub-element", this.getParent().getParent());
            var clone = composant.clone();
            var offset = composant.offset();
            clone.addClass("no-animate draggable");
            var width_clone = composant.offset().width;
            scroll_value = doc.scrollTop;
            var top_value = scroll_value+offset.top;
            clone.css({ "width" : width_clone+"px", "position" : "absolute", "top" : top_value+"px", "left" : offset.left+"px"  });
            var body = dom.get("body");
            move = params.move =  true;
            var index_array = [];
            var index = null;
            body.on("mousemove", function(evtm) {
                if (current_element !== null) {
                    var timer = setTimeout(function() {
                        if (move && clone !== null) {
                            scroll_value = doc.scrollTop;
                            var x = evtm.clientX+10;
                            var y = evtm.clientY+scroll_value;

                            var count_new = coordonnes_elements.length;
                            var before = true;
                            if ( coordonnes_elements[index_element].top > y ) {
                                before = true;
                            }
                            else {
                                before = false;
                            }

                            for (var n = 0; n < count_new; n++) {

                                var item_offset = coordonnes_elements[n];
                                if (  Math.abs(y - item_offset.top ) < 3)  {
                                    index_array.push(n);
                                    index = n;
                                    //n = count_new;
                                } 

                            }

                            if (index !== null && index_element !== index) {
                                var target = sub_elements_parent.eq(index);
                                var clones = listing_container.findAll(".clone-sortable");
                                if ( clones.length > 0) {
                                    clones.remove();
                                }

                                // Math.abs(y - coordonnes_elements[index_element].top ) > height_element && 

                                if ( listing_container.findAll(".clone-sortable").length === 0) {

                                    if (target !== null && typeof target !== "undefined") {
                                        if ( before === true ) {
                                            target.before("<div class='clone-sortable'></div>");
                                        }
                                        else {
                                            target.after("<div class='clone-sortable'></div>");
                                        }

                                    }
                                }


                            }



                            clone.css({ "top" : y+"px" });
                        }
                    }, 150);
                }
                
                
                
                evtm.preventDefault();
            }, true);



            body.on("mouseup", function(evtu) {
                index = index_array[index-1];
                var result_sortable = false;
                var x_up = evtu.clientX;
                var y_up = evtu.clientY;
                //current_element = sub_elements.eq(index);
                scroll_value = doc.scrollTop;
                var clone_sortable = listing_container.find(".clone-sortable");
                if (clone_sortable !== null && current_element !== null ) {
                    
                    var element_after = clone_sortable.after(current_element);
                    
                    
                    
                    
                    element_after.getParent().addClass("no-active");
                    element_after.getParent().removeClass("dragging");
                    element_after.getParent().removeClass("down");
                    current_element.removeClass("down");
                    clone_sortable.remove();
                    current_element.remove();
                    
                    var new_sub_elements = listing_container.findAll(".sub-element");
                    var count_new = new_sub_elements.length;
                    
                    var element_down = listing_container.find('.down');
                    if ( element_down !== null && count_new > count) {
                        element_down.remove();
                    }

                    new_sub_elements = listing_container.findAll(".sub-element");
                    var count_new = new_sub_elements.length;
                    var ids = [];
                    for (var i = 0;i < count_new; i++) {
                        ids.push(new_sub_elements[i].data("value"));
                    }

                    listing_container.find(".input-tags-container").val(ids.toString());

                   
                    dragDrop();

                }
                
                 
                if (clone !== null) {
                    body.off("mousemove");
                    clone.removeClass("no-animate draggable");


                    var timer = setTimeout(function() {
                        clone.remove();
                        clone = null;
                    }, 100);
                }
                evtu.preventDefault();
            }, true);

            evt.preventDefault();
        });
    }
    
    
}); 