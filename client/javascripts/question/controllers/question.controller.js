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
      vm.isDisplayAnswerBox = false;
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

      vm.submitComment = function(postID) {
        var postAnswerURL = "api/v1/comment/id=" + postID + '/';
        $http.post(postAnswerURL, {
          "content": vm.commentContent[postID]
        })
        .then(function successCallback(response) {
          $state.reload();
        },
        function errorCallback(response) {
          console.log("Error when submit comment");
        });
      }

      vm.upvotePost = function(postID) {
        var upvoteURL = "api/v1/vote/?postID=" + postID;
        $http.post(upvoteURL, {
          "score" : 1
        })
        .then(function successCallback(response) {
          $state.reload();
        },
        function errorCallback(response) {
          console.log("Error when upvote a post");
        });
      }

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
              var voteStatusURL = "/api/v1/vote/?postID=" + vm.questionID;
              $http.get(voteStatusURL)
              .then(function successCallback(response) {
                vm.question.myScore = response.data;
              },
              function errorCallback(response) {});
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
                var voteStatusURL = "/api/v1/vote/?postID=" + answer.id;
                $http.get(voteStatusURL)
                .then(function successCallback(response) {
                  answer.myScore = response.data;
                },
                function errorCallback(response) {});
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
