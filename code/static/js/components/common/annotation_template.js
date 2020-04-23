import invock, {Component} from "invock-js";

class AnnotationTemplate extends Component {
    
    
    constructor(params) {
        super(params);
        this.events = {
            "click .remove-item-annotation" : "removeItem"
        }
    }
    
    
    removeItem(evt, self) {
        var parent = this.closests(".inline-annotation-item");
        if ( parent !== null ) {
            parent.animate(0.5, { "opacity" : 0, onComplete : function() {parent.remove(); } });
        }
    }
    
    render() {
        return `<div class="div-p half-p top20 inline-annotation-item inline-block-item">
                    <span class="block absolute remove-item remove-item-annotation pointer fade-hover"></span>
                    <p>
                        <label>Annotation </label>
                        <select name="annotation_name_{{props.count|default:}}" data-rule="string" data-value="">
                            <option value="">Select Container</option>   
                            <option value="nginx.ingress.kubernetes.io/app-root">app-root (String)</option>
                            <option value="nginx.ingress.kubernetes.io/ssl-redirect">SSl-redirect ("true" or "false")</option>
                            <option value="nginx.ingress.kubernetes.io/force-ssl-redirect">Force-SSl-redirect ("true" or "false")</option>
                            <option value="nginx.ingress.kubernetes.io/from-to-www-redirect">Force-to-www-redirect ("true" or "false")</option>
                            <option value="nginx.ingress.kubernetes.io/http2-push-preload">http2-push-preload ("true" or "false")</option>
                            <option value="nginx.ingress.kubernetes.io/rewrite-target">Rewrite-target(String)</option>
                            <option value="certmanager.k8s.io/cluster-issuer">Cluster Issuer(String)</option>
                            <option value="nginx.ingress.kubernetes.io/client-body-buffer-size">Client-body-buffer-size (String)</option>
                            <option value="nginx.ingress.kubernetes.io/proxy-body-size">Proxy-body-size (String)</option>
                            <option value="nginx.ingress.kubernetes.io/proxy-read-timeout">Proxy-Read-Timeout</option>
                            <option value="ginx.ingress.kubernetes.io/proxy-send-timeout">Proxy-Send-Timeout</option>
                            <option value="nginx.ingress.kubernetes.io/force-ssl-redirect">Force-SSl-redirect ("true" or "false")</option>
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
                    <input type="text" name="annotation_value_{{props.count|default:}}" placeholder="Example : /home?(.*)" class="" data-rule="string" />
                </p>

                <div class="clr"></div>

            </div>`;
    }
}

invock.export("AnnotationTemplate", AnnotationTemplate);