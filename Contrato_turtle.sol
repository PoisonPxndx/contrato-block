// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract TurtleTracker {

    struct Vector3 {
        int256 x;
        int256 y;
        int256 z;
    }

    struct Route {
        string name;
        Vector3[] positions;
    }

    struct TurtleBot {
        string name;
        uint256[] routeIds;
    }

    mapping(uint256 => Route) private routes;
    mapping(uint256 => TurtleBot) private bots;

    uint256 public routeCounter;
    uint256 public botCounter;

    // Crear un recorrido vacío con nombre
    function createRoute(string memory _name) public {
        routes[routeCounter].name = _name;
        routeCounter++;
    }

    // Agregar una posición a un recorrido
    function addPositionToRoute(uint256 _routeId, int256 _x, int256 _y, int256 _z) public {
        require(_routeId < routeCounter, "Ruta no existe");
        routes[_routeId].positions.push(Vector3(_x, _y, _z));
    }

    // Crear un bot con nombre y sin rutas
    function createBot(string memory _name) public {
        bots[botCounter].name = _name;
        botCounter++;
    }

    // Asignar una ruta a un bot
    function assignRouteToBot(uint256 _botId, uint256 _routeId) public {
        require(_botId < botCounter, "Bot no existe");
        require(_routeId < routeCounter, "Ruta no existe");
        bots[_botId].routeIds.push(_routeId);
    }

    // Renombrar bot o recorrido
    function renameBot(uint256 _botId, string memory _newName) public {
        require(_botId < botCounter, "Bot no existe");
        bots[_botId].name = _newName;
    }

    function renameRoute(uint256 _routeId, string memory _newName) public {
        require(_routeId < routeCounter, "Ruta no existe");
        routes[_routeId].name = _newName;
    }

    // Obtener cantidad de posiciones en una ruta
    function getRouteLength(uint256 _routeId) public view returns (uint256) {
        require(_routeId < routeCounter, "Ruta no existe");
        return routes[_routeId].positions.length;
    }

    // Obtener una posición específica
    function getPosition(uint256 _routeId, uint256 _index) public view returns (int256, int256, int256) {
        require(_routeId < routeCounter, "Ruta no existe");
        require(_index < routes[_routeId].positions.length, unicode"Índice fuera de rango");
        Vector3 memory pos = routes[_routeId].positions[_index];
        return (pos.x, pos.y, pos.z);
    }

    // Obtener nombre de un recorrido
    function getRouteName(uint256 _routeId) public view returns (string memory) {
        require(_routeId < routeCounter, "Ruta no existe");
        return routes[_routeId].name;
    }

    // Obtener nombre de un bot
    function getBotName(uint256 _botId) public view returns (string memory) {
        require(_botId < botCounter, "Bot no existe");
        return bots[_botId].name;
    }

    // Obtener rutas asociadas a un bot
    function getBotRoutes(uint256 _botId) public view returns (uint256[] memory) {
        require(_botId < botCounter, "Bot no existe");
        return bots[_botId].routeIds;
    }

    // Ver si una ruta está asignada a algún bot
    function isRouteAssigned(uint256 _routeId) public view returns (bool) {
        require(_routeId < routeCounter, "Ruta no existe");
        for (uint256 i = 0; i < botCounter; i++) {
            uint256[] memory ids = bots[i].routeIds;
            for (uint256 j = 0; j < ids.length; j++) {
                if (ids[j] == _routeId) {
                    return true;
                }
            }
        }
        return false;
    }
}
