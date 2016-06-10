(function () {
  'use strict';

  angular
    .module('tech2016.controllers')
    .controller('NavBarController', NavBarController);

  NavBarController.$inject = ['$scope', 'Authentication'];

  function NavBarController($scope, Authentication) {
    var vm = this;

    init();

    function init() {
      vm.username = Authentication.getAuthenticatedAccount().username;
    }

    vm.logout = function() {
      Authentication.logout();
    }
  }
})();
