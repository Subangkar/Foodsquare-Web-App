var app = angular.module('demoApp', ['ngAnimate']);
app.controller('demoController', function($scope, $http){
	var opendd;
	angular.element('#notifications-count').removeClass('fadeIn').addClass('fadeOut');

	$scope.showNotifications = function($event){
		var targetdd = angular.element($event.target).closest('.dropdown-container').find('.dropdown-menu');
		opendd = targetdd;
		if(targetdd.hasClass('fadeInDown')){
			hidedd(targetdd);
		}
		else{
			targetdd.css('display', 'block').removeClass('fadeOutUp').addClass('fadeInDown')
				.on('animationend webkitAnimationEnd oanimationend MSAnimationEnd', function(){
					angular.element(this).show();
				});
			targetdd.find('.dropdown-body')[0].scrollTop = 0;
			$scope.awaitingNotifications = 0;
			angular.element('#notifications-count').removeClass('fadeIn').addClass('fadeOut');
		}
	};

	// //Hide dropdown function
	var hidedd = function(targetdd){
		$http({
			url: "/customer/read_notifications/",
			method: "GET",
			data: {"foo":"bar"}
		}).then(function successCallback(response) {

			$scope.newNotifications = response.data.notifications;
			// $scope.awaitingNotifications = 3;
			console.log(response.data.notifications);
		}, function errorCallback(response) {
			$scope.newNotifications = response;
		});
		targetdd.removeClass('fadeInDown').addClass('fadeOutUp')
			.on('animationend webkitAnimationEnd oanimationend MSAnimationEnd', function(){
				angular.element(this).hide();
			});
		opendd = null;
		$scope.awaitingNotifications = 0;
		// angular.forEach($scope.newNotifications, function(notification){
		// 	$scope.readNotifications.push(notification);
		// });
		$scope.newNotifications = [];

		if($scope.awaitingNotifications > 0)
			angular.element('#notifications-count').removeClass('fadeOut').addClass('fadeIn');

	}


	window.onclick = function(event){
		var clickedElement = angular.element(event.target);
		var clickedDdTrigger = clickedElement.closest('.dd-trigger').length;
		var clickedDdContainer = clickedElement.closest('.dropdown-menu').length;
		if(opendd != null && clickedDdTrigger == 0 && clickedDdContainer == 0){
			hidedd(opendd);
		}
	}

	window.onbeforeunload = function(e) {
		if(opendd != null){
			console.log('closingdd');
			hidedd(opendd);
		}
	};

	// init();
	setInterval(function(){
		$http({
			url: "/customer/get_notifications/",
			method: "GET",
			data: {"foo":"bar"}
		}).then(function successCallback(response) {

			$scope.newNotifications = response.data.notifications;
			$scope.awaitingNotifications = $scope.newNotifications.length;
			if($scope.awaitingNotifications > 0 )
			{
				angular.element('#notifications-count').removeClass('fadeOut').addClass('fadeIn');
			}

			// console.log(response.data.notifications);
		}, function errorCallback(response) {
			$scope.newNotifications = response;
		});
	}, 4000);



});
