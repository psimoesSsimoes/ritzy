'use strict'

var MongoDB = require('mongodb')
    .Db;
var Server = require('mongodb')
    .Server;
var moment = require('moment');

var dbPort = 27017;
var dbHost = 'localhost';
var dbName = 'ritzy';
var db = new MongoDB(dbName, new Server(dbHost, dbPort, {
    auto_reconnect: true
}), {
    w: 1
});
db.open(function(e, d) {
    if (e) {
        console.log(e);
    } else {
        console.log('connected to database :: ' + dbName);
    }
});
var DB = {};
var recipes = db.collection('recipes');
var accounts = db.collection('accounts');
DB.recipes = recipes;
DB.accounts = accounts;
module.exports = DB;
