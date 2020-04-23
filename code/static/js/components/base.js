import invock, {Component} from "invock-js";


export default class Base extends Component {
    constructor(params) {
        super(params);
    }
    
    afterRender() {
        this.outZone();
    }
    
    
    
    
    
   outZone() {

      dom.outZone(".option-component", function(elems) {
      
        var option_component = dom.get('.option-component.active');
        var sub_menu_options = dom.get(".sub-menu-options.open"); 
          
        if (option_component !== null && sub_menu_options !== null) {
            option_component.removeClass("active");
            sub_menu_options.removeClass("open");
            sub_menu_options.fadeOut();
        }
     });
   }
    
}


invock.export("Base", Base);

invock.mount({ parent : "body", root : "{% Base %}" });




      