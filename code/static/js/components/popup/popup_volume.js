export default function PopupVolume() {
    return `
    <div class="overlay overlay-popup"></div>
    <div class="container-popup">
        <div class="popup relative center-auto border shadow">
            <div class="bleu-violet box15 uppercase relative">
                <h3 class="bold">Create New Volume</h3>
                <div class="close-popup absolute pointer fade-hover action-popup" data-action="close"></div>
            </div>
            <div class="content-popup">
                <div class="tabs-ui bleu-violet-tabs uppercase none" id="container-pagination"></div>
                <div class="clr"></div>

                <div class="" id="container-form">
                    <form class="form-popup relative">
                        <div class="relative hidden">
                            <div class="relative slider-form-container">
                                <div class="slide-form left">
                                    <div class="inputs box30">
                                        <div class="container-inputs">
                                            <p>
                                                <label>Name of Volume <span class="asterix">*</span></label>
                                                <input type="text" name="name" placeholder="Example : example.com" class="required" data-rule="string" value="{{props.data.name|default:}}" />
                                            </p>

                                            <p>
                                                <label>Access Mode <span class="asterix">*</span></label>
                                                <select name="access_mode" class="requried" data-rule="string" data-value="{{props.data.access_mode|default:}}">
                                                    <option value="">Select The Access Mode</option>
                                                    <option value="ReadWriteOnce">Read & Write Once</option>
                                                    <option value="ReadOnlyMany">Read Only Many</option>
                                                    <option value="ReadWriteMany">Read & Write Many</option>
                                                </select>
                                            </p>

                                            <p class="">
                                                <label>Storage </label>
                                                <input type="text" name="storage" placeholder="Example : 300Mi" class="required" data-rule="string" value="{{props.data.storage|default:}}" />
                                            </p>

                                            <p>
                                                <label>Volume Mode <span class="asterix">*</span></label>
                                                <select name="volume_mode" class="requried" data-rule="string" data-value="{{props.data.volume_mode|default:}}">
                                                    <option value="">Select The Volume Mode</option>
                                                    <option value="Filesystem">File System</option>
                                                    <option value="Blockdevice">Block Device</option>
                                                </select>
                                            </p>

                                            <p>
                                                <label>Mount Math </label>
                                                <input type="text" name="mount_path" placeholder="Example : /etc/data/media" class="" data-rule="string" value="{{props.data.mount_path|default:}}" />
                                            </p>

                                            <p>
                                                <label>Sub Math </label>
                                                <input type="text" name="sub_path" placeholder="Example : media" class="" data-rule="string" value="{{props.data.sub_path|default:}}" />
                                            </p>

                                            <p>
                                                <span class="asterix">*</span> <span>: Mandatory Field</span>
                                            </p>
                                        </div>

                                        <div class="align-center top30 bottom15">
                                            <input type="button" value="Close" class="fonce action-popup" data-action="close" />
                                            <input type="button" value="Validate" class="green green-shadow finish-slide" data-index="1" />

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