dom.addPlugin("getEase", function(params) {
    var name = params.name, suffix = params.suffix, duration = params.duration;
    var ease_object = {};
    var transition = suffix+"transition";
    var transition_timing = suffix+"transition-timing-function";
    switch (name) {
        case "easeIn":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.420, 0.000, 1.000, 1.000)";
            ease_object[transition_timing] = "cubic-bezier(0.420, 0.000, 1.000, 1.000)";
        break;
        case "easeOut":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.000, 0.000, 0.580, 1.000)";
            ease_object[transition_timing] = "cubic-bezier(0.000, 0.000, 0.580, 1.000)";
        break;
        case "easeInOut":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.420, 0.000, 0.580, 1.000)";
            ease_object[transition_timing] = "cubic-bezier(0.420, 0.000, 0.580, 1.000)";
        break;
        case "easeInQuad":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.550, 0.085, 0.680, 0.530)";
            ease_object[transition_timing] = "cubic-bezier(0.550, 0.085, 0.680, 0.530)";
        break;
        case "easeInCubic":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.550, 0.055, 0.675, 0.190)";
            ease_object[transition_timing] = "cubic-bezier(0.550, 0.055, 0.675, 0.190)";
        break;
        case "easeInQuart":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.895, 0.030, 0.685, 0.220)";
            ease_object[transition_timing] = "cubic-bezier(0.895, 0.030, 0.685, 0.220)";
        break;
        case "easeInQuint":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.755, 0.050, 0.855, 0.060)";
            ease_object[transition_timing] = "cubic-bezier(0.755, 0.050, 0.855, 0.060)";
        break;
        case "easeInSine":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.470, 0.000, 0.745, 0.715)";
            ease_object[transition_timing] = "cubic-bezier(0.470, 0.000, 0.745, 0.715)";
        break;
        case "easeInExpo":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.950, 0.050, 0.795, 0.035)";
            ease_object[transition_timing] = "cubic-bezier(0.950, 0.050, 0.795, 0.035)";
        break;
        case "easeInCirc":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.600, 0.040, 0.980, 0.335)";
            ease_object[transition_timing] = "cubic-bezier(0.600, 0.040, 0.980, 0.335)";
        break;
        case "easeInBack":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.600, -0.280, 0.735, 0.045)";
            ease_object[transition_timing] = "cubic-bezier(0.600, -0.280, 0.735, 0.045)";
        break;
        case "easeOutQuad":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.250, 0.460, 0.450, 0.940)";
            ease_object[transition_timing] = "cubic-bezier(0.250, 0.460, 0.450, 0.940)";
        break;
        case "easeOutCubic":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.215, 0.610, 0.355, 1.000)";
            ease_object[transition_timing] = "cubic-bezier(0.215, 0.610, 0.355, 1.000)";
        break;
        case "easeOutQuart":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.165, 0.840, 0.440, 1.000)";
            ease_object[transition_timing] = "cubic-bezier(0.165, 0.840, 0.440, 1.000)";
        break;
        case "easeOutQuint":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.230, 1.000, 0.320, 1.000)";
            ease_object[transition_timing] = "cubic-bezier(0.230, 1.000, 0.320, 1.000)";
        break;
        case "easeOutSine":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.390, 0.575, 0.565, 1.000)";
            ease_object[transition_timing] = "cubic-bezier(0.390, 0.575, 0.565, 1.000)";
        break;
        case "easeOutExpo":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.190, 1.000, 0.220, 1.000)";
            ease_object[transition_timing] = "cubic-bezier(0.190, 1.000, 0.220, 1.000)";
        break;
        case "easeOutCirc":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.075, 0.820, 0.165, 1.000)";
            ease_object[transition_timing] = "cubic-bezier(0.075, 0.820, 0.165, 1.000)";
        break;
        case "easeOutBack":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.175, 0.885, 0.320, 1.275)";
            ease_object[transition_timing] = "cubic-bezier(0.175, 0.885, 0.320, 1.275)";
        break;
        case "easeInOutQuad":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.455, 0.030, 0.515, 0.955)";
            ease_object[transition_timing] = "cubic-bezier(0.455, 0.030, 0.515, 0.955)";
        break;
        case "easeInOutCubic":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.645, 0.045, 0.355, 1.000)";
            ease_object[transition_timing] = "cubic-bezier(0.645, 0.045, 0.355, 1.000)";
        break;
        case "easeInOutQuart":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.770, 0.000, 0.175, 1.000)";
            ease_object[transition_timing] = "cubic-bezier(0.770, 0.000, 0.175, 1.000)";
        break;
        case "easeInOutQuint":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.860, 0.000, 0.070, 1.000)";
            ease_object[transition_timing] = "cubic-bezier(0.860, 0.000, 0.070, 1.000)";
        break;
        case "easeInOutSine":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.445, 0.050, 0.550, 0.950)";
            ease_object[transition_timing] = "cubic-bezier(0.445, 0.050, 0.550, 0.950)";
        break;
        case "easeInOutExpo":
            ease_object[transition] =  "all "+duration+" cubic-bezier(1.000, 0.000, 0.000, 1.000)";
            ease_object[transition_timing] = "cubic-bezier(1.000, 0.000, 0.000, 1.000)";
        break;
        case "easeInOutCirc":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.785, 0.135, 0.150, 0.860)";
            ease_object[transition_timing] = "cubic-bezier(0.785, 0.135, 0.150, 0.860)";
        break;
        case "easeInOutBack":
            ease_object[transition] =  "all "+duration+" cubic-bezier(0.680, -0.550, 0.265, 1.550)";
            ease_object[transition_timing] = "cubic-bezier(0.680, -0.550, 0.265, 1.550)";
        break;
    }
    return ease_object;
});
dom.easeInfo = {
    easeIn : ["easeIn", "easeInOut", "easeInQuad", "easeOutCubic", "easeInQuart", "easeInQuint", "easeInSine", "easeInExpo", "easeInCirc", "easeInBack"],
    easeOut : ["easeOut", "easeOutQuad", "easeOutCubic", "easeOutQuart", "easeOutQuint", "easeOutSine", "easeOutExpo", "easeOutCirc", "easeOutBack"],
    easeInOut : ["easeInOut", "easeInOutQuad", "easeInOutCubic", "easeInOutQuart", "easeInOutQuint", "easeInOutSine", "easeInOutExpo", "easeInOutCirc", "easeInOutBack"]
};