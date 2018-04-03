define(['./module'], function (controllers) {
	'use strict';

	controllers.controller('AppCtrl', ['$rootScope', '$http', '$scope', '$window', 'moment', 'IOSvc',
		function ($rootScope, $http, $scope, $window, moment, io) {

			console.log('AppCtrl');

			$scope.route = {
				add: function (source_id, cage_id) {
					routeSvc.add(source_id, cage_id)
				},
				remove: function (source_id, cage_id) {
					routeSvc.remove(source_id, cage_id);
				}
			};

			$scope.action = {
				locate: function (id) {
					actionSvc.locate(id)
				}
			};

			$scope.util = {
				isEmpty: function (dict) {
					if (dict !== null && typeof dict === 'object') {
						return Object.keys(dict).length === 0;
					}
					return true
				}
			};


			io.on('success', function (message) {
				console.log('success: ' + message.message);
				n.info(message.title, message.message);
			});

			io.on('info', function (message) {
				console.log('info: ' + message.message);
				n.info(message.title, message.message);
			});

			io.on('warning', function (message) {
				console.log('warning: ' + message.message);
				n.warning(message.title, message.message);
			});

			io.on('danger', function (message) {
				console.log('danger: ' + message.message);
				n.danger(message.title, message.message);
			});

			//////////////////////////////////////////////////

		}])
});