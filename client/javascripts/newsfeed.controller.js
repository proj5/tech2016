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
      /* Not work
      window.onload = function() {
        document.getElementById("navbar-homepage").setClass('active');
      }
      */
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
          length = vm.questions.length;
          for (var i = 0; i < length; i++) {
            promises.push(
              $http.get("api/v1/vote/?postID=" + vm.questions[i].answer.id)
                .then(function successCallback(response) {
                  votes.push(response.data);
                }, function errorCallback(response) {
                })
            )
          }
        }, function errorCallback(response) {
          console.error("Failed to get questions");
        })
      );
      $q.all(ajax).then(function() {
        $q.all(promises).then(function() {
          for (var i = 0; i < vm.questions.length; i++) {
            vm.questions[i].answer.my_vote = votes[i];
          }
        })
      });
    }

    vm.upvote = function(answer) {
      var url = "api/v1/vote/?postID=" + answer.id;
      $http({
        method: 'POST',
        url: url,
        data: {
          'score': 1
        }
      }).then(function successCallback(response) {
        $state.reload();
      }, function errorCallback(response) {
        console.error("Failed to upvote answer");
      })
    }

    vm.downvote = function(answer) {
      var url = "api/v1/vote/?postID=" + answer.id;
      $http({
        method: 'POST',
        url: url,
        data: {
          'score': -1
        }
      }).then(function successCallback(response) {
        $state.reload();
      }, function errorCallback(response) {
        console.error("Failed to downvote answer");
      })
    }
  }

})();