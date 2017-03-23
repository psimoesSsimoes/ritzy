var bodyParser = require('body-parser'),
    router = require('./routes');

module.exports = function(server) {
    router(server);
    server.use(bodyParser.urlencoded({
        'extended': true
    }));
    server.use(bodyParser.json());
    return server;
}
