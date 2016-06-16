(function () {
  'use strict';

  angular
    .module('tech2016.controllers')
    .controller('NewsFeedController', NewsFeedController);

  NewsFeedController.$inject = ['$scope', '$state', '$q', '$http', 'Authentication'];

  function NewsFeedController($scope, $state, $q, $http, Authentication) {
    var vm = this;
    vm.questions = [];

    function init() {
      window.onload = function() {
        document.getElementById("navbar-homepage").setClass('active');
      }
      //vm.username = Authentication.getAuthenticatedAccount().username;
    }
  }    
})();
