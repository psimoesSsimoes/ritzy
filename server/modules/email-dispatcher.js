var ES = require('./email-settings');
var EM = {};
module.exports = EM;

EM.server = require("emailjs/email")
    .server.connect({

        host: ES.host,
        user: ES.user,
        password: ES.password,
        ssl: true

    });

EM.dispatchConfirmationRegistry = function(req, callback) {
    EM.server.send({
        from: ES.sender,
        to: req.body.email,
        subject: 'Ritzy Account Created!',
        text: "atum",
        attachment: EM.composeEmailRegistry(req)
    }, callback);
}


EM.dispatchResetPasswordLink = function(account, callback) {
    EM.server.send({
        from: ES.sender,
        to: account.email,
        subject: 'Password Reset',
        text: 'something went wrong... :(',
        attachment: EM.composeEmail(account)
    }, callback);
}

function getIPAddress() {
    var interfaces = require('os')
        .networkInterfaces();
    for (var devName in interfaces) {
        var iface = interfaces[devName];

        for (var i = 0; i < iface.length; i++) {
            var alias = iface[i];
            if (alias.family === 'IPv4' && alias.address !== '127.0.0.1' && !alias.internal)
                return alias.address;
        }
    }

    return '0.0.0.0';
}

EM.composeEmailRegistry = function(o) {
    var link = 'http://' + getIPAddress() + ':8080/reset-password?e=' + o.email + '&p=' + o.pass;
    var html = "<html><body>";
    html += "Hi " + o.body.name + ",<br><br>";
    html += "Thanks for registering into Ritzy. Your user is <strong>" + o.body.user + "</strong> and your pass is <strong>" + o.body.pass + "</strong></b><br><br>";
    html += "<a href='" + link + "'>Please click here to reset your password</a><br><br>";
    html += "Cheers,<br>";
    html += "";
    html += "</body></html>";
    return [{
        data: html,
        alternative: true
    }];
}


EM.composeEmail = function(o) {
    var link = 'http://' + getIPAddress() + ':8080/reset-password?e=' + o.email + '&p=' + o.pass;
    var html = "<html><body>";
    html += "Hi " + o.name + ",<br><br>";
    html += "Someone, hopefully you, has requested to reset the password for your C2netHubAccount.  If you did not perform this request, you can safely ignore this email. Otherwise, click the link below to complete the process. </b><br><br>";
    html += "<a href='" + link + "'>Please click here to reset your password</a><br><br>";
    html += "Cheers,<br>";
    html += "";
    html += "</body></html>";
    return [{
        data: html,
        alternative: true
    }];
}
