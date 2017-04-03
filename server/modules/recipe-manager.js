var crypto = require('crypto'),
    DB = require('./db_connector');


exports.getAllRecords = function(callback) {
    DB.recipes.find()
        .toArray(
            function(e, res) {
                if (e) callback(e)
                else callback(null, res)
            });
};
