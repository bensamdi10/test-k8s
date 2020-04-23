import invock, {Component} from "invock-js";
import FormCommon from "./common/form";
import Plugins from "../plugins/plugins";

class Account extends Component {
    
    afterRender() {
        var self = this;
        this.applyInputFiles();
    }
    
    applyInputFiles() {
        var self = this;
        var files = dom.getAll(".input-file");
        var l_files = files.length;
        for (var f = 0; f < l_files; f++) {
            var input = files[f];
            self.utils.convertBase64(input, function(base64, file) {
                if (base64 !== "" && base64 !== null) {
                    var parent_children = this.getParent().find(".parent-children");
                    parent_children.html("<div class='inline-block img'><img src='"+base64+"' class='full-image' /></div> <span>"+file.name+"</span>");
                    parent_children.addClass("white-fade");
                    parent_children.getParent().find(".drag-background").hide();
                    this.getParent().find(".input-base64").val(base64);
                    this.getParent().addClass("active");
                }
                else {
                    parent_children.html("");
                    parent_children.removeClass("white-fade");
                    parent_children.getParent().find(".drag-background").hide();
                    this.getParent().find(".input-base64").val("");
                    this.getParent().removeClass("active");
                }
             });
        }
    }
    
}

invock.export("Account", Account);

invock.mount({ parent : "body", root : "{% Account %}" });

var container_form = dom.get("#container-form");

if ( container_form !== null ) {
    invock.mount({ parent : "#container-form", root : "{% FormCommon parent_name='#container-form' %}" });
}

