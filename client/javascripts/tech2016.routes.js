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
      views: {
        '': {
          templateUrl: 'client/templates/NewsFeed.html',
          controller: 'NewsFeedController',
          controllerAs: 'vm'
        },
        'nav-bar@newsfeed': {
          templateUrl: 'client/templates/NavBar.html',
          controller: 'NavBarController',
          controllerAs: 'vm'
        }
      }
    })
    .state('question', {
      url: '/question/:questionID',
      views: {
        '': {
          templateUrl: 'client/templates/Question.html',
          controller: 'QuestionController',
          controllerAs: 'vm'
        },
        'nav-bar@question': {
          templateUrl: 'client/templates/NavBar.html',
          controller: 'NavBarController',
          controllerAs: 'vm'
        }
      }
    })
    .state('notification', {
      url: '/notification',
      views: {
        '': {
          templateUrl: 'client/templates/Notifications.html',
          controller: 'NotificationController',
          controllerAs: 'vm'
        },
        'nav-bar@notification': {
          templateUrl: 'client/templates/NavBar.html',
          controller: 'NavBarController',
          controllerAs: 'vm'
        }
      }
    })
    .state('profile', {
      url: '/profile',
      views: {
        '': {
          templateUrl: 'client/templates/Profile.html',
          controller: 'ProfileController',
          controllerAs: 'vm'
        },
        'nav-bar@profile': {
          templateUrl: 'client/templates/NavBar.html',
          controller: 'NavBarController',
          controllerAs: 'vm'
        }
      }
    });
  }
})();
