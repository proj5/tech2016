(function () {
  'use strict';

  angular
    .module('tech2016.question.services')
    .factory('PostService', PostService);

  PostService.$inject = ['$cookies', '$http'];

  function PostService($cookies, $http) {

    var PostService = {
      getComments: getComments,
      getMyVote: getMyVote
    };

    return PostService;
    
    function getComments(post, callback){
      var commentsURL = "/api/v1/comments/id=" + post.id + "/";
      $http.get(commentsURL).then(function successCallback(response){        
        post.comments = response.data;
        callback(post);
      }, function errorCallback(response){
        console.log("Error get comments for question");
        post.comments = [];
      });
    }
    
    function getMyVote(post){
      var voteStatusURL = "/api/v1/vote/?postID=" + post.id;
      $http.get(voteStatusURL).then(function successCallback(response) {
        post.myScore = response.data;
      },function errorCallback(response) {});
    }

    
  }
})();