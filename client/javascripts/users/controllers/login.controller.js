(function () {
  'use strict';

  angular
    .module('tech2016.users.controllers')
    .controller('LoginController', LoginController);

  LoginController.$inject = ['$location', '$scope', 'Authentication'];

  /**
  * @namespace LoginController
  */
  function LoginController($location, $scope, Authentication) {
    var vm = this;

    vm.login = login;
    vm.resetField = resetField;

    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    */
    function activate() {
      // If the user is authenticated, they should not be here.
      if (Authentication.isAuthenticated()) {
        $state.go('newsfeed');
      }
    }

    /**
    * @name login
    * @desc Log the user in
    */
    function login() {
      Authentication.login(vm.username, vm.password);
    }

    function resetField() {
      vm.username = "";
      vm.password = "";
    }
  }
})();
