var restify = require('restify'),
    fs = require('fs'),
    config = require('./configure');


var server = restify.createServer({
    certificate: fs.readFileSync('./cert/cert.pem'),
    key: fs.readFileSync('./cert/key.pem'),
    name: 'Ritzy',
});

server = config(server);

server.listen(9000, function() {
    console.log('%s listening at %s', server.name, server.url);
});
