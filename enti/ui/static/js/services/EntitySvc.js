define(['./module'], function (services) {
	'use strict';
	services.factory('EntitySvc', [
		function () {

	        var entities = {};

			return {
				entities: entities,
                syncAll: syncAll,
                sync: sync
			};

			//////////////////////////////////////////////////

            function syncAll(data) {
                entities = data;
                return entities;
            }

            function sync(entity) {
                entities[entity.id] = entity;
                return entity;
            }


		}])
});