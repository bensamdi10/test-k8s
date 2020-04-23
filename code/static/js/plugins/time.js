import drop_down from "./drop-down";

dom.addPlugin("time", function(params) {
	var element = initHTML();
	params = params || {};
    
    var parent = this.getParent();
    var width_slide = 500;
    var align = params.align || "left";
    var name_space = params.name_space || "time-picker";
    params.name_space = name_space;
    var doc = document.documentElement;
    var scroll_value = doc.scrollTop;
    
    if (typeof params.supportZero === "undefined") {
        params.supportZero = true;
    }
    
    var hours = { name : "", label : "" };
    var minutes = { name : "", label : "" };
    
    /* var type_range = element.find(".type-range");
    type_range.findAll("li").on("click", function() {
       var type = this.attr("data-value");
       result_calendar.type = type;
       type_range.find(".active").removeClass("active");
       this.addClass("active");
    });*/
    
    
    var action_time = element.find(".action-time");
    action_time.findAll("input").on("click", function() {
        var value = this.attr("data-value");
        if (value === "apply") {
            if (typeof params.afterApply === "function") {
                params.afterApply.call(this, hours, minutes);
                
                var li_picker = dom.get(".ul-date-picker-time").findAll("li");
                if (li_picker.length > 1) {
                    li_picker.eq(0).text(hours.label);
                    li_picker.eq(1).text(minutes.label);
                }
                
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
    
    function initHTML() {
        var html_code =  `
                <div id="time-details" class="center-auto top20">
                    <div class="bottom10">
                        <div class="center-auto">
                            <div class="time-column left">
                                <label class="block bottom10">Heures</label>
                                <div id="drop-down-hours" class="calcul-dropdown drop-down-composant" data-value="full-day" data-type="operator">
                                    <div class="value-dropdown relative animate">
                                    <div class="absolute arrow-absolute"><img src="/static/images/icons/arrow_widget_views.png" alt=""></div>
                                    <div class="operation-option" data-value="full-day" data-view="full-day">Toute la journée</div></div>
                                    <div class="list-dropdown">

                                        <div class="operation-option relative" data-id="00" data-value="00">
                                            <ul class="horizontal">
                                                <li>00 / 00 AM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="01">
                                            <ul class="horizontal">
                                                <li>01 / 01 AM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>
                                        <div class="operation-option relative" data-id="01" data-value="02">
                                            <ul class="horizontal">
                                                <li>02 / 02 AM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="03">
                                            <ul class="horizontal">
                                                <li>03 / 03 AM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="04">
                                            <ul class="horizontal">
                                                <li>04 / 04 AM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="05">
                                            <ul class="horizontal">
                                                <li>05 / 05 AM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="06">
                                            <ul class="horizontal">
                                                <li>06 / 06 AM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="07">
                                            <ul class="horizontal">
                                                <li>07 / 07 AM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="08">
                                            <ul class="horizontal">
                                                <li>08 / 08 AM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="09">
                                            <ul class="horizontal">
                                                <li>09 / 09 AM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="10">
                                            <ul class="horizontal">
                                                <li>10 / 10 AM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="11">
                                            <ul class="horizontal">
                                                <li>11 / 11 AM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="12">
                                            <ul class="horizontal">
                                                <li>12 / 12 AM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="13">
                                            <ul class="horizontal">
                                                <li>13 / 01 PM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="14">
                                            <ul class="horizontal">
                                                <li>14 / 02 PM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="15">
                                            <ul class="horizontal">
                                                <li>15 / 03 PM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="16">
                                            <ul class="horizontal">
                                                <li>16 / 04 PM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="17">
                                            <ul class="horizontal">
                                                <li>17 / 05 PM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="18">
                                            <ul class="horizontal">
                                                <li>18 / 06 PM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="19">
                                            <ul class="horizontal">
                                                <li>19 / 07 PM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="20">
                                            <ul class="horizontal">
                                                <li>20 / 08 PM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="21">
                                            <ul class="horizontal">
                                                <li>21 / 09 PM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="22">
                                            <ul class="horizontal">
                                                <li>22 / 10 PM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>

                                        <div class="operation-option relative" data-id="01" data-value="23">
                                            <ul class="horizontal">
                                                <li>23 / 11 PM</li>
                                                <li class="check-view right"></li>
                                            </ul>
                                            <div class="clr"></div>
                                        </div>




                                    </div>
                                </div>
                            </div>

                         <div class="time-column left">
                              <label class="block bottom10">Minutes</label>
                              <div id="drop-down-minutes" class="calcul-dropdown drop-down-composant" data-value="full-day" data-type="operator">
                                        <div class="value-dropdown relative animate">
                                        <div class="absolute arrow-absolute"><img src="/static/images/icons/arrow_widget_views.png" alt=""></div>
                                        <div class="operation-option" data-value="full-day" data-view="full-day">Toute la journée</div></div>
                                        <div class="list-dropdown">

                                            <div class="operation-option relative" data-id="00" data-value="00">
                                                <ul class="horizontal">
                                                    <li>00 Minute</li>
                                                    <li class="check-view right"></li>
                                                </ul>
                                                <div class="clr"></div>
                                            </div>
                                            <div class="operation-option relative" data-id="10" data-value="10">
                                                <ul class="horizontal">
                                                    <li>10 Minutes</li>
                                                    <li class="check-view right"></li>
                                                </ul>
                                                <div class="clr"></div>
                                            </div>

                                            <div class="operation-option relative" data-id="15" data-value="15">
                                                <ul class="horizontal">
                                                    <li>15 Minutes</li>
                                                    <li class="check-view right"></li>
                                                </ul>
                                                <div class="clr"></div>
                                            </div>

                                            <div class="operation-option relative" data-id="20" data-value="20">
                                                <ul class="horizontal">
                                                    <li>20 Minutes</li>
                                                    <li class="check-view right"></li>
                                                </ul>
                                                <div class="clr"></div>
                                            </div>

                                            <div class="operation-option relative" data-id="25" data-value="25">
                                                <ul class="horizontal">
                                                    <li>25 Minutes</li>
                                                    <li class="check-view right"></li>
                                                </ul>
                                                <div class="clr"></div>
                                            </div>

                                            <div class="operation-option relative" data-id="30" data-value="30">
                                                <ul class="horizontal">
                                                    <li>30 Minutes</li>
                                                    <li class="check-view right"></li>
                                                </ul>
                                                <div class="clr"></div>
                                            </div>

                                            <div class="operation-option relative" data-id="35" data-value="35">
                                                <ul class="horizontal">
                                                    <li>35 Minutes</li>
                                                    <li class="check-view right"></li>
                                                </ul>
                                                <div class="clr"></div>
                                            </div>

                                            <div class="operation-option relative" data-id="40" data-value="40">
                                                <ul class="horizontal">
                                                    <li>40 Minutes</li>
                                                    <li class="check-view right"></li>
                                                </ul>
                                                <div class="clr"></div>
                                            </div>

                                            <div class="operation-option relative" data-id="45" data-value="45">
                                                <ul class="horizontal">
                                                    <li>45 Minutes</li>
                                                    <li class="check-view right"></li>
                                                </ul>
                                                <div class="clr"></div>
                                            </div>

                                            <div class="operation-option relative" data-id="50" data-value="50">
                                                <ul class="horizontal">
                                                    <li>50 Minutes</li>
                                                    <li class="check-view right"></li>
                                                </ul>
                                                <div class="clr"></div>
                                            </div>

                                            <div class="operation-option relative" data-id="55" data-value="55">
                                                <ul class="horizontal">
                                                    <li>55 Minutes</li>
                                                    <li class="check-view right"></li>
                                                </ul>
                                                <div class="clr"></div>
                                            </div>


                                        </div>
                                    </div>
                          </div>
                        </div>
                        <div class="clr"></div>
                    </div>
                    
                </div>
                
        `;
        
        var btns_calendar = '<div class="action-time top40 align-center bottom20">'+
                    '<input type="button" value="Apply" class="violet-date violet-date-shadow action-calendar" data-value="apply" />'+
                    '<input type="button" value="Cancel" class="gris-tabs action-calendar black-color" data-value="cancel" />'+
                '</div>';
        
        if (typeof params.lang !== "undefined" ) {
            if (params.lang === "fr") {
                btns_calendar = '<div class="action-time top20 align-center bottom10">'+
                    '<input type="button" value="Appliquer" class="violet-date violet-date-shadow action-calendar" data-value="apply" />'+
                    '<input type="button" value="Fermer" class="gris-tabs action-calendar black-color" data-value="cancel" />'+
                '</div>';
            }
            
        }
        
        
        var container_time_parent = dom.get("#time-"+params.name_space);
    
        if (container_time_parent !== null) {
            container_time_parent.remove();
        }
        
         html_code = html_code+btns_calendar;

        var body = dom.get("body");
        var style_scroll = "";
        if (params.scroll === false) {
            style_scroll = "position : fixed;"
        }
        var calendar_container_html = '<div id="time-'+params.name_space+'" class="absolute shadow white box15 time-container" style="'+style_scroll+'"></div>';
        var container = body.appendTo(calendar_container_html);
        container.html(html_code);

        runDropsTime();

        return container;
            
        
        
       
    }
    
    function runDropsTime() {
      var dropdown_hours = dom.get("#drop-down-hours");
      if (dropdown_hours !== null) {
        var dropdown_plugin = dropdown_hours.runPlugin("dropdown", {
            after : function(value, prev, text) {
                hours = { name : value, label : text };
            }
        });
      }
        
      var dropdown_minutes = dom.get("#drop-down-minutes");
      if (dropdown_minutes !== null) {
        var dropdown_plugin = dropdown_minutes.runPlugin("dropdown", {
            after : function(value, prev, text) {
                minutes =  { name : value, label : text };
            }
        });
      }  
        
        
    }
    
    
}); 