'use strict';

var Models = require('../models'),
    AM = require('../modules/account-manager'),
    EM = require('../modules/email-dispatcher'),
    UT = require('../models/utils');



module.exports = {
    register: function(req, res, next) {
        if (UT.bad_regist_fields(req))
            res.send('wrong req fields', 400);
        else {
            AM.addNewAccount({
                name: req.body.name,
                email: req.body.email,
                user: req.body.user,
                pass: req.body.pass,
                country: req.body.country
            }, function(e) {
                if (e) {
                    res.send(e, 400);
                } else {
                    EM.dispatchConfirmationRegistry(req);
                    res.send('ok', 200);
                    next;
                }
            });

        }
    },
    login: function(req, res, next) {
        if (req.body.email == null || req.body.pass == null)
            res.send('login failed', 400);
        else {
            AM.manualLogin(req.body.email, req.body.pass, function(e) {
                if (e) {
                    res.send(e, 400);
                } else {
                    res.send('ok', 200);
                }
            })
        }
    },
    lostpassword: function(req, res, next) {
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
};
