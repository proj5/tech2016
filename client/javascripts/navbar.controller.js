(function () {
  'use strict';

  angular
    .module('tech2016.controllers')
    .controller('NavBarController', NavBarController);

  NavBarController.$inject = ['$scope', 'Authentication', '$http'];

  function NavBarController($scope, Authentication, $http) {
    var vm = this;

    init();

    function init() {
      vm.username = Authentication.getAuthenticatedAccount().username;
      // http://localhost:8000/api/v1/accounts/admin/
      var userURL = "api/v1/accounts/" + vm.username + "/";
      $http.get(userURL)
      .then(function successCallback(response) {
          vm.user = response.data;
        },
        function errorCallback(response) {
          console.log("Error when get User")
        });
    }

    vm.logout = function() {
      Authentication.logout();
    }
  }
})();
