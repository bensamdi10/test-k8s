import invock, {dom, utils} from "invock-js";

dom.addPlugin("table_paginator", function(params) {
	var element = this;
	var parent = this.getParent();
	params = params || {};
    var thead = element.find("thead");
    var tbody = element.find("tbody");
    var footer = element.getParent().getParent().find(".footer-table");
    var limit = params.limit || 10;
   
    var rows = tbody.findAll("tr");
    var l_rows = rows.length;
    var nbr_pages = Math.ceil(l_rows/limit);
    
    if (nbr_pages > 1) {
        footer.appendTo("<ul class='horizontal'></ul>");
        var page = 0;
        var table_simulator = [];

        for (var p = 0; p < nbr_pages; p++ ) {
            var temp_table = [];
            var j = p+1;
            var k = (j*limit)-limit;

            for (var i = k; i < j*limit; i++) {
                if (i <= l_rows - 1) {
                    var row = rows.eq(i);
                    temp_table.push(row);
                    if (i > limit-1) {
                        row.remove();
                    }
                }   
            }

            table_simulator.push(temp_table);

            footer.find("ul").appendTo("<li class='table-page animate' data-index='"+p+"'>"+j+"</li>");

        }



        footer.appendTo("<div class='clr'></div>");

        footer.find(".table-page").addClass("active");
        footer.findAll(".table-page").on("click", function(evt) {
            var index = this.data("index");
            if (index !== null) {
                page = index;
            }
            footer.find(".table-page.active").removeClass("active");
            this.addClass("active");
            var new_page = table_simulator[index];
            var l_new_page = new_page.length;
            tbody.html("");
            for (var n = 0; n < l_new_page; n++) {
                tbody.appendTo(new_page[n]);
            }
            var column_sorted = thead.find("th[aria-sort]");
            if (column_sorted !== null) {
                var value_sorted = column_sorted.attr("aria-sort");
                if (value_sorted == "descending") {
                    column_sorted.click();
                    column_sorted.click();
                }
                else {

                    column_sorted.click();
                }
            }
            
            if (typeof params.afterNavigate === "function" && params.afterNavigate !== null ) {
                params.afterNavigate.call(this);
            }

        });
    }
    
}); 