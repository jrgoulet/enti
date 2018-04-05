define(['./module'], function (services) {
	'use strict';
	services.factory('AttributeSvc', [
		function () {

	        var attributes = {};

			return {
				attributes: attributes,
                sync: sync
			};

			//////////////////////////////////////////////////

            function sync(data) {
                attributes = data;
                return attributes;
            }


		}])
});