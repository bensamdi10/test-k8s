import invock, {Component} from "invock-js";

export default class PopupConfirmation extends Component {
    constructor(params) {
        super(params);
        this.id = "";
        this.events = { "click input[type='button']" : "actionPopup" };
    }
    afterRender() {
         this.parent.find(".overlay-popup").animate(0.5, { "opacity" : 1});
        
        var scrollTop = document.documentElement.scrollTop;
        
        this.parent.find(".container-popup").css({ top : scrollTop  });
    }
    
    close() {
        var self = this;
        this.parent.find(".overlay-popup").animate(0.5, { "opacity" : 0, onComplete : function() {
                self.parent.find(".overlay-popup").remove();
            } 
        });
        
        this.parent.find(".container-popup").animate(0.5, { "opacity" : 0, onComplete : function() {
                self.parent.find(".container-popup").remove();
            } 
        });
    }
    
    actionPopup(evt, self) {
        var class_yes = this.hasClass("yes");
        var class_no = this.hasClass("no");
        
        if (class_yes) {
            if (typeof self.props.callback !== "undefined" && self.props.callback !== null) {
                self.props.callback.call(this, self);
                self.close();
            }
            
        }
        if (class_no) {
            self.close();
        }
    }
    
    render() {
        return `
            <desktop>
                <div class="overlay-popup"></div>
                <div class="container-popup">
                    <div class="box-popup relative border white box-popup-confirmation">
                        <div class="box30">
                            <h2 class="sub-title align-center">{{props.message|default}}</h2>
                            <div class="top30 align-center">
                                <input type="button" value='لا' class="border-gris no" />
                                <input type="button" value='نعم، انا اؤكد' class="border-green yes" />
                            </div>
                        </div>
                    </div>
                </div>
            </desktop>
          `; 
        
    }
}

