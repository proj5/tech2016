(function () {
  'use strict';

  angular
    .module('tech2016.main.controllers')
    .controller('MainController', MainController);

    MainController.$inject = ['$scope', '$state', 'Authentication'];

    function MainController($scope, $state, Authentication) {
      var vm = this;

      redirect();

      function redirect() {
        if (Authentication.isAuthenticated()) {
          event.preventDefault();
          $state.go('newsfeed');
        } else {
          $state.go('home.login');
        }
      }
    }
})();