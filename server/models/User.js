'use strict'

var mongoose = require('mongoose'),
    Schema = mongoose.Schema;
// email will be the key of our database
var User_Schema = new Schema({
    name: {
        type: String
    },
    email: {
        type: String
    },
    password: {
        type: String
    }
});

module.exports = mongoose.model('user', User_Schema, 'users')
