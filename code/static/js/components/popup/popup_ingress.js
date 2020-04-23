export default function PopupIngress() {
    return `
            <div class="overlay overlay-popup"></div>
            <div class="container-popup">
                <div class="popup relative center-auto border shadow">
                    <div class="bleu-violet box15 uppercase relative">
                        <h3 class="bold">Config Ingress Service</h3>
                        <div class="close-popup absolute pointer fade-hover action-popup" data-action="close"></div>
                    </div>
                    <div class="content-popup">
                        <div class="tabs-ui bleu-violet-tabs uppercase" id="container-pagination"></div>
                        <div class="clr"></div>

                        <div class="" id="container-form">
                            <form class="form-popup relative">
                                <div class="relative hidden">
                                    <div class="relative slider-form-container">
                                        <div class="slide-form left">
                                            <div class="inputs box30">
                                                <div class="container-inputs">
                                                    <p>
                                                        <label>Domain Name <span class="asterix">*</span></label>
                                                        <input type="text" name="domain" placeholder="Example : example.com" class="required" data-rule="string" value="{{props.data.domain|default:}}" />
                                                    </p>

                                                    <div class="relative top20">
                                                        Accept TLS : 

                                                        <div class="switcher {{props.data.accept_tls_active}} right" data-value="accept_tls" data-yes="Yes" data-no="No">
                                                               <div class="handler animate"></div>
                                                               <div class="text-handler animate">{{props.data.accept_tls_label}}</div>
                                                               <input type="hidden" name="accept_tls" value="{{props.data.accept_tls}}" />
                                                        </div>

                                                        <div class="clr"></div>

                                                    </div>

                                                    <div class=" relative bottom20 top20">
                                                        Accept SSL : 

                                                        <div class="switcher {{props.data.accept_ssl_active}} right" data-value="accept_ssl" data-yes="Yes" data-no="No">
                                                               <div class="handler animate"></div>
                                                               <div class="text-handler animate">{{props.data.accept_ssl_label}}</div>
                                                               <input type="hidden" name="accept_ssl" value="{{props.data.accept_ssl}}" />
                                                        </div>

                                                        <div class="clr"></div>

                                                    </div>



                                                    <p>
                                                        <span class="asterix">*</span> <span>: Mandatory Field</span>
                                                    </p>
                                                </div>

                                                <div class="align-center top30 bottom15">
                                                    <input type="button" value="Close" class="fonce action-popup" data-action="close" />
                                                    <input type="button" value="Next" class="bleu-violet bleu-violet-shadow next-slide" data-index="1" />

                                                </div>
                                            </div>
                                        </div>
                                        

                                        <div class="slide-form left">
                                            <div class="inputs box30">
                                                <div class="container-inputs">
                                                    <div id="container-annotations">
                                                        <div id="" class="relative subs-container">
                                                            {% for annot in props.data.annotations %}
                                                                <div class="div-p relative half-p top20 inline-annotation-item inline-block-item">
                                                                    <span class="block absolute remove-item remove-item-command pointer fade-hover"></span>
                                                                    <p>
                                                                        <label>Annotation </label>
                                                                        <select name="annotation_name_{{annot.loop_counter|default:}}" data-rule="string" data-value="{{annot.annotation_name|default:}}">
                                                                            <option value="">Select Container</option>   
                                                                                <option value="nginx.ingress.kubernetes.io/app-root">app-root (String)</option>
                                                                                <option value="nginx.ingress.kubernetes.io/ssl-redirect">SSl-redirect ("true" or "false")</option>
                                                                                <option value="nginx.ingress.kubernetes.io/force-ssl-redirect">Force-SSl-redirect ("true" or "false")</option><option value="nginx.ingress.kubernetes.io/proxy-read-timeout">Proxy-Read-Timeout</option>
                                                                                <option value="nginx.ingress.kubernetes.io/force-ssl-redirect">Force-SSl-redirect ("true" or "false")</option><option value="ginx.ingress.kubernetes.io/proxy-send-timeout">Proxy-Send-Timeout</option>
                                                                                <option value="nginx.ingress.kubernetes.io/from-to-www-redirect">Force-to-www-redirect ("true" or "false")</option>
                                                                                <option value="nginx.ingress.kubernetes.io/http2-push-preload">http2-push-preload ("true" or "false")</option>
                                                                                <option value="nginx.ingress.kubernetes.io/rewrite-target">Rewrite-target(String)</option>
                                                                                <option value="certmanager.k8s.io/cluster-issuer">Cluster Issuer(String)</option>

                                                                                <option value="nginx.ingress.kubernetes.io/client-body-buffer-size">Client-body-buffer-size (String)</option>
                                                                                <option value="nginx.ingress.kubernetes.io/proxy-body-size">Proxy-body-size (String)</option>
                                                                                <option value="nginx.ingress.kubernetes.io/configuration-snippet">Configuration-snippet (String)</option>
                                                                                <option value="nginx.ingress.kubernetes.io/configuration-snippet">Configuration-snippet (String)</option>
                                                                                <option value="nginx.ingress.kubernetes.io/enable-cors">Enable-cors ("true" or "false")</option>
                                                                                <option value="nginx.ingress.kubernetes.io/cors-allow-origin">Cors-allow-origin (String)</option>
                                                                                <option value="nginx.ingress.kubernetes.io/cors-allow-methods">Cors-allow-methodes (String)</option>
                                                                                <option value="nginx.ingress.kubernetes.io/cors-allow-credentials">Cors-allow-credentials ("true" or "false")</option>
                                                                                <option value="nginx.ingress.kubernetes.io/cors-max-age">Cors-max-age (Number)</option>
                                                                                <option value="nginx.ingress.kubernetes.io/cors-max-age">Cors-max-age (Number)</option>
                                                                                <option value="nginx.ingress.kubernetes.io/limit-connections">Limit-connections (Number)</option>
                                                                                <option value="nginx.ingress.kubernetes.io/permanent-redirect">Permanent-redirect (String)</option>
                                                                                <option value="nginx.ingress.kubernetes.io/permanent-redirect-code">Permanent-redirect-code (Number)</option>
                                                                                <option value="nginx.ingress.kubernetes.io/temporal-redirect">temporal-redirect (String)</option>
                                                                                <option value="nginx.ingress.kubernetes.io/load-balance">Load-balance (String)</option>
                                                                        </select>
                                                                    </p>

                                                                    <p>
                                                                        <label>Value of Annotation </label>
                                                                        <input type="text" name="annotation_value_{{annot.loop_counter|default:}}" placeholder="Example : /home?(.*)" class="" data-rule="string" value="{{annot.annotation_value|default:}}" />
                                                                    </p>

                                                                    <div class="clr"></div>

                                                                </div>
                                                            {% endfor %}
                                                        </div>
                                                        <div class="align-center top30">
                                                            <input type="button" value="Add New Annotation" data-action="add_annotation_ingress" class="bleu-web bleu-web-shadow action-popup" />
                                                        </div>
                                                        </div>



                                                        <p>
                                                            <span class="asterix">*</span> <span>: Mandatory Field</span>
                                                        </p>
                                                </div>

                                                <div class="align-center top30 bottom15">
                                                    <input type="button" value="Back" class="fonce back-slide"/>
                                                    <input type="button" value="Next" class="bleu-violet bleu-violet-shadow next-slide" data-index="2" />
                                                </div>
                                            </div>
                                        </div>


                                        <div class="slide-form left">
                                            <div class="inputs box30">
                                                <div class="container-inputs">
                                                    <div id="container-containers">
                                                        <div id="" class="relative subs-container">
                                                            {% for container in props.data.path %}
                                                                <div class="div-p relative third-p top20 inline-container-item inline-block-item">
                                                                    <span class="block absolute remove-item pointer fade-hover"></span>
                                                                    <p>
                                                                        <label>Cluster Ip Service </label>
                                                                        <select name="container_name_{{container.loop_counter|default:}}" data-rule="string" data-value="{{container.container_name|default:}}" data-index='{{container.loop_counter}}'>
                                                                            <option value="">Select Cluster Ip Service</option>
                                                                            {% for cluster in props.data.clusters %}
                                                                                <option value="{{cluster.slug}}">{{cluster.name}}</option>
                                                                            {% endfor %}

                                                                        </select>
                                                                    </p>

                                                                    <p>
                                                                        <label>Path </label>
                                                                        <input type="text" name="container_path_{{container.loop_counter|default:}}" placeholder="Example : /home?(.*)" class="" data-rule="string" value="{{container.container_path|default:}}" />
                                                                    </p>

                                                                    <p>
                                                                        <label>Port </label>
                                                                        <input type="text" name="container_port_{{container.loop_counter|default:}}" placeholder="Example : 3000" class="" data-rule="number" value="{{container.container_port|default:}}" />
                                                                    </p>

                                                                    <div class="clr"></div>

                                                                </div>
                                                            {% endfor %}
                                                        </div>
                                                        <div class="align-center top30">
                                                            <input type="button" value="Add New Container" data-action="add_container_ingress" class="bleu-web bleu-web-shadow action-popup" />
                                                        </div>
                                                        </div>



                                                        <p>
                                                            <span class="asterix">*</span> <span>: Mandatory Field</span>
                                                        </p>
                                                </div>

                                                <div class="align-center top30 bottom15">
                                                    <input type="button" value="Back" class="fonce back-slide"/>
                                                    <input type="button" value="Save" class="green green-shadow finish-slide" data-index="3" />
                                                </div>
                                            </div>
                                        </div>
                                        <div class="clr"></div>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
    `;
}