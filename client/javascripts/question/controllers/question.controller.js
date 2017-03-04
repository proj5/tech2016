(function () {
  'use strict';

  angular
    .module('tech2016.question.controllers')
    .controller('QuestionController', QuestionController);

    QuestionController.$inject = ['$scope', '$state', '$http', '$stateParams', 'ngDialog', 'PostService', 'TopicService'];

    function QuestionController($scope, $state, $http, $stateParams, ngDialog, PostService, TopicService) {
      var vm = this;
      vm.questionID = $stateParams.questionID;
      vm.totalUpvote = 0;
      vm.totalComment = 0;
      vm.isDisplayAnswerBox = false;
      vm.showEditBox = false;
      getQuestion();
      getTopics();
      getAnswers();

      vm.displayAnswerBox = function() {
        vm.isDisplayAnswerBox = !vm.isDisplayAnswerBox;
      }

      vm.submitAnswer = function() {
        //console.log(vm.answerContent);
        var postAnswerURL = "api/v1/answer/?questionID=" + vm.questionID;
        $http.post(postAnswerURL, {
          "content": vm.answerContent
        })
        .then(function successCallback(response) {
          $state.reload();
        },
        function errorCallback(response) {
          console.log("Error when submit answer");
        });
      }

      vm.toggleEditBox = function() {
        vm.showEditBox = !vm.showEditBox;
      }

      vm.getRelatedTopic = function(){
        TopicService.getRelatedTopic(vm.topicName, function callback(data){
            vm.relatedTopics = data;
        });
      }

      vm.submitTopic = function(){
        var url = "api/v1/question/topic/?questionID=" + vm.questionID;
        var createUrl = "api/v1/topic/"
        $http.post(url,  vm.topicName
        )
        .then(function addTopicSuccessFn(data, status, headers, config) {
          vm.topics.push(vm.topicName);
          vm.toggleEditBox();
        },
        function createQuestionErrorFn(response) {
          if (response.data.detail){
            var obj = {
              "name": vm.topicName,
              "description": ""
            }
            $http.post(createUrl, obj).then(
              function addTopicSuccess(data, status, headers, config){
                obj.id = data.data.id;
                $http.post(url,  obj).then(function succ(response){
                  vm.topics.push(obj);
                  vm.toggleEditBox();
                }, function fail(response) {

                });
              },
              function addTopicError(response) {

              }
            );
          }
        });
      }

      function updateTotalComment(post){
        vm.totalComment += post.comments.length;
      }

      function getQuestion() {
        //http://localhost:8000/api/v1/question/?questionID=1
        var url = "api/v1/question/?questionID=" + vm.questionID;
        $http.get(url)
        .then(function successCallback(response){
            vm.question = response.data;
            getRelatedQuestions();
            vm.totalUpvote += vm.question.post.total_vote;

            PostService.getMyVote(vm.question.post);
            PostService.getComments(vm.question.post, updateTotalComment);
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
              PostService.getComments(answer, updateTotalComment);
              PostService.getMyVote(answer);
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
