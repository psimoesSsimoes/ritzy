'use strict'
var Models = require('../models'),
    UT = require('../modules/utils'),
    DB = require('../modules/db_connector')

//ugly, rewrite later
var categories = ['']




module.exports = {
    all: function(req, res, next) {
        DB.recipes.find({}, {
                'name': 1,
                'img': 1,
                'url_recipe': 1
            })
            .toArray(function(err, all) {
                if (err) {
                    res.send('Internal server error', 500);
                } else {
                    console.log(all);
                    return res.send(all);
                }
            });
    },
    category: function(req, res, next) {
        //if (!allowedCategories(req.body.category))
        //  res.send("wrong category", 400);
    }
}
