(function () {
  'use strict';

  angular
    .module('tech2016.question.controllers')
    .controller('QuestionController', QuestionController);

    QuestionController.$inject = ['$scope', '$state', '$http', '$stateParams'];

    function QuestionController($scope, $state, $http, $stateParams) {
      var vm = this;
      vm.questionID = $stateParams.questionID;
      getQuestion();
      getTopics();
      getAnswers();

      function getQuestion() {
        //http://localhost:8000/api/v1/question/?questionID=1
        var url = "api/v1/question/?questionID=" + vm.questionID;
        $http.get(url)
        .then(function successCallback(response){
            vm.question = response.data;
        }, function errorCallback(response) {
            console.log("Error get question");
        });
      }

      function getTopics() {
        //http://localhost:8000/api/v1/question/topic/?questionID=1
        var url = "api/v1/question/topic/?questionID=" + vm.questionID;
        $http.get(url)
        .then(function successCallback(response){
            vm.topics = response.data;
        }, function errorCallback(response) {
            console.log("Error get topics");
        });
      }

      function getAnswers() {
        //http://localhost:8000/api/v1/answers/?questionID=1
        var url = "api/v1/answers/?questionID=" + vm.questionID;
        $http.get(url)
        .then(function successCallback(response){
            vm.answers = response.data;
        }, function errorCallback(response) {
            console.log("Error get topics");
        });
      }
    }
})();
