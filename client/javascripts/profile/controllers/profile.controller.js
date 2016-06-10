(function () {
  'use strict';
  angular
    .module('tech2016.profile.controllers')
    .controller('ProfileController', ProfileController);

  ProfileController.$inject = ['$scope', '$state', '$http', 'fileUpload', 'Authentication'];

  function ProfileController($scope, $state, $http, fileUpload, Authentication) {
    var vm = this;

    init();
    getUserProfile();
    getAvatar();

    function init() {
      vm.username = Authentication.getAuthenticatedAccount().username;
    }

    function getUserProfile() {
      var url = "api/v1/accounts/" + vm.username;
      $http.get(url)
        .then(function successCallback(response) {
          vm.user = response.data;
        }, function errorCallback(response) {
          console.error("Failed to get user profile");
        })
    }

    function getAvatar() {
      var url = "api/v1/account/avatar/" + vm.username + "/";
      $http.get(url)
        .then(function successCallback(response) {
          vm.avatar = response.data;
        }, function errorCallback(response) {
          console.error("Failed to get avatar");
        })
    }

    vm.uploadAvatar = function() {
      var url = "api/v1/account/avatar/";
      fileUpload.uploadFileToUrl(file, url);
      $state.reload();
    }
  }
})();