'use strict';

var Models = require('../models'),
    contants = require('../contants');




module.exports = {
    category: function(req, res, next) {
        switch (req.params.category) {
            case 'pingo':
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
