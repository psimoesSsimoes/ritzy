var bodyParser = require('body-parser'),
    restify = require('restify'),
    router = require('./routes');

module.exports = function(server) {
    router(server);
    server.use(bodyParser.urlencoded({
        'extended': true
    }));
    server.use(bodyParser.json());
    server.use(restify.bodyParser());
    return server;
}
