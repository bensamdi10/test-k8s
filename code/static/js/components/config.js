var Config = {
    
    add : function(key, value) {
        this[key] = value;
    },
    get : function(key) {
        return this[key];
    },
    set : function(key, value) {
        this[key] = value;
    },
    remove : function(key) {
        delete this[key];
    }
}
