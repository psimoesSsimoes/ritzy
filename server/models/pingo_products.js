'use strict';

var mongoose = require('mongoose'),
    Schema = mongoose.Schema;

mongoose.connect('mongodb://localhost/pyramid');

var Pingo_Product_Schema = new Schema({
    name: {
        type: String
    },
    category: {
        type: String
    },
    img: {
        type: String
    },
    price: {
        type: String
    },
    promo: {
        type: String
    },
    subcat: {
        type: String
    }
});

module.exports = mongoose.model('pp', Pingo_Product_Schema, 'pingodoce'); // collection name
