(function () {
  'use strict';

  angular
    .module('tech2016.controllers')
    .controller('NavBarController', NavBarController);

  NavBarController.$inject = ['$scope', 'Authentication', '$window', '$http', 'ngDialog'];

  function NavBarController($scope, Authentication, $window, $http, ngDialog) {
    var vm = this;

    vm.openQuestionForm = openQuestionForm;
    vm.submitQuestion = submitQuestion;

    init();

    function init() {
      vm.username = Authentication.getAuthenticatedAccount().username;
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