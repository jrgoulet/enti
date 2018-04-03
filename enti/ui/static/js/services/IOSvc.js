define(['./module'], function (services) {
	'use strict';
	services.factory('IOSvc', ['$rootScope', 'moment',
		function ($rootScope, moment) {

			return {
				on: on,
				emit: emit
			};

			//////////////////////////////////////////////////

			function on(event, callback) {
				socket.on(event, function (data) {

					log().on(event, data);
					var args = arguments;

					$rootScope.$apply(function () {
						callback.apply(socket, args);
					});
				});
			}

			function emit(event, data, callback) {
				socket.emit(event, data, function () {

					log().emit(event, data);
					var args = arguments;

					$rootScope.$apply(function () {
						if (callback) {
							callback.apply(socket, args);
						}
					});
				});
			}

			function log() {
				return {
					on: function (event, data) {
						console.log(
							'<<' + '\t' +
							moment().format('HH:mm:ss') +
							'\t' + event + '\t'
						);
						console.log(
							data
						)
					},
					emit: function (event, data) {
						console.log(
							'>>' + '\t' +
							moment().format('HH:mm:ss') +
							'\t' + event + '\t'
						);
					}
				}
			}
		}])
});