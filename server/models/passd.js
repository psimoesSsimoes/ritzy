'use strict'
var rand = require("random-key");

module.exports gen = function() {
    return rand.generate(35);
}
