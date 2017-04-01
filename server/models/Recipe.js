'use strict'

var mongoose = require('mongoose'),
    Schema = mongoose.Schema;


// email will be the key of our database
var Recipe_Schema = new Schema({
    category: {
        type: String
    },
    name: {
        type: String
    },
    img: {
        type: String
    },
    ingr: {
        type: String
    },
    prep: {
        type: String
    }

});

module.exports = mongoose.model('recipe', Recipe_Schema, 'recipes');
