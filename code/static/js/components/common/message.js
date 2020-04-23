import invock, {Component} from "invock-js";


export default class Message extends Component {
    constructor(params) {
        super(params);
        this.state = { type : "", message : "" };
    }
    display(objet) {
        this.setState(objet);
        var self = this;
        var timer = setTimeout(function() {
            var parent_message = dom.get(".message-element");
            parent_message.removeClass("success-message");
            parent_message.removeClass("errors-message");
            parent_message.addClass(self.props.type);
            parent_message.animate(1, { "top" : 0, "opacity" : 1 });
            var timer = setTimeout(function() { //
                parent_message.animate(0.5, { "top" : -20, "opacity" : 0, onComplete : function() {  parent_message.closests("message").remove(); 
                                                                                                  if (typeof self.props.callback === "function" && self.props.callback !== null ) { self.props.callback.call(this); }
                                                                                                  } });

            }, 4000);
            
        }, 100);
        
        
    }
    
    afterRender() {
        var type = this.props.type;
        var message = this.props.message;
        var objet = {};
        if (type === "success") {
            objet = { type : "success-message", message : message };
            this.props.type = "success-message";
        }
        if (type === "error") {
             objet = { type : "errors-message", message : message };
            this.props.type = "errors-message";
        }
        this.display(objet);
        //dom.get(".overlay").fadeIn();
    }
    render() {
        return `
        <desktop>
            <div class="message-element"><div class="center-auto box15 align-center font22">{{props.message}}</div></div>
        </desktop>
      `; 
    }
    
}


invock.export("Message", Message);