'use strict'
var Models = require('../models'),
    RM = require('../modules/recipe-manager'),
    UT = require('../models/utils');

//ugly, rewrite later
var categories = ['']




module.exports = {
    all: function(req, res, next) {

    },
    category: function(req, res, next) {
        if (!allowedCategories(req.body.category))
            res.send("wrong category", 400);
    }
}
