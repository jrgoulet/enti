define(['./module'], function (services) {
    'use strict';
    services.factory('EntitySvc', ['IOSvc',
        function (io) {

            var entities = {};

            return {
                entities: entities,
                syncAll: syncAll,
                sync: sync,
                export: export_,
                add: add,
                reattemptAdd: reattemptAdd,
                confirmAdd: confirmAdd,
                update: update,
                remove: remove,
                download: download
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

            function export_() {
                n.info('Export', 'Preparing entities for export');
                io.emit('entity.export.all', null);
            }

            function download() {
                var link = document.createElement("a");
                link.href = 'export';
                link.style = "visibility:hidden";
                link.download = "entities.xml";
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }

            function add($scope) {
                io.emit('entity.add', {
                    id: $scope.form.add.entity.id,
                    name: $scope.form.add.entity.name,
                    type: $scope.form.add.entity.type,
                    canonical: $scope.form.add.entity.canonical
                });
                $scope.form.add.entity.expanded = false;
            }

            function reattemptAdd($scope) {
                $scope.form.add.entity.expanded = true;
                n.warning('Add Entity', 'Please check new entity data and try again.');
            }

            function confirmAdd($scope) {
                $scope.form.add.entity.id = null;
                $scope.form.add.entity.name = null;
                $scope.form.add.entity.type = null;
                $scope.form.add.entity.canonical = true;
            }

            function update($scope, entityId, property) {
                var entity = {
                    id: $scope.entities[entityId].id,
                    name: $scope.entities[entityId].name,
                    type: $scope.entities[entityId].type,
                    canonical: $scope.entities[entityId].canonical
                };
                entity[property] = $scope.form.property[entityId][property].edit;
                io.emit('entity.update', entity);
                $scope.form.property[entityId][property].expanded = false;
            }

            function remove($scope, entityId) {
                io.emit('entity.remove', {
                    id: entityId
                });
                delete $scope.entities[entityId];
                delete entitySvc.entities[entityId];
            }


        }])
});