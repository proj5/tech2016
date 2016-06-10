(function () {
  'use strict';
  angular
    .module('tech2016.controllers')
    .controller('ProfileController', ProfileController);

  ProfileController.$inject = ['$scope', 'Authentication'];

  function ProfileController($scope, Authentication) {
    var vm = this;

    init();

    function init() {
      vm.user = Authentication.getAuthenticatedAccount();
    }
  }
})();