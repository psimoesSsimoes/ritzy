var restify = require('restify'),
    router = require('./routes');

module.exports = function(server) {

    server.use(restify.bodyParser());
    router(server);

    return server;
}
