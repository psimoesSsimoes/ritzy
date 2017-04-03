'use strict'

var constants = require('../contants');
var categories = constants.CATEGORIES;

exports.bad_regist_fields = function(user) {
    return req.body.name == null || req.body.email == null || req.body.user == null || req.body.pass == null || req.body.country == null;
}
exports.allowedCategories = function(cat) {
    console.log(categories);
    console.log(cat);
    return categories.indexOf(cat) >= 0;
}
