'use strict';

var Models = require('../models'),
    contants = require('../contants');

Array.prototype.contains = function(element) {
    return this.indexOf(element) > -1;
};

// auth policy  here:
// true if req does have permissions
// (check here permissions and roles
//  allowed to access the REST action depending
//  on the URI being accessed)

function reqHasPermission(req) {
    // decode req.accessToken, extract
    // supposed fields there: userId:roleId:expiryTime
    // and check them
    console.log(contants.CATEGORIES);
    if (req.headers.authorization != contants.auth || !contants.CATEGORIES.contains(req.params.category)) {
        return false;
    }
    return true;
} // ()

module.exports = {
    category: function(req, res, next) {

        if (!reqHasPermission(req)) {
            console.log('failed auth');
            res.writeHead(401); // unauthorized
            res.end();
            return; // don't call next()
        } else {
            switch (req.params.category) {
                case 'all':
                    Models.Pingo.find({}, function(err, products) {
                        if (err) throw err;
                        if (products.length > 1) {
                            // object of all the users
                            console.log(products.length);
                            res.send(200, JSON.stringify(products));
                            next();
                        } else {
                            res.writeHead(204); // unauthorized
                            res.end();
                        }

                    });
                    break;
                default:
                    Models.Pingo.find({
                        subcat: req.params.category
                    }, function(err, products) {
                        if (err) throw err;
                        if (products.length > 1) {
                            // object of all the users
                            //  console.log(products.length);
                            res.send(200, JSON.stringify(products));
                            next();
                        } else {
                            res.writeHead(204); // unauthorized
                            res.end();
                        }

                    });
                    break;
            }
        }
    }
};
