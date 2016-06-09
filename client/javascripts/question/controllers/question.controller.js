(function () {
  'use strict';

  angular
    .module('tech2016.question.controllers')
    .controller('QuestionController', QuestionController);

    QuestionController.$inject = ['$scope', '$state', '$http', '$stateParams'];

    function QuestionController($scope, $state, $http, $stateParams) {
      var vm = this;
      vm.questionID = $stateParams.questionID;
      vm.totalUpvote = 0;
      vm.totalComment = 0;
      getQuestion();
      getTopics();
      getAnswers();

      function getQuestion() {
        //http://localhost:8000/api/v1/question/?questionID=1
        var url = "api/v1/question/?questionID=" + vm.questionID;
        $http.get(url)
        .then(function successCallback(response){
            vm.question = response.data;
            getRelatedQuestions();
            vm.totalUpvote += vm.question.post.total_vote;
            var commentsURL = "/api/v1/comments/id=" + vm.question.post.id + "/"
            $http.get(commentsURL)
            .then(function successCallback(response){
              vm.question.comments = response.data;
              vm.totalComment += vm.question.comments.length;
            }, function errorCallback(response) {
              console.log("Error get comments for question");
            });

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
            vm.answers.forEach(function(answer) {
              vm.totalUpvote += answer.total_vote;
              var commentsURL = "/api/v1/comments/id=" + answer.id + "/"
              $http.get(commentsURL)
              .then(function successCallback(commentResponse){
                answer.comments = commentResponse.data;
                vm.totalComment += answer.comments.length;
              }, function errorCallback(response) {
                console.log("Error get comments for answer");
              });
            });
        }, function errorCallback(response) {
            console.log("Error get Answers");
        });
      }

      function getRelatedQuestions() {
        //http://localhost:8000/api/v1/answers/?questionID=1
        var url = "api/v1/questions/?keyword=" + vm.question.question;
        $http.get(url)
        .then(function successCallback(response){
            vm.relatedQuestions = response.data;
        }, function errorCallback(response) {
            console.log("Error get related question");
        });
      }
    }
})();
