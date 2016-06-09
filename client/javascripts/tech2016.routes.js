(function () {
  'use strict';

  angular
  .module('tech2016.routes')
  .config(config);

  config.$inject = ['$stateProvider', '$urlRouterProvider'];

  function config($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/');
    $stateProvider
    .state('home', {
      url: '/',
      templateUrl: '/templates/index.html',
      controller: 'MainController',
      controllerAs: 'vm'
    })
    .state('home.login', {
      url: '',
      templateUrl: '/client/templates/login.html',
      controller: 'LoginController',
      controllerAs: 'vm'
    })
    .state('home.register', {
      url: '',
      templateUrl: '/client/templates/register.html',
      controller: 'RegisterController',
      controllerAs: 'vm'
    })
    .state('newsfeed', {
      url: '/newsfeed',
      templateUrl: 'client/templates/NewsFeed.html'
    });
  }
})();