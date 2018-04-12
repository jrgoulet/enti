define(['./module'], function (filters) {
	'use strict';
	filters.filter('entityType', function () {
		return function (input, entityType) {

		    var out = [];

		    console.log('entityType: ' + entityType);

		    angular.forEach(input, function(entity) {

		        if (entityType === 'all') {
		            out.push(entity)
                } else if (entityType === entity.type) {
                    out.push(entity)
                }
            });

            return out;
		};
	})
});