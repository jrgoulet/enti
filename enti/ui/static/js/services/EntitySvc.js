define(['./module'], function (services) {
	'use strict';
	services.factory('EntitySvc', [
		function () {

	        var entities = {};

			return {
				entities: entities,
                sync: sync
			};

			//////////////////////////////////////////////////

            function sync(data) {
                entities = data;
                return entities;
            }


		}])
});