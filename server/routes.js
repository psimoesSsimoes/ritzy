var pingo = require('./controllers/pingo'),
    accounts = require('./controllers/accounts'),
    recipes = require('./controllers/recipes');
//  continente = require('../controllers/continente'),
//  all = require('../controllers/all');

module.exports = function(server) {
    //get by categories
    //server.get('/pingo/:category', pingo.category);
    //server.get('/continente/:category', continente.category);
    //server.get('/all/:category', continente.category);
    // get by keyword of product
    // server.get('/pingo/:product', pingo.category);
    // server.get('/continente/:product', continente.category);
    // server.get('/all/:product', continente.category);
    // // get List of recipes by category
    // server.get('/recipes/:category', recipes.category);
    // //given recipe get ingredients
    // server.get('/recipes_products/:recipe', recipes_products.ingredients);
    // //given recipe return prep
    // server.get('/recipes/:recipe/prep');
    server.post('/account/register', accounts.register);
    server.post('/account/login/', accounts.login);
    server.get('/recipes/all', recipes.all);
    server.post('/recipes/category', recipes.category)
    // server.post('/account/:id/shopping_list');
    // server.get('/account/:id/shopping_list');
    // server.post('/account/:id/shopping_list/:product/inc');
    // server.post('/account/:id/shopping_list/:product/dec');


};
