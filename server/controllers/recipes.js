'use strict'
var Models = require('../models');

module.exports = {
    all: function(req, res, next) {
        Models.Recipe.findAll({}, function(err, products) {
            if (err) throw err;
            if (products.length > 1) {

                console.log(products.length);
                res.send(200, JSON.stringify(products));
                next();
            } else {
                res.writeHead(204); // unauthorized
                res.end();
            }
        });
    },
    category: function(req, res, next) {

        res.send(200, req.params.category);
    }
}
