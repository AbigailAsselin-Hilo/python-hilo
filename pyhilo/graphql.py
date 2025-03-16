import asyncio
from typing import Any, Dict
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.websockets import WebsocketsTransport
from pyhilo.device.graphql_value_mapper import GraphqlValueMapper
from pyhilo import API
from pyhilo.devices import Devices
from typing import List, Optional


class GraphQlHelper:
    """The GraphQl Helper class."""

    def __init__(self, api: API, devices: Devices):
        self._api = api
        self._devices = devices
        self.access_token = ""
        self.mapper: GraphqlValueMapper = GraphqlValueMapper()

        self.subscriptions: List[Optional[asyncio.Task]] = [None]

    async def async_init(self) -> None:
        """Initialize the Hilo "GraphQlHelper" class."""
        self.access_token = await self._api.async_get_access_token()
        self.subscriptions[0] = asyncio.create_task(
            self._subscribe_to_device_updated(self._devices.location_hilo_id)
        )
        await self.call_get_location_query(self._devices.location_hilo_id)

    QUERY_GET_LOCATION: str = """query getLocation($locationHiloId: String!) {
                getLocation(id:$locationHiloId) {
                    hiloId
                    lastUpdate
                    lastUpdateVersion
                    devices {
                    deviceType
                        hiloId
                        physicalAddress
                        connectionStatus
                        ... on Gateway {
                            connectionStatus
                            controllerSoftwareVersion
                            lastConnectionTime
                            willBeConnectedToSmartMeter
                            zigBeeChannel
                            zigBeePairingModeEnhanced
                            smartMeterZigBeeChannel
                            smartMeterPairingStatus
                        }
                        ... on BasicSmartMeter {
                            deviceType
                            hiloId
                            physicalAddress
                            connectionStatus
                            zigBeeChannel
                            power {
                                value
                                kind
                            }
                        }
                        ... on LowVoltageThermostat {
                            coolTempSetpoint {
                                value
                            }
                            fanMode
                            fanSpeed
                            mode
                            currentState
                            power {
                                value
                                kind
                            }
                            ambientHumidity
                            gDState
                            ambientTemperature {
                                value
                                kind
                            }
                            ambientTempSetpoint {
                                value
                                kind
                            }
                            version
                            zigbeeVersion
                            connectionStatus
                            maxAmbientCoolSetPoint {
                                value
                                kind
                            }
                            minAmbientCoolSetPoint {
                                value
                                kind
                            }
                            maxAmbientTempSetpoint {
                                value
                                kind
                            }
                            minAmbientTempSetpoint {
                                value
                                kind
                            }
                            allowedModes
                            fanAllowedModes
                        }
                        ... on BasicSwitch {
                            deviceType
                            hiloId
                            physicalAddress
                            connectionStatus
                            state
                            power {
                                value
                                kind
                            }
                        }
                        ... on BasicLight {
                            deviceType
                            hiloId
                            physicalAddress
                            connectionStatus
                            state
                            hue
                            level
                            saturation
                            colorTemperature
                            lightType
                        }
                        ... on BasicEVCharger {
                            deviceType
                            hiloId
                            physicalAddress
                            connectionStatus
                            status
                            power {
                                value
                                kind
                            }
                        }
                        ... on BasicChargeController {
                            deviceType
                            hiloId
                            physicalAddress
                            connectionStatus
                            gDState
                            version
                            zigbeeVersion
                            state
                            power {
                                value
                                kind
                            }
                        }
                        ... on HeatingFloorThermostat {
                            deviceType
                            hiloId
                            physicalAddress
                            connectionStatus
                            ambientHumidity
                            gDState
                            version
                            zigbeeVersion
                            thermostatType
                            physicalAddress
                            floorMode
                            power {
                                value
                                kind
                            }
                            ambientTemperature {
                                value
                                kind
                            }
                            ambientTempSetpoint {
                                value
                                kind
                            }
                            maxAmbientTempSetpoint {
                                value
                                kind
                            }
                            minAmbientTempSetpoint {
                                value
                                kind
                            }
                            floorLimit {
                                value
                            }
                        }
                        ... on WaterHeater {
                            deviceType
                            hiloId
                            physicalAddress
                            connectionStatus
                            gDState
                            version
                            probeTemp {
                                value
                                kind
                            }
                            zigbeeVersion
                            state
                            ccrType
                            alerts
                            power {
                                value
                                kind
                            }
                        }
                        ... on BasicDimmer {
                            deviceType
                            hiloId
                            physicalAddress
                            connectionStatus
                            state
                            level
                            power {
                                value
                                kind
                            }
                        }
                        ... on BasicThermostat {
                            deviceType
                            hiloId
                            physicalAddress
                            connectionStatus
                            ambientHumidity
                            gDState
                            version
                            zigbeeVersion
                            ambientTemperature {
                                value
                                kind
                            }
                            ambientTempSetpoint {
                                value
                                kind
                            }
                            power {
                                value
                                kind
                            }
                        }
                    }
                }
    }"""

    SUBSCRIPTION_DEVICE_UPDATED: str = """subscription onAnyDeviceUpdated($locationHiloId: String!) {
    onAnyDeviceUpdated(locationHiloId: $locationHiloId) {
        deviceType
        locationHiloId
        transmissionTime
        operationId
        status
        device {
            ... on Gateway {
                connectionStatus
                controllerSoftwareVersion
                lastConnectionTime
                willBeConnectedToSmartMeter
                zigBeeChannel
                zigBeePairingModeEnhanced
                smartMeterZigBeeChannel
                smartMeterPairingStatus
            }
            ... on BasicSmartMeter {
                deviceType
                hiloId
                physicalAddress
                connectionStatus
                zigBeeChannel
                power {
                    value
                    kind
                }
            }
            ... on LowVoltageThermostat {
                deviceType
                hiloId
                physicalAddress
                  coolTempSetpoint {
                    value
                  }
                  fanMode
                  fanSpeed
                  mode
                  currentState
                  power {
                    value
                    kind
                  }
                  ambientHumidity
                  gDState
                  ambientTemperature {
                    value
                    kind
                  }
                  ambientTempSetpoint {
                    value
                    kind
                  }
                  version
                  zigbeeVersion
                  connectionStatus
                  maxAmbientCoolSetPoint {
                     value
                     kind
                  }
	              minAmbientCoolSetPoint {
	                value
                    kind
	              }
                maxAmbientTempSetpoint {
                    value
                    kind
                }
		            minAmbientTempSetpoint {
                    value
                    kind
		            }
		            allowedModes
		            fanAllowedModes
            }
            ... on BasicSwitch {
   	            deviceType
                hiloId
                physicalAddress
                connectionStatus
                state
                power {
                    value
                    kind
                }
            }
            ... on BasicLight {
                deviceType
                hiloId
                physicalAddress
                connectionStatus
                state
                hue
                level
                saturation
                colorTemperature
                lightType
            }
            ... on BasicEVCharger {
                deviceType
                hiloId
                physicalAddress
                connectionStatus
                status
                power {
                    value
                    kind
                }
            }
            ... on BasicChargeController {
                deviceType
                hiloId
                physicalAddress
                connectionStatus
                gDState
                version
                zigbeeVersion
                state
                power {
                    value
                    kind
                }
            }
            ... on HeatingFloorThermostat {
                deviceType
                hiloId
                physicalAddress
                connectionStatus
                ambientHumidity
                gDState
                version
                zigbeeVersion
                thermostatType
                physicalAddress
                floorMode
                power {
                    value
                    kind
                }
                ambientTemperature {
                    value
                    kind
                }
                ambientTempSetpoint {
                    value
                    kind
                }
                maxAmbientTempSetpoint {
                    value
                    kind
                }
                minAmbientTempSetpoint {
                    value
                    kind
                }
                floorLimit {
                    value
                }
            }
            ... on WaterHeater {
                deviceType
                hiloId
                physicalAddress
                connectionStatus
                gDState
                version
                probeTemp {
                    value
                    kind
                }
                zigbeeVersion
                state
                ccrType
	            alerts
                power {
                    value
                    kind
                }
            }
            ... on BasicDimmer {
                deviceType
                hiloId
                physicalAddress
                connectionStatus
                state
                level
                power {
                    value
                    kind
                }
            }
            ... on BasicThermostat {
                deviceType
                hiloId
                physicalAddress
                connectionStatus
                ambientHumidity
                gDState
                version
                zigbeeVersion
                ambientTemperature {
                    value
                    kind
                }
                ambientTempSetpoint {
                    value
                    kind
                }
                power {
                    value
                    kind
                }
            }
        }
    }
}"""

    async def call_get_location_query(self, location_hilo_id: str) -> None:
        transport = AIOHTTPTransport(
            url="https://platform.hiloenergie.com/api/digital-twin/v3/graphql",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql(self.QUERY_GET_LOCATION)

        async with client as session:
            result = await session.execute(
                query, variable_values={"locationHiloId": location_hilo_id}
            )
        self._handle_query_result(result)

    async def _subscribe_to_device_updated(self, location_hilo_id: str) -> None:
        transport = WebsocketsTransport(
            url=f"wss://platform.hiloenergie.com/api/digital-twin/v3/graphql?access_token={self.access_token}"
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql(self.SUBSCRIPTION_DEVICE_UPDATED)
        print("Connected to device updated subscription")
        try:
            async with client as session:
                async for result in session.subscribe(
                    query, variable_values={"locationHiloId": location_hilo_id}
                ):
                    self._handle_subscription_result(result)
        except asyncio.CancelledError:
            print("Subscription cancelled.")
            asyncio.sleep(1)
            await self._subscribe_to_device_updated(location_hilo_id)

    def _handle_query_result(self, result: Dict[str, Any]) -> None:
        devices_values: list[any] = result["getLocation"]["devices"]
        attributes = self.mapper.map_query_values(devices_values)
        self._devices.parse_values_received(attributes)

    def _handle_subscription_result(self, result: Dict[str, Any]) -> None:
        devices_values: list[any] = result["onAnyDeviceUpdated"]["device"]
        attributes = self.mapper.map_subscription_values(devices_values)
        self._devices.parse_values_received(attributes)
