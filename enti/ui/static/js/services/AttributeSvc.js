define(['./module'], function (services) {
    'use strict';
    services.factory('AttributeSvc', ['IOSvc',
        function (io) {

            var attributes = {};

            return {
                attributes: attributes,
                sync: sync,
                add: add,
                remove: remove,
                update: update
            };

            //////////////////////////////////////////////////

            function sync(data) {
                attributes = data;
                return attributes;
            }


            function add($scope, entityId) {
                io.emit('attribute.add', {
                    entityId: entityId,
                    attributeId: $scope.form.attribute.new[entityId].attributeId,
                    fields: $scope.form.attribute.new[entityId].fields
                });
            }

            function remove(entityId, attributeId) {
                io.emit('attribute.remove', {
                    entityId: entityId,
                    attributeId: attributeId
                })
            }

            function update($scope, entityId, attributeId, fieldId) {
                io.emit('attribute.update', {
                    entityId: entityId,
                    fieldId: fieldId,
                    value: $scope.form.attribute.edit[fieldId].value
                });
                $scope.form.attribute.edit[fieldId].expanded = false;
            }


        }])
});