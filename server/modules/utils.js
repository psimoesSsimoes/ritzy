'use strict'

var constants = require('../contants');

exports.bad_regist_fields = function(user) {
    return req.body.name == null || req.body.email == null || req.body.user == null || req.body.pass == null || req.body.country == null;
}
exports.allowedCategories = function(cat) {
    return constants.CATEGORIES.contains(cat);
}
