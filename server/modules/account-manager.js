var crypto = require('crypto'),
    DB = require('./db_connector');

/* login validation methods */

exports.autoLogin = function(user, pass, callback) {
    DB.accounts.findOne({
        user: user
    }, function(e, o) {
        if (o) {
            o.pass == pass ? callback(o) : callback(null);
        } else {
            callback(null);
        }
    });
}

exports.manualLogin = function(email, pass, callback) {
    DB.accounts.findOne({
        email: email
    }, function(e, o) {
        if (o == null) {
            callback('email-not-found');
        } else {
            validatePassword(pass, o.pass, function(err, res) {
                if (res) {
                    callback(null, o);
                } else {
                    callback('invalid-password');
                }
            });
        }
    });
}

/* record insertion, update & deletion methods */

exports.addNewAccount = function(newData, callback) {
    DB.accounts.findOne({
        user: newData.user
    }, function(e, o) {
        if (o) {
            callback('username-taken');
        } else {
            DB.accounts.findOne({
                email: newData.email
            }, function(e, o) {
                if (o) {
                    callback('email-taken');
                } else {
                    saltAndHash(newData.pass, function(hash) {
                        newData.pass = hash;
                        // append date stamp when record was created //
                        newData.date = moment()
                            .format('MMMM Do YYYY, h:mm:ss a');
                        DB.accounts.insert(newData, {
                            safe: true
                        }, callback);
                    });
                }
            });
        }
    });
}

exports.updateAccount = function(newData, callback) {
    DB.accounts.findOne({
        user: newData.user
    }, function(e, o) {
        o.name = newData.name;
        o.email = newData.email;
        o.country = newData.country;
        if (newData.pass == '') {
            DB.accounts.save(o, {
                safe: true
            }, callback);
        } else {
            saltAndHash(newData.pass, function(hash) {
                o.pass = hash;
                DB.accounts.save(o, {
                    safe: true
                }, callback);
            });
        }
    });
}

exports.updatePassword = function(email, newPass, callback) {
    DB.accounts.findOne({
        email: email
    }, function(e, o) {
        if (e) {
            callback(e, null);
        } else {
            saltAndHash(newPass, function(hash) {
                o.pass = hash;
                DB.accounts.save(o, {
                    safe: true
                }, callback);
            });
        }
    });
}

/* account lookup methods */

exports.deleteAccount = function(id, callback) {
    DB.accounts.remove({
        _id: getObjectId(id)
    }, callback);
}

exports.getAccountByEmail = function(email, callback) {
    DB.accounts.findOne({
        email: email
    }, function(e, o) {
        callback(o);
    });
}

exports.validateResetLink = function(email, passHash, callback) {
    DB.accounts.find({
        $and: [{
            email: email,
            pass: passHash
        }]
    }, function(e, o) {
        callback(o ? 'ok' : null);
    });
}

exports.getAllRecords = function(callback) {
    DB.accounts.find()
        .toArray(
            function(e, res) {
                if (e) callback(e)
                else callback(null, res)
            });
};

exports.delAllRecords = function(callback) {
    DB.accounts.remove({}, callback); // reset DB.accounts collection for testing //
}

/* private encryption & validation methods */

var generateSalt = function() {
    var set = '0123456789abcdefghijklmnopqurstuvwxyzABCDEFGHIJKLMNOPQURSTUVWXYZ';
    var salt = '';
    for (var i = 0; i < 10; i++) {
        var p = Math.floor(Math.random() * set.length);
        salt += set[p];
    }
    return salt;
}

var md5 = function(str) {
    return crypto.createHash('md5')
        .update(str)
        .digest('hex');
}

var saltAndHash = function(pass, callback) {
    var salt = generateSalt();
    callback(salt + md5(pass + salt));
}

var validatePassword = function(plainPass, hashedPass, callback) {
    var salt = hashedPass.substr(0, 10);
    var validHash = salt + md5(plainPass + salt);
    callback(null, hashedPass === validHash);
}

/* auxiliary methods */

var getObjectId = function(id) {
    return DB.accounts.db.bson_serializer.ObjectID.createFromHexString(id)
}

var findById = function(id, callback) {
    DB.accounts.findOne({
            _id: getObjectId(id)
        },
        function(e, res) {
            if (e) callback(e)
            else callback(null, res)
        });
};


var findByMultipleFields = function(a, callback) {
    // this takes an array of name/val pairs to search against {fieldName : 'value'} //
    DB.accounts.find({
            $or: a
        })
        .toArray(
            function(e, results) {
                if (e) callback(e)
                else callback(null, results)
            });
}
