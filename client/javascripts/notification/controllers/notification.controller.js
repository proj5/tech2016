(function () {
  'use strict';

  angular
    .module('tech2016.notification.controllers')
    .controller('NotificationController', NotificationController);

    NotificationController.$inject = ['$scope', '$state', '$http', '$stateParams', 'Authentication', '$pusher'];

    function NotificationController($scope, $state, $http, $stateParams, Authentication, $pusher) {
      var vm = this;
      // vm.numofNoti = $stateParams.numberOfNoti;
      vm.numofNoti = 20;
      vm.getNotifications = getNotifications;

      vm.username = Authentication.getAuthenticatedAccount().username;
      console.log('Username:', vm.username);
      // http://localhost:8000/api/v1/accounts/admin/
      var userURL = "api/v1/accounts/" + vm.username + "/";
      $http.get(userURL)
      .then(function successCallback(response) {
          vm.user = response.data;
        },
        function errorCallback(response) {
          console.log("Error when get User")
        });

      var client = new Pusher('df818e2c5c3828256440');
      var pusher = $pusher(client);

      var channel = pusher.subscribe('notification_' + vm.username);
      channel.bind('new_noti', function(data) {
        vm.user = data
      })

      vm.redirectToQuestion = function(questionID, readID) {
        // Seen notification
        // api/v1/notifications/?readID=1
        var seenNotiUrl = "api/v1/notifications/?readID=" + readID;
        $http.put(seenNotiUrl)
        .then(function successCallback(response) {},
        function errorCallback(response) {});
        $state.go('question', {'questionID': questionID});
      }

      function getNotifications() {
        // http://localhost:8000/api/v1/notifications/?count=2

        var url = "api/v1/notifications/?count=" + vm.numofNoti;
        $http.get(url)
        .then(function successCallback(response) {
          vm.notis = response.data;
          vm.notis.forEach(function(noti) {
            noti.content = getContent(noti.notification);
          });
          vm.user.num_unread_notis = 0;
        },
        function errorCallback(response) {
          console.log("Error when get notification")
        });
      }

      function getContent(obj) {
        var result = "";
        if (obj.type === "USER comments on your QUESTION/ANSWER") {
          result = " commented on your " + obj.post.type + " to: ";
        } else if (obj.type === "USER upvotes/downvotes ANSWER") {
          result = " upvoted your " + obj.post.type + " to: ";
        } else if (obj.type === "USER answers followed QUESTION") {
          result = "  answered followed question: "
        }
        return result;
      }
    }
})();
