(function () {
  'use strict';

  angular
    .module('tech2016.users.controllers')
    .controller('RegisterController', RegisterController);

  RegisterController.$inject = ['$location', '$scope', 'Authentication'];

  /**
  * @namespace RegisterController
  */
  function RegisterController($location, $scope, Authentication) {
    var vm = this;

    vm.register = register;
    vm.resetField = resetField;

    /*
    * @name register
    * @desc Register a new user
    */
    function register() {
      Authentication.register(vm.username, vm.password, vm.confirmPassword, vm.email, vm.firstName, vm.lastName);
    }

    activate();

    /**
     * @name activate
     * @desc Actions to be performed when this controller is instantiated
     */
    function activate() {
      // If the user is authenticated, they should not be here.
      if (Authentication.isAuthenticated()) {
        $location.url('/');
      }
    }

    function resetField() {
      vm.username = "";
      vm.password = "";
      vm.confirmPassword = "";
      vm.email = "";
      vm.firstName = "";
      vm.lastName = "";
    }

  }
})();