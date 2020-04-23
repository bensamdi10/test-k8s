import invock, {Component} from "invock-js";

class Paginator extends Component {
    constructor(params) {
        super (params);
        this.nbr_items = 9;
        this.width = 1200;
    }
    
    afterRender() {
        this.buildWrappers();
    }
    
    buildWrappers() {
        var cards = this.parent.findAll(".card-wrapper");
        var l_cards = cards.length;
        var list_cards_content = [];
        var wrapper_content = "";
        for (var i = 0; i < l_cards; i++) {
            var j = i+1;
            if (j%this.nbr_items === 0) {
                wrapper_content += cards.eq(i).html();
                list_cards_content.push(wrapper_content);
                wrapper_content = "";
            }
            else {
                wrapper_content += cards.eq(i).html();
            }
        }
        if (l_cards%this.nbr_items !== 0) {
            list_cards_content.push(wrapper_content);
            wrapper_content = "";
        }
        var parent = dom.get("#container-cards");
        parent.html("");
        var slider = parent.appendTo("<div class='slider-dashboard relative'></div>");
        slider.width(list_cards_content.length*(this.width+100));
        this.insertWrappers(list_cards_content, slider);
        parent.appendTo("<div class='clr'></div>");
    }
    
    insertWrappers(list, parent) {
        var  l = list.length;
        var parent_pagination = dom.get("#paginator-container").find("ul");
        if (l > 0) {
            for (var i = 0; i < l; i++) {
                var content_slide = list[i];
                var wrapper = "<div class='slide-dashboard left'>"+content_slide+"</div>";
                parent.appendTo(wrapper);
                if (l > 1) {
                    parent_pagination.appendTo("<li class='circle-pagination' data-index='"+i+"'></li>");
                }
                
            }
            if (parent_pagination.findAll("li").length > 0) {
                parent_pagination.find("li").addClass("active");
            }
            
            this.buildEventPagination(parent_pagination, parent);
            this.cleanCards(parent);
        }
    }
    
    cleanCards(slider) {
        var slides = slider.findAll(".slide-dashboard");
        var l_slides = slides.length;
        for (var i = 0; i < l_slides; i++) {
            var slide = slides.eq(i);
            var cards = slide.findAll(".card-dashboard");
            var l_cards = cards.length;
            for (var c = 0; c < l_cards; c++) {
                var current_card = cards.eq(c);
                var d = c+1;
                if (c > 0) {
                    current_card.addClass("gratter-left-pourcent");
                }
                if (d%3 === 0) {
                    current_card.addClass("noSpace");
                }
            }
        }
        
    }
    
    buildEventPagination(parent_pagination, slider) {
        var pas = this.width;
        parent_pagination.findAll("li").on("click", function(evt) {
            var index = this.data("index");
            if (index !== null) {
                var ul = this.getParent();
                ul.find(".active").removeClass("active");
                this.addClass("active");
            }
            slider.animate(0.3, { left : -index*pas });
        });
    }
    
    
    
}
invock.export("Paginator", Paginator);

var container_dashboard = dom.get("#container-dashboard");
if (container_dashboard !== null) {
    invock.mount({ parent : "#container-dashboard", root : "{% Paginator %}" });
}