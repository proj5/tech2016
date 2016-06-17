(function () {
  'use strict';
  angular
    .module('tech2016.profile.controllers')
    .controller('ProfileController', ProfileController);

  ProfileController.$inject = ['$scope', '$state', '$stateParams', '$http', 'fileUpload', 'Authentication'];

  function ProfileController($scope, $state, $stateParams, $http, fileUpload, Authentication) {
    var vm = this;
    vm.changeAvatar = false;
    vm.questions = [];

    init();
    getAvatar();
    getNextQuestions(0 , 5);

    function init() {
      vm.username = $stateParams.username;
      getUserProfile();
      vm.view = 'question';
      vm.noMore = false;
    }

    function getUserProfile() {
      var url = "api/v1/accounts/" + vm.username + "/";
      $http.get(url)
        .then(function successCallback(response) {
          vm.user = response.data;
        }, function errorCallback(response) {
          console.error("Failed to get user profile");
        })
    }

    function getAvatar() {
      var url = "api/v1/account/avatar/" + vm.username + "/";
      $http.get(url)
        .then(function successCallback(response) {
          vm.avatar = response.data;
        }, function errorCallback(response) {
          console.error("Failed to get avatar");
        })
    }

    vm.uploadAvatar = function() {
      var url = "api/v1/account/avatar/" + vm.username + "/";
      fileUpload.uploadFileToUrl(vm.newAvatar, url);
      $state.reload();
    }

    vm.loadMoreQuestions = function(){
      if (vm.questions.length > 0)
        getNextQuestions(vm.questions[ vm.questions.length - 1].id, 5);
    }

    function getNextQuestions(startID, count){
      var url = "api/v1/profile/" + vm.username + "/?type=question&startID=" + startID + "&count=" + count;
      console.log(url);
      $http.get(url)
        .then(function successCallback(response) {
          if (response.data.length == 0)
            vm.noMore = true;
          for(var i = 0; i < response.data.length; ++i)
            vm.questions.push(response.data[i]);
        }, function errorCallback(response) {
          console.error("Failed to get questions");
        });
    }
  }

  angular
    .module('tech2016.profile.controllers')
    .directive('fileModel', ['$parse', function ($parse) {
      return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;

            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
      };
    }]);
})();