(function () {
  'use strict';

  angular
    .module('tech2016.question.controllers')
    .controller('ListQuestionController', ListQuestionController);

    ListQuestionController.$inject = ['$http'];

  function ListQuestionController($http) {
    var vm = this;
    vm.questions = [];
    
    var promises = [];
    var ajax = [];
        
    getNextQuestions(0 , 5);
        
    vm.loadMoreQuestions = function(){
      if (vm.questions.length > 0)
        getNextQuestions(vm.questions[ vm.questions.length - 1].id, 5);
    }
    
    function getQuestionAnswerDetail(question){      
      promises.push(
        $http.get("api/v1/vote/?postID=" + question.answer.id)
          .then(function successCallback(response) {
            question.answer.myScore = response.data;
          }, function errorCallback(response) {
            question.answer.myScore = 0;
          })
      )
    }    
    
    function getNextQuestions(startID, count){
      var url = "api/v1/questions/newest/?startID=" + startID + "&count=" + count;
      console.log(url);
      ajax.push($http.get(url)
        .then(function successCallback(response) {
          if (response.data.length == 0)
            vm.noMore = true;
          for(var i = 0; i < response.data.length; ++i)
            vm.questions.push(response.data[i]);
          response.data.forEach(getQuestionAnswerDetail);
        }, function errorCallback(response) {
          console.error("Failed to get questions");
        })
      );
    }    
  }
})();
