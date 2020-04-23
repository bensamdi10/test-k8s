import invock, {dom} from "invock-js";

dom.addPlugin("active", function(params) {
	var element = this;
	params = params || {};
    var url_document = location.pathname;
    var link_target = dom.getAll("a[href='"+url_document+"']");
    if (link_target !== null) {
        link_target.addClass("active");
    }
});
