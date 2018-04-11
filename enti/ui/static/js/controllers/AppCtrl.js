define(['./module'], function (controllers) {
    'use strict';

    controllers.controller('AppCtrl', ['$rootScope', '$http', '$scope', '$window', 'moment', 'IOSvc', 'AttributeSvc',
        'EntitySvc', 'NotificationSvc', 'FileUploader',
        function ($rootScope, $http, $scope, $window, moment, io, attrSvc, entitySvc, n, FileUploader) {

            console.log('AppCtrl');

            $scope.attributes = {};
            $scope.entities = {};
            $scope.entityTypes = {};
            $scope.source = 'testSource';


            $scope.view = 'default';
            $scope.uploader = new FileUploader();

            $scope.attrForm = {
                entityId: null,
                attributeId: null,
                fields: {}
            };

            $scope.exportEntities = function () {
                n.info('Export', 'Preparing entities for export');
                io.emit('entity.export.all', null);
            };

            $scope.form = {
                hover: {},
                attribute: {
                    edit: {},
                    new: {},
                    expanded: {}
                },
                entity: {
                    expanded: {},
                    edit: {},
                    new: {}
                },
                expanded: {},
                property: {},
                add: {
                    entity: {
                        id: null,
                        name: null,
                        type: null,
                        canonical: true,
                        expanded: false
                    }
                },
                remove: {
                    entity: {
                        expanded: {}
                    }
                }
            };

            $scope.hover = {};

            $scope.addEntity = function () {
                io.emit('entity.add', {
                    id: $scope.form.add.entity.id,
                    name: $scope.form.add.entity.name,
                    type: $scope.form.add.entity.type,
                    canonical: $scope.form.add.entity.canonical
                });
                $scope.form.add.entity.expanded = false;
            };

            $scope.reattemptAddEntity = function () {
                $scope.form.add.entity.expanded = true;
                n.warning('Add Entity', 'Please check new entity data and try again.');
            };

            $scope.confirmAddEntity = function () {
                $scope.form.add.entity.id = null;
                $scope.form.add.entity.name = null;
                $scope.form.add.entity.type = null;
                $scope.form.add.entity.canonical = true;
            };

            $scope.initializeEntityProps = function (entityId) {
                $scope.form.property[entityId] = {
                    id: {
                        hover: false,
                        expanded: false,
                        edit: null
                    },
                    name: {
                        hover: false,
                        expanded: false,
                        edit: null
                    },
                    type: {
                        hover: false,
                        expanded: false,
                        edit: null
                    },
                    canonical: {
                        hover: false,
                        expanded: false,
                        edit: null
                    }
                }
            };

            $scope.updateEntity = function (entityId, property) {
                var entity = {
                    id: $scope.entities[entityId].id,
                    name: $scope.entities[entityId].name,
                    type: $scope.entities[entityId].type,
                    canonical: $scope.entities[entityId].canonical
                };
                entity[property] = $scope.form.property[entityId][property].edit;
                io.emit('entity.update', entity);
                $scope.form.property[entityId][property].expanded = false;
            };

            $scope.beforeEditProperty = function (entityId, property) {
                $scope.form.property[entityId][property].expanded = true;
                $scope.form.property[entityId][property].edit = $scope.entities[entityId][property];
            };

            $scope.initializeContainerItem = function (entityId) {
                if ($scope.form.expanded[entityId] == null) {
                    $scope.form.expanded[entityId] = false;
                }
            };

            $scope.beforeAddAttribute = function (entityId) {
                $scope.form.attribute.new[entityId] = {
                    attributeId: null,
                    fields: {}
                };
            };

            $scope.addAttribute = function (entityId) {
                console.log('Add attribute: ' + entityId + ', ' + $scope.form.attribute.new[entityId].attributeId);
                console.log($scope.form.attribute.new[entityId].fields);
                io.emit('attribute.add', {
                    entityId: entityId,
                    attributeId: $scope.form.attribute.new[entityId].attributeId,
                    fields: $scope.form.attribute.new[entityId].fields
                });
            };

            $scope.removeAttribute = function (entityId, attributeId) {
                console.log('Remove attribute: ' + entityId + ', ' + attributeId);
                io.emit('attribute.remove', {
                    entityId: entityId,
                    attributeId: attributeId
                })
            };

            $scope.initAttributeField = function (fieldId) {
                if ($scope.form.attribute.edit[fieldId] == null) {
                    $scope.form.attribute.edit[fieldId] = {
                        expanded: false,
                        value: null
                    };
                }
            };

            $scope.beforeUpdateAttribute = function (fieldId) {
                $scope.initAttributeField(fieldId);
                $scope.form.attribute.edit[fieldId].expanded = !$scope.form.attribute.edit[fieldId].expanded;
            };

            $scope.updateAttribute = function (entityId, attributeId, fieldId) {
                n.info('Updating Attribute', 'Updating ' + $scope.entities[entityId].name + ' field to ' + $scope.form.attribute.edit[fieldId].value);
                io.emit('attribute.update', {
                    entityId: entityId,
                    fieldId: fieldId,
                    value: $scope.form.attribute.edit[fieldId].value
                });
                $scope.form.attribute.edit[fieldId].expanded = false;
                console.log('Update attribute: ' + entityId + ', ' + attributeId + ', ' + fieldId)
            };

            $scope.uploader.onAfterAddingFile = function (file) {
                console.log('File added');
                console.log(file);
            };

            $scope.uploader.onErrorItem = function (item, response, status, headers) {
                item.remove();
                n.warning('Upload failed', 'Ensure that the file is a valid XML file.')
            };

            $scope.uploader.onSuccessItem = function (item, response, status, headers) {
                item.remove();
                n.info('Upload successful', 'The XML file has been uploaded successfully.');
                io.emit('xml.upload', null)
            };


            $scope.setView = function (view) {
                console.log('View set to ' + view);
                $scope.view = view;
            };

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

            $scope.removeEntity = function (entityId) {
                io.emit('entity.remove', {
                    id: entityId
                });
                delete $scope.entities[entityId];
                delete entitySvc.entities[entityId];
            };

            io.on('attribute.sync', function (attributes) {
                $scope.attributes = attrSvc.sync(attributes);
            });

            io.on('entity.sync.all', function (entities) {
                $scope.entities = entitySvc.syncAll(entities);
            });

            io.on('entity.sync', function (entity) {
                $scope.entities[entity.id] = entitySvc.sync(entity);
            });

            io.on('entity.type.sync', function (types) {
                $scope.entityTypes = types;
            });

            io.on('entity.add.success', function () {
                $scope.confirmAddEntity();
                n.info('Add Entity', 'Entity added successfully.');
            });

            io.on('entity.add.failure', function () {
                $scope.reattemptAddEntity();
            });

            io.on('entity.export.all.success', function () {
                // $http({
                //     method: "get",
                //     url: "export"
                // }).success(function () {
                //     n.info('Export', 'Export successful');
                // }).error(function () {
                //     n.danger('Export', 'Export failed');
                // })
                //Initialize file format you want csv or xls
                var uri = 'data:text/xml;charset=utf-8,';

                //this trick will generate a temp <a /> tag
                var link = document.createElement("a");
                link.href = 'export';

                //set the visibility hidden so it will not effect on your web-layout
                link.style = "visibility:hidden";
                link.download = "entities.xml"; //this is an example file to download, use yours

                //this part will append the anchor tag and remove it after automatic click
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            });

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

            io.emit('attribute.sync', null);
            io.emit('entity.sync.all', null);
            io.emit('entity.type.sync', null);
        }])
});