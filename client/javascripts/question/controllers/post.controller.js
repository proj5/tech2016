(function () {
  'use strict';

  angular
    .module('tech2016.question.controllers')
    .controller('PostController', PostController);

    PostController.$inject = ['$scope', '$state', '$http', '$stateParams', 'ngDialog'];

    function PostController($scope, $state, $http, $stateParams, ngDialog) {
      var vm = this;            

      vm.submitComment = function(post) {
        var postAnswerURL = "api/v1/comment/id=" + post.id + '/';
        $http.post(postAnswerURL, {
          "content": vm.commentContent
        })
        .then(function successCallback(response) {
          //$state.reload();
          post.comments.push(response.data);
        },
        function errorCallback(response) {
          console.log("Error when submit comment");
        });
      }

      vm.upvotePost = function(post) {
        console.log(post);
        var upvoteURL = "api/v1/vote/?postID=" + post.id;
        $http.post(upvoteURL, {
          "score" : 1
        })
        .then(function successCallback(response) {
          //$state.reload();
          post.total_vote = response.data.total_vote;
          post.myScore = response.data.my_vote;
        },
        function errorCallback(response) {
          console.log("Error when upvote a post");
        });
      }
	  
     
    }
})();
