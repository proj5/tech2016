(function () {
  'use strict';

  angular
    .module('tech2016.controllers')
    .controller('NewsFeedController', NewsFeedController);

  NewsFeedController.$inject = ['$scope', '$state', '$q', '$http', 'Authentication'];

  function NewsFeedController($scope, $state, $q, $http, Authentication) {
    var vm = this;
    vm.questions = [];
    init();
    getQuestions();


    function init() {
      window.onload = function() {
        document.getElementById("navbar-homepage").setClass('active');
      }
      //vm.username = Authentication.getAuthenticatedAccount().username;
    }

    function getQuestions() {
      var url = "api/v1/questions/newest/?startID=0&count=10";
      var promises = [];
      var votes = [];
      var ajax = [];
      ajax.push($http.get(url)
        .then(function successCallback(response) {
          vm.questions = response.data;
          vm.questions.forEach(function(question) {
            promises.push(
              $http.get("api/v1/vote/?postID=" + question.answer.id)
                .then(function successCallback(response) {
                  question.answer.myScore = response.data;
                }, function errorCallback(response) {
                  question.answer.myScore = 0;
                })
            )
          })
        }, function errorCallback(response) {
          console.error("Failed to get questions");
        })
      );
    }
  }

})();
