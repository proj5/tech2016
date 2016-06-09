(function () {
  'use strict';

  angular
    .module('tech2016.notification.controllers')
    .controller('NotificationController', NotificationController);

    NotificationController.$inject = ['$scope', '$state', '$http', '$stateParams'];

    function NotificationController($scope, $state, $http, $stateParams) {
      var vm = this;
    }
})();
