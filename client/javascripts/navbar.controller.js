(function () {
  'use strict';

  angular
    .module('tech2016.controllers')
    .controller('NavBarController', NavBarController);

  NavBarController.$inject = ['$scope', '$state', 'Authentication', '$window', '$http', 'ngDialog', '$pusher'];

  function NavBarController($scope, $state, Authentication, $window, $http, ngDialog, $pusher) {
    var vm = this;

    vm.openQuestionForm = openQuestionForm;
    vm.submitQuestion = submitQuestion;

    init();

    function init() {
      name = $state.current.name;
      if (name == "newsfeed") {
        document.getElementById("navbar-homepage").className = "active";
      } else if (name == "notification") {
        document.getElementById("navbar-notification").className = "active";
      }
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

      var client = new Pusher('df818e2c5c3828256440');
      var pusher = $pusher(client);

      var channel = pusher.subscribe('notification_' + vm.username);
      channel.bind('new_noti', function(data) {
        vm.user = data
      })

    }

    vm.logout = function() {
      Authentication.logout();
    }

    function openQuestionForm() {
      ngDialog.open({
        template: 'client/templates/AddQuestion.html',
        className: 'ngdialog-theme-default',
        controller: 'NavBarController',
        controllerAs: 'vm'
      });
    }

    function submitQuestion() {
      var postQuestionURL = "api/v1/question/";
      $http.post(postQuestionURL, {
        "question": vm.questionTitle,
        "content": vm.questionContent,
        "topics": ""
      })
      .then(function createQuestionSuccessFn(data, status, headers, config) {
        var url = '/question/' + parseInt(data.data);
        $window.location.href = url;
      },
      function createQuestionErrorFn(response) {
      });
    }
  }
})();
