'use strict';

var Models = require('../models'),
    AM = require('./modules/account-manager'),
    EM = require('./modules/email-dispatcher'),
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
    register: function(req, res, next) {

        AM.addNewAccount({
            name: req.param('name'),
            email: req.param('email'),
            user: req.param('user'),
            pass: req.param('pass'),
            country: req.param('country')
        }, function(e) {
            if (e) {
                res.send(e, 400);
            } else {
                res.send('ok', 200);
                next;
            }
        });
        lost - password: function(req, res, next) {
            AM.getAccountByEmail(req.param('email'), function(o) {
                if (o) {
                    res.send('ok', 200);
                    EM.dispatchResetPasswordLink(o, function(e, m) {

                        if (!e) {

                        } else {
                            res.send('email-server-error', 400);
                            for (k in e) console.log('error : ', k, e[k]);
                        }
                    });
                } else {
                    res.send('email-not-found', 400);
                }
            });
        }


    }
};
