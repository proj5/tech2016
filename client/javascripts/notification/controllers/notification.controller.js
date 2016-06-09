(function () {
  'use strict';

  angular
    .module('tech2016.notification.controllers')
    .controller('NotificationController', NotificationController);

    NotificationController.$inject = ['$scope', '$state', '$http', '$stateParams'];

    function NotificationController($scope, $state, $http, $stateParams) {
      var vm = this;
      // vm.numofNoti = $stateParams.numberOfNoti;
      vm.numofNoti = 20;
      getNotifications();

      function getNotifications() {
        // http://localhost:8000/api/v1/notifications/?count=2
        var url = "api/v1/notifications/?count=" + vm.numofNoti;
        $http.get(url)
        .then(function successCallback(response) {
          vm.notis = response.data;
          vm.notis.forEach(function(noti) {
            noti.content = getContent(noti.notification);
            console.log(noti);
          });
        },
        function errorCallback(response) {
          console.log("Error when get notification")
        });
      }

      function getContent(obj) {
        var result = "";
        if (obj.type === "USER comments on your QUESTION/ANSWER") {
          result = " commented on your " + obj.post.type + " to: ";
        } else if (obj.type === "USER upvotes/downvotes ANSWER  ") {
          result = " upvoted your " + obj.post.type + " to: ";
        } else if (obj.type === "USER answers followed QUESTION") {
          result = "  answered followed question: "
        }
        return result;
      }
    }
})();
