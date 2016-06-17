(function () {
  'use strict';

  angular
    .module('tech2016.topic.services')
    .factory('TopicService', TopicService);

  TopicService.$inject = ['$cookies', '$http'];

  function TopicService($cookies, $http) {

    var TopicService = {
      getRelatedTopic: getRelatedTopic
    };

    return TopicService;
    
    function getRelatedTopic(keyword, callback){
      var url = "api/v1/topics/?keyword=" + keyword;
      $http.get(url).
        then(
          function successCallback(response){
            callback(response.data);
          }, 
          function errorCallback(response) {
            callback([]);
          }
        );
    }
 
  }
})();