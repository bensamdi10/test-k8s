import invock, {dom, utils} from "invock-js";
dom.addPlugin("calendar", function(params) {
	var element = initHTML();
	var parent = this.getParent();
    var result_calendar = { start : "", end : "", type : "day" };
    var width_slide = 500;
    var nbr_months = 0;
    
	params = params || {};
    var range = true;
    
    if (params.hasOwnProperty("range") === true) {
        range = params.range;
    }
    
    
    
    if ( typeof params.lang === "undefined" ) {
        params.lang = "en";
    }
    
    var align = params.align || "left";
    var name_space = params.name_space || "calendar-picker";
    params.name_space = name_space;
    var doc = document.documentElement;
    var scroll_value = doc.scrollTop;
    
    if (typeof params.supportZero === "undefined") {
        params.supportZero = true;
    }
    
    
    var type_range = element.find(".type-range");
    type_range.findAll("li").on("click", function() {
       var type = this.attr("data-value");
       result_calendar.type = type;
       type_range.find(".active").removeClass("active");
       this.addClass("active");
    });
    
    var action_calendar = element.find(".action-calendar");
    action_calendar.findAll("input").on("click", function() {
        var value = this.attr("data-value");
        if (value === "apply") {
            if (typeof params.afterApply === "function") {
                params.afterApply.call(this, result_calendar);
                element.removeClass("active");
                element.hide();
            }
        }
        element.removeClass("active");
        element.hide();
    });
    if (params.btn !== null) {
        params.btn.on("click", function() {
            var offset = this.offset();
           var class_active = element.hasClass('active');
            if (class_active) {
                element.removeClass("active");
                element.fadeOut();
            }
            else {
                element.addClass("active");
                element.fadeIn();
                if (offset.height === 0) {
                    offset.height = 63;
                }
                
                scroll_value = doc.scrollTop;
                
                if ( align === "left" ) {
                    element.css({  "left" : offset.left, "top" : offset.top+offset.height+scroll_value});
                }
                if (align === "right") {
                    element.css({  "left" : (offset.left+offset.width) - 482, "top" : offset.top+offset.height+scroll_value});
                }
                if (align === "center") {
                    element.css({  "left" : offset.left-(482/2), "top" : offset.top+offset.height+scroll_value});
                }
                
            }
            
        });
    }
    
    
    var today = new Date();
    
    
    var today_year = today.getFullYear();
    
    var bissextile = getBissextile(today_year);
    
    var month = today.getMonth();
    var day = today.getDay();
    var day_number = today.getDate();
    var day_debut_month_today =  getStartMonth(month, day_number, day);
    var current_month = createMonth(month, day_debut_month_today, today_year );
    var month_prev_number = getPrevMonth(month).month;
    var day_debut_prev_month = getStartMonthPrev(month_prev_number, day_debut_month_today, bissextile);
    var prev_month = createMonth(month_prev_number, day_debut_prev_month,getPrevMonth(month).year);
    var month_next_number = getNextMonth(month).month;
    if (month_next_number === 12) {
        month_next_number = 0;
    }
    var next_month = createMonth(month_next_number, current_month.day_fin+1, getNextMonth(month).year);
    var last_day_prev = prev_month.day_fin;
    var last_day = next_month.day_fin;
    var slider_months_calendar = element.find(".slider-months-calendar");
    var container = element.find('.days-container');
    var container_child = container.find('.slider-days-container');
    var list_months = [month-1+"-"+today_year, month+"-"+today_year, month+1+"-"+today_year ];
    
    
    
    renderMonth(prev_month);
    renderMonth(current_month, function(day_name, day_column) {
        day_column.find(".day-"+day_number).addClass("current");
    });
    renderMonth(next_month);
    
    
    
    
    
    function getNextMonth(month) {
        var month_next_number = month;
        var year_next = today_year;
        if (month < 11) {
            month_next_number +=1;
        }
        else {
            month_next_number = 0;
            year_next +=1;
        }
        return { "month" : month_next_number, "year" : year_next };
    }
    
    function getPrevMonth(month) {
        var month_prev_number = month;
        var year_prev = today_year;
        if (month < 0) {
            month_prev_number = 11;
            year_prev -=1;
        }
        else {
            if (month > 0) {
                month_prev_number -= 1;
            }
            else {
                month_prev_number = 11;
                year_prev -=1;
            }
        }
        return { "month" : month_prev_number, "year" : year_prev };
    }
    
    var current_slide = 0;
    var prev_calendar = element.find(".prev-calendar");
    var prev_counter = 0;
    var step = 143.5;
    prev_calendar.on("click", function() {
        
        if (current_slide > -24) {
            
            if (month_prev_number < 0) {
                month_prev_number = 11;
                today_year -=1;
            }
            else {
                if (month_prev_number > 0) {
                    month_prev_number -= 1;
                }
                else {
                    month_prev_number = 11;
                    today_year -=1;
                }
            }
            
            if (!findInArray(list_months, month_prev_number+"-"+today_year)) {
                
                list_months.push(month_prev_number+"-"+today_year);
                var day_debut_prev_month_prev = getStartMonthPrev(month_prev_number, day_debut_prev_month, bissextile);
                var prev_month_prev = createMonth(month_prev_number, day_debut_prev_month_prev,getPrevMonth(month).year);
                day_debut_prev_month = getStartMonthPrev(month_prev_number, day_debut_prev_month, bissextile);
                renderMonth(prev_month_prev, getPrevMonth(month).year, function(day, column, li_month) {
                    prev_counter++;
                    column.css({ "margin-left" : -step*prev_counter });
                    li_month.css({ "margin-left" : -step*prev_counter });

                }, true);
            }
            current_slide -=1;
            slider_months_calendar.animate(0.5, { "left" : -step*current_slide, ease:"easeInSine" });
            container_child.animate(0.5, { "left" : -step*current_slide, ease:"easeInSine" });
        }
        
    });
    var next_calendar = element.find(".next-calendar");
    next_calendar.on("click", function() {
        if (month_next_number < 11) {
            month_next_number +=1;
        }
        else {
            month_next_number = 0;
            today_year +=1;
        }
        if (!findInArray(list_months, month_next_number+"-"+today_year)) {
            last_day +=1;
            list_months.push(month_next_number+"-"+today_year);
            var next_month_next = createMonth(month_next_number, last_day, getNextMonth(month).year);
            renderMonth(next_month_next, getNextMonth(month).year);
            last_day = next_month_next.day_fin;
        }
        current_slide +=1;
        slider_months_calendar.animate(0.5, { "left" : -step*current_slide, ease:"easeInSine" });
       container_child.animate(0.5, { "left" : -step*current_slide, ease:"easeInSine" });
    });
    
    
    var date_debut = null, date_fin = null;
    
    initDate();
    
    
    function initHTML() {
        var html_code =  `
                <div class="type-range align-center none">
                    <ul class="horizontal inline-block">
                        <li data-value="day" class="active"><span class="block name-block">Journey</span>  <span class="block violet-date-active"></span></li>
                        <li data-value="week"><span class="block name-block">Weekly</span>  <span class="block violet-date-active"></span></li>
                        <li data-value="month"><span class="block name-block">Monthly</span>  <span class="block violet-date-active"></span></li>
                        <li data-value="all"><span class="block name-block">All</span>  <span class="block violet-date-active"></span></li>
                    </ul>
                    <div class="clr"></div>
                </div>

                <div class="range-choice align-center">
                    <ul class="horizontal gris inline-block box10">
                        <li></li>
                        <li></li>
                    </ul>
                    <div class="clr"></div>
                </div>

                <div id="calendar-details" class="center-auto top10">
                    <div class="header-calendar relative">
                        <div class="prev-calendar pointer left absolute"></div>
                        <div class="months-calendar left center-auto">
                            <div class="slider-months-calendar relative">
                                <ul class="horizontal align-center">

                                </ul>
                                <div class="clr"></div>
                            </div>

                        </div>
                        <div class="next-calendar pointer right absolute"></div>
                        <div class="clr"></div>
                    </div>

                    <div class="barre-days gris-tabs">
                        <div class="center-auto">
                            <div class="day-column left first-day-column">
                                <ul class="horizontal">
                                    <li class="box-day">M</li>
                                    <li class="box-day">T</li>
                                    <li class="box-day">W</li>
                                    <li class="box-day">T</li>
                                    <li class="box-day">F</li>
                                    <li class="box-day">S</li>
                                    <li class="box-day">S</li>
                                </ul>
                                <div class="clr"></div>
                            </div>
                            <div class="day-column left">
                                <ul class="horizontal">
                                    <li class="box-day">M</li>
                                    <li class="box-day">T</li>
                                    <li class="box-day">W</li>
                                    <li class="box-day">T</li>
                                    <li class="box-day">F</li>
                                    <li class="box-day">S</li>
                                    <li class="box-day">S</li>
                                </ul>
                                <div class="clr"></div>
                            </div>
                            <div class="day-column left">
                                <ul class="horizontal">
                                    <li class="box-day">M</li>
                                    <li class="box-day">T</li>
                                    <li class="box-day">W</li>
                                    <li class="box-day">T</li>
                                    <li class="box-day">F</li>
                                    <li class="box-day">S</li>
                                    <li class="box-day">S</li>
                                </ul>
                                <div class="clr"></div>
                            </div>
                            <div class="clr"></div>
                        </div>
                    </div>
                    <div class="days-container bottom10">
                        <div class="center-auto top10 container-slider-days">
                              <div class="slider-days-container relative">

                              </div>
                        </div>

                        <div class="clr"></div>
                    </div>

                </div>

                
        `;
        
        if (params.lang === "ar") {
              html_code =  `
                <div class="type-range align-center none">
                    <ul class="horizontal inline-block">
                        <li data-value="day" class="active"><span class="block name-block">Journey</span>  <span class="block violet-date-active"></span></li>
                        <li data-value="week"><span class="block name-block">Weekly</span>  <span class="block violet-date-active"></span></li>
                        <li data-value="month"><span class="block name-block">Monthly</span>  <span class="block violet-date-active"></span></li>
                        <li data-value="all"><span class="block name-block">All</span>  <span class="block violet-date-active"></span></li>
                    </ul>
                    <div class="clr"></div>
                </div>

                <div class="range-choice align-center">
                    <ul class="horizontal gris inline-block box10">
                        <li></li>
                        <li></li>
                    </ul>
                    <div class="clr"></div>
                </div>

                <div id="calendar-details" class="center-auto top10">
                    <div class="header-calendar relative">
                        <div class="prev-calendar pointer left absolute"></div>
                        <div class="months-calendar left center-auto">
                            <div class="slider-months-calendar relative">
                                <ul class="horizontal align-center">

                                </ul>
                                <div class="clr"></div>
                            </div>

                        </div>
                        <div class="next-calendar pointer right absolute"></div>
                        <div class="clr"></div>
                    </div>

                    <div class="barre-days gris-tabs">
                        <div class="center-auto">
                            <div class="day-column left first-day-column">
                                <ul class="horizontal">
                                    <li class="box-day">الإث</li>
                                    <li class="box-day">الثلا</li>
                                    <li class="box-day">الأر</li>
                                    <li class="box-day">الخم</li>
                                    <li class="box-day">الجم</li>
                                    <li class="box-day">الس</li>
                                    <li class="box-day">الأح</li>
                                </ul>
                                <div class="clr"></div>
                            </div>
                            <div class="day-column left">
                                <ul class="horizontal">
                                    <li class="box-day">الإث</li>
                                    <li class="box-day">الثلا</li>
                                    <li class="box-day">الأر</li>
                                    <li class="box-day">الخم</li>
                                    <li class="box-day">الجم</li>
                                    <li class="box-day">الس</li>
                                    <li class="box-day">الأح</li>
                                </ul>
                                <div class="clr"></div>
                            </div>
                            <div class="day-column left">
                                <ul class="horizontal">
                                    <li class="box-day">الإث</li>
                                    <li class="box-day">الثلا</li>
                                    <li class="box-day">الأر</li>
                                    <li class="box-day">الخم</li>
                                    <li class="box-day">الجم</li>
                                    <li class="box-day">الس</li>
                                    <li class="box-day">الأح</li>
                                </ul>
                                <div class="clr"></div>
                            </div>
                            <div class="clr"></div>
                        </div>
                    </div>
                    <div class="days-container bottom10">
                        <div class="center-auto top10 container-slider-days">
                              <div class="slider-days-container relative">

                              </div>
                        </div>

                        <div class="clr"></div>
                    </div>

                </div>

                
        `;   
        }
        
        
        var btns_calendar = '<div class="action-calendar top20 align-center bottom10">'+
                    '<input type="button" value="Apply" class="border-violet action-calendar" data-value="apply" />'+
                    '<input type="button" value="Cancel" class="border-gris action-calendar " data-value="cancel" />'+
                '</div>';
        
            if (params.lang === "fr") {
                btns_calendar = '<div class="action-calendar top20 align-center bottom10">'+
                    '<input type="button" value="Appliquer" class="border-violet action-calendar" data-value="apply" />'+
                    '<input type="button" value="Fermer" class="border-gris action-calendar black-color" data-value="cancel" />'+
                '</div>';
            }
            
            if (params.lang === "ar") {
                btns_calendar = '<div class="action-calendar top20 align-center bottom10">'+
                    '<input type="button" value="تطبيق" class="border-violet action-calendar" data-value="apply" />'+
                    '<input type="button" value="إلغاء" class="border-gris action-calendar black-color" data-value="cancel" />'+
                '</div>';
            }
            
        
        var container_calendar_parent = dom.get("#calendar-"+params.name_space);
        if (container_calendar_parent !== null) {
            container_calendar_parent.remove();
        }
        
        html_code = html_code+btns_calendar;
        
        var body = dom.get("body");
        var style_scroll = "";
        if (params.scroll === false) {
            style_scroll = "position : fixed;"
        }
        var calendar_container_html = '<div id="calendar-'+params.name_space+'" class="absolute border white box15 calendar-container" style="'+style_scroll+'"></div>';
        var container = body.appendTo(calendar_container_html);
        container.html(html_code);
        return container;
        
        
        
        
    }
    function initDate() {
        if (typeof params.init_date !== "undefined" && params.init_date !== "") {
            var split_init_date = params.init_date.split(", ");
            
            var l_split_init_date = split_init_date.length;
            
            if ( l_split_init_date === 2 ) {
                var date_debut_init = split_init_date[0];
                var date_fin_init = split_init_date[1];
            }
            else {
                var date_debut_init = split_init_date[0];
                var date_fin_init = date_debut_init;
            }
            var split_date_debut = date_debut_init.split('-');
            var month_date_debut = parseInt(split_date_debut[1])-1;
            if (month_date_debut === -1) {
                month_date_debut = 0;
            }
            
            var day_date_debut = split_date_debut[2];
            var year_date_debut = split_date_debut[0];
            
            
            
            split_date_debut[1] = month_date_debut;
            date_debut_init = day_date_debut+ " "+ month_date_debut+" "+year_date_debut;

            var split_date_fin = date_fin_init.split('-');
            var month_date_fin = parseInt(split_date_fin[1])-1;
            
            
            if (year_date_debut >= next_month.year) {
                if (month_date_debut > next_month.month_number) {
                    var l_diff = month_date_debut - next_month.month_number;
                    for (var i = 0; i < l_diff; i++) {
                        next_calendar.click();
                    }
                }

                if (month_date_fin > next_month.month_number) {
                    var l_diff_fin = month_date_fin - next_month.month_number;
                    for (var j = 0; j < l_diff_fin; j++) {
                        next_calendar.click();
                    }
                }
                
                if (month_date_debut < current_month.month_number) {
                    var l_diff_prev = current_month.month_number - month_date_debut;
                    for (var k = 0; k < l_diff_prev; k++) {
                        prev_calendar.click();
                    }
                }
                if (month_date_fin < current_month.month_number) {
                    var l_diff_prev_fin = current_month.month_number - month_date_fin;
                    for (var m = 0; m < l_diff_prev_fin; m++) {
                        next_calendar.click();
                    }
                }
            }
            else {
                var l_prev_year_months = 12 - month_date_debut;
                    for (var n = 0; n < l_prev_year_months; n++) {
                        prev_calendar.click();
                    }
            }
            
            split_date_fin[1] = month_date_fin;
            var day_date_fin = split_date_fin[2];
            var year_date_fin = split_date_fin[0];
            date_fin_init = day_date_fin+ " "+ month_date_fin+" "+year_date_fin;

            date_debut = date_debut_init;
            date_fin = date_fin_init;
            var diff_dates = diffDates(date_fin, date_debut);
            
            
            
            activeChoices(date_debut, date_fin, diff_dates.number_days);
            displayDate(date_debut, date_fin);
        }
    }
    
    function runChoice() {
        element.findAll('.box-day-active').lockEvent = false;
        element.findAll('.box-day-active').on("click", function() {
            var number_day = this.attr("data-day");
            var number_month = this.attr("data-month");
            var number_year = this.attr("data-year");
            var date_box = getDateFormat(number_day, number_month, number_year);
            var date_box_compar = number_day + " "+ number_month+ " "+ number_year;
            
            if (date_debut === null) {
                date_debut = date_box_compar;
                var box_actives = container_child.findAll('.box-day.active-selected');
                if (box_actives !== null && box_actives.length > 0) {
                    box_actives.removeClass("active-selected");
                }
                this.addClass("active-selected");
                
                date_fin = null;
            }
            
            if (range === true) {
                var diff_dates = diffDates(date_box_compar, date_debut);
                var number_days = diff_dates.number_days;
                if (!diff_dates.result) {
                    date_debut = date_box_compar;
                }
                if (date_debut !== null &&  diffDates(date_box_compar, date_debut).result) {
                    date_fin = date_box_compar;
                }
                if (date_fin !== null && date_debut !== date_box_compar && diffDates(date_fin, date_box_compar) && date_fin !== date_box_compar) {
                    //date_debut = date_box_compar;
                }

                if (date_fin !== null && date_debut !== null) {
                    activeChoices(date_debut, date_fin, number_days);
                    displayDate(date_debut, date_fin);
                }
            }
            else {
                date_debut = date_box_compar;
                var box_actives = container_child.findAll('.box-day.active-selected');
                if (box_actives !== null && box_actives.length > 0) {
                    box_actives.removeClass("active-selected");
                }
                this.addClass("active-selected");
                date_fin = date_debut;
                if (date_fin !== null && date_debut !== null) {
                    //activeChoices(date_debut, date_fin, number_days);
                    displayDate(date_debut, date_fin);
                }
            }
            
            
            return true;
        }, false);
        element.findAll('.box-day-active').on("dblclick", function() {
            var number_day = this.attr("data-day");
            var number_month = this.attr("data-month");
            var number_year = this.attr("data-year");
            
            var date_box = getDateFormat(number_day, number_month, number_year);
            var date_box_compar = number_day + " "+ number_month+ " "+ number_year;
            date_debut = date_box_compar;
            var box_actives = container_child.findAll('.box-day.active-selected');
            if (box_actives !== null && box_actives.length > 0) {
                box_actives.removeClass("active-selected");
            }
            
            this.addClass("active-selected");
            date_fin = date_debut;
            if (date_fin !== null && date_debut !== null) {
                activeChoices(date_debut, date_fin, 0);
                displayDate(date_debut, date_fin);
            }
            
        }, false);
    }
    
    function formatDateDisplay(date) {
        var result_date = "";
        var split_date = date.split(" ");
        var year = split_date[2];
        var month = parseInt(split_date[1])+1;
        var day = split_date[0];
        var zero_day = "";
        var zero_month = "";
        if (parseInt(day) < 10 && day.toString().length === 1) {
            zero_day = "0";
        }
        if (parseInt(month) < 10 && month.toString().length === 1) {
            zero_month = "0";
        }
        result_date = year+"-"+zero_month+month+"-"+zero_day+day;
        return result_date;
    }
    
    function displayDate(date_debut, date_fin) {
        
        
        var days_actives = element.findAll(".active-selected");
                
        if (days_actives.length === 1) {

            date_fin = date_debut;
        }
            
        result_calendar.start = formatDateDisplay(date_debut);
        result_calendar.end = formatDateDisplay(date_fin);
        var range_choice = element.find('.range-choice');
        range_choice.addClass("active");
        var li_range_choice = range_choice.findAll("li");
        date_debut = dateFormat(date_debut);
        date_fin = dateFormat(date_fin);
        result_calendar.start_text = date_debut;
        result_calendar.end_text = date_fin;
        li_range_choice.eq(0).text(date_debut);
        li_range_choice.eq(1).text(date_fin);
        var split_init_date = params.init_date.split(", ");
        if (split_init_date.length > 1 && typeof params.afterInit === "function" && params.afterInit !== null) {
            params.afterInit.call(this, date_debut, date_fin);
        }
    }
    function activeChoices(date_debut, date_fin, number_days) {
        var box_actives = container_child.findAll('.box-day.active-selected');
        if (box_actives !== null && box_actives.length > 0) {
            box_actives.removeClass("active-selected");
        }
        number_days = Math.abs(number_days);
        var split_date_debut = date_debut.split(" ");
        //var split_date_fin = date_fin.split(" ");
        var zero_day = "";
        var zero_month = "";
        if (params.supportZero) {
            if (parseInt(split_date_debut[0]) < 10 && split_date_debut[0].toString().length === 1) {
                zero_day = "0";
            }

            if (parseInt(split_date_debut[1]) < 10 && parseInt(split_date_debut[1]) > 0 && split_date_debut[1].toString().length === 1) {
                zero_month = "0";
            }
        }
        
        
        var selector_date_debut = '.day-'+zero_day+split_date_debut[0]+"-"+zero_month+split_date_debut[1]+"-"+split_date_debut[2];
        var element_date_debut = element.find(selector_date_debut);
        if (element_date_debut !== null) {
            var index_date_debut = element_date_debut.index(".box-day-active", container_child);
            var box_indexs = container_child.findAll(".box-day-active");
            var number_all_days = index_date_debut + number_days+1;
            for (var i = index_date_debut; i < number_all_days; i++ ) {
                var element_day = box_indexs.eq(i);
                element_day.addClass("active-selected");
                var days_actives = element.findAll(".active-selected");
                
                if (days_actives.length === 1) {
                    
                    date_fin = null;
                }

            }
        }
        
        
    }                                   
    function diffDates(date1, date2) {
        var result = true;
        var number_days = 0;
        if (date1 === null) {
            return false;
        }
        if (date2 === null) {
            return true;
        }
        
        var split_date1 = date1.split(" ");
        var split_date2 = date2.split(" ");
        
        var day1 = parseInt(split_date1[0]);
        var month1 = parseInt(split_date1[1]);
        var year1 = parseInt(split_date1[2]);
        
        var day2 = parseInt(split_date2[0]);
        var month2 = parseInt(split_date2[1]);
        var year2 = parseInt(split_date2[2]);
        
        var date_format1 =  new Date(year1, month1, day1);
        var date_format2 =  new Date(year2, month2, day2);
        number_days =  Math.round((date_format1-date_format2)/(1000*60*60*24));
        if (year2 > year1) {
            result = false;
            return { result : result, number_days : number_days };
        }
        if (year2 === year1 && month2 > month1) {
            result = false;
            return { result : result, number_days : number_days };
        }
        
        if (year2 === year1 && month2 === month1 && day2 > day1) {
            result = false;
            return { result : result, number_days : number_days };
        }
        if (year2 === year1 && month2 === month1 && day2 === day1) {
            result = false;
            return { result : result, number_days : number_days };
        } 
        
        return { result : result, number_days : number_days };
    }
    function getDateFormat(day, month, year) {
        day = getNameDay(day);
        month = getNameMonth(month);
        return day+" "+ month+ " "+ year;
    }
    function dateFormat(date) {
        var split_date = date.split(" ");
        var day = split_date[0];
        var month = split_date[1];
        var year = split_date[2];
        month = getNameMonth(month);
        return day+" "+ month+ " "+ year;
    }
    
    var month_header = dom.get(".months-calendar");
    function findInArray(array, value) {
        var status = false;
        var l = array.length;
        for (var i = 0; i < l; i++) {
            var temp_value = array[i];
            if (value === temp_value) {
                status = true;
                i = l;
            }
        }
        return status;
    } 
    function renderMonth(month, year, callback, prepend, classes) {
        classes = classes || "";
        nbr_months +=1;
        var weeks = month.month;
        var day_column;
       
        if (typeof prepend !== "undefined" && prepend === true) {
            day_column = container_child.prependTo('<div class="day-column left"></div>');
        }
        else {
            day_column = container_child.appendTo('<div class="day-column left"></div>');
        }
        var days_week = null;
        for (var w = 0; w < weeks.length; w++ ) {
            var week_div = day_column.appendTo('<div class="week"></div>');
            var ul_days = week_div.appendTo('<ul class="horizontal"></ul>');
            var week = weeks[w].week;
            for (var d = 0;d < weeks[w].week.length; d++) {
                days_week = week[d];
                var class_no_empty = "box-day-active";
                if (days_week === "") {
                    class_no_empty = "";
                }
                var zero_day = "";
                var zero_month = "";
                if (params.supportZero) {
                    if (days_week < 10  && day.toString().length === 1) {
                        zero_day = "0";
                    }

                    if (month.month_number < 10 && month.month_number > 0  && month.month_number.toString().length === 1 ) {
                        zero_month = "0";
                    }
                }
                
                var class_day = 'day-'+zero_day+days_week+'-'+zero_month+month.month_number+'-'+month.year;
                ul_days.appendTo('<li class="box-day '+class_no_empty+' day-'+zero_day+days_week+' '+class_day+'" data-month="'+month.month_number+'" data-year="'+month.year+'" data-day="'+days_week+'">'+days_week+'</li>');
            }
            
        }
        
        var clr_exist = container_child.find(".clr");
        if (clr_exist === null) {
            //container_child.appendTo('<div class="clr"></div>');
        }
        var months_calendar_ul = element.find(".months-calendar ul");
        slider_months_calendar.css({ "width" : width_slide*nbr_months});
        container_child.css({ "width" : width_slide*nbr_months });
        var li_month;
        if (typeof prepend !== "undefined" && prepend === true) {
            li_month = months_calendar_ul.prependTo("<li>"+month.name+" "+month.year+"</li>");
        }
        else {
            li_month = months_calendar_ul.appendTo("<li>"+month.name+" "+month.year+"</li>");
        }
        if (typeof callback === "function") {
            callback.call(this, days_week, day_column, li_month);
        }
        runChoice(); 
    }
    function createMonth(month, start, year) {
        var bissextile =  getBissextile(year);
        
        var total_month = getTotalDaysMonth(month, bissextile);
        var nbr_week = Math.ceil(total_month / 7)+1;
        var weeks = [];
        var diff_start = 7 - start;
        var day_number_fin_month = 0;
        var index_weeks = 0;
        for (var w = 0; w < nbr_week; w++) {
            var data_week = [];
            if (w === 0) {
                for (var j = 0; j < diff_start; j++) {
                    data_week.push(j+1);
                }
                var week = createWeek(start,data_week);
                if (week !== null) {
                    weeks.push(week);
                }
                
            }
            else {
                var w_ = w+1;
                var numbers_week = (7*w)+diff_start;
                var start_numbers_week = numbers_week - 7;
                if (numbers_week < total_month+7)  {
                    //index_weeks += 1;
                    for (var b = start_numbers_week; b < numbers_week; b++) {
                        if (b <= total_month-1 ) {
                            data_week.push(b+1);
                        }
                    }
                    var week_ = createWeek(0,data_week);
                    if (week_ !== null) {
                        weeks.push(week_);
                    }
                }   
            }
        }
        index_weeks = weeks.length-1;
        if (index_weeks > -1) {
            day_number_fin_month = weeks[index_weeks].day_fin;
            return { year : year, month :  weeks, day_fin : day_number_fin_month, month_number : month, name : getNameMonth(month)};
        }
        
        
    }
    
    function getNameDay(n) {
        var name = "";
        n = parseInt(n);
        switch(n) {
            case 0 :
                name = "Monday";
                if (params.lang === "fr") {
                    name = "Lundi";
                }
                if (params.lang === "ar") {
                    name = "الإثنين";
                }
            break;
            case 1:
                name = "Tuesday";
                if (params.lang === "fr") {
                    name = "Mardi";
                }
                if (params.lang === "ar") {
                    name = "الثلاثاء";
                }
            break;
            case 2:
                name = "Wednesday";
                if (params.lang === "fr") {
                    name = "Mercredi";
                }
                if (params.lang === "ar") {
                    name = "الأربعاء";
                }
            break;
            case 3:
                name = "Thursday";
                if (params.lang === "fr") {
                    name = "Jeudi";
                }
                if (params.lang === "ar") {
                    name = "الخميس";
                }
            break;
            case 4:
                name = "Friday";
                if (params.lang === "fr") {
                    name = "Vendredi";
                }
                if (params.lang === "ar") {
                    name = "الجمعة";
                }
            break;
            case 5:
                name = "Saturday";
                if (params.lang === "fr") {
                    name = "Samedi";
                }
                if (params.lang === "ar") {
                    name = "السبت";
                }
            break;
            case 6:
                name = "Sunday";
                if (params.lang === "fr") {
                    name = "Dimanche";
                }
                if (params.lang === "ar") {
                    name = "الأحد";
                }
            break;
        }
        return name;
    }
    function getNameMonth(n) {
        var name = "";
        n = parseInt(n);
        switch(n) {
            case 0 :
                name = "January";
                if (params.lang === "fr") {
                    name = "Janvier";
                }
                if (params.lang === "ar") {
                    name = "يناير";
                }
            break;
            case 1:
                name = "February";
                if (params.lang === "fr") {
                    name = "Février";
                }
                if (params.lang === "ar") {
                    name = "فبراير";
                }
            break;
            case 2:
                name = "March";
                if (params.lang === "fr") {
                    name = "mars";
                }
                if (params.lang === "ar") {
                    name = "مارس";
                }
            break;
            case 3:
                name = "April";
                if (params.lang === "fr") {
                    name = "Avril";
                }
                if (params.lang === "ar") {
                    name = "أبريل";
                }
            break;
            case 4:
                name = "May";
                if (params.lang === "fr") {
                    name = "Mai";
                }
                if (params.lang === "ar") {
                    name = "مايو";
                }
            break;
            case 5:
                name = "June";
                if (params.lang === "fr") {
                    name = "Juin";
                }
                if (params.lang === "ar") {
                    name = "يونيو";
                }
            break;
            case 6:
                name = "July";
                if (params.lang === "fr") {
                    name = "Juillet";
                }
                if (params.lang === "ar") {
                    name = "يوليوز";
                }
            break;
            case 7:
                name = "August";
                if (params.lang === "fr") {
                    name = "Août";
                }
                if (params.lang === "ar") {
                    name = "غشت";
                }
            break;
            case 8:
                name = "September";
                if (params.lang === "fr") {
                    name = "Septembre";
                }
                if (params.lang === "ar") {
                    name = "سبتمبر";
                }
            break;
            case 9:
                name = "October";
                if (params.lang === "fr") {
                    name = "Octobre";
                }
                if (params.lang === "ar") {
                    name = "أكتوبر";
                }
            break;
            case 10:
                name = "November";
                if (params.lang === "fr") {
                    name = "Novembre";
                }
                if (params.lang === "ar") {
                    name = "نونبر";
                }
            break;
            case 11:
                name = "December";
                if (params.lang === "fr") {
                    name = "Décembre";
                }
                if (params.lang === "ar") {
                    name = "ديسمبر";
                }
            break;
        }
        return name;
    }
    function createWeek(start, data) {
        if (data.length > 0) {
            var week = [];
            var index = 0;
            var day_number_fin_week = 0;
            for (var i = 0; i < 7; i++) {
                if (i < start) {
                    week.push("");
                }
                else {
                    var data_day = data[index];
                    if (typeof data_day !== "undefined") {
                        day_number_fin_week = index;
                        week.push(data_day);
                    }
                    index++;
                }
            }
            return {week : week, day_fin : day_number_fin_week};
        }
        else {
            return null;
        }
        
    }
    function getStartMonth(month, day_number, day_name) {
        for (var i = day_number; i > 0; i--) {
            if (day_name > 0) {
                day_name -=1;
            }
            if (day_name === 0) {
                day_name = 7;
            }
        }
        return day_name;
    }
    function getStartMonthPrev(month, day_number, bissextile) {
        day_number = day_number+1;
        var total_days = getTotalDaysMonth(month, bissextile);
        var first_week = true;
        var day_name = 0;
        for (var i = 0; i < total_days+1; i++) {
            if (first_week) {
                if (i === day_number-1) {
                    day_name = 0;
                    first_week = false;
                }
            }
            else {
                if (day_name === 0) {
                    day_name = 6;
                }
                else {
                    day_name -=1;
                }
            }
        }
        return day_name;
    }
    function getTotalDaysMonth(month, bissextile) {
        var total = 0;
        switch(month) {
            case 0:
                total = 31;
            break;
            case 1:
                total = 28;
                if (bissextile) {
                    total = 29;
                }
            break;
            case 2:
                total = 31;
            break;
            case 3:
                total = 30;
            break;
            case 4:
                total = 31;
            break;
            case 5:
                total = 30;
            break;
            case 6:
                total = 31;
            break;
            case 7:
                total = 31;
            break;
            case 8:
                total = 30;
            break;
            case 9:
                total = 31;
            break;
            case 10:
                total = 30;
            break;
            case 11:
                total = 31;
            break;
            case 12:
                total = 31;
            break;
        }
        return total;
    }
    function getBissextile(year) {
        var year_debut = 1972;
        var bissextile = false;
        if (year%2 === 0) {
            var diff_years = year - year_debut;
            if (year > year_debut && diff_years%4 === 0) {
                bissextile = true;
            }   
        }
        return bissextile;
    }
}); 