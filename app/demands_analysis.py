from enum import Enum
from fastapi_camelcase import CamelModel
from pydantic import Field
from typing import List, Optional


class ResourceTypeType(str, Enum):
    """
    Type of resource type
    """

    generic = "Generic"
    continuous = "Continuous"
    discrete = "Discrete"


class Environment(str, Enum):
    """
    Stowage environment
    """

    pressurized = "Pressurized"
    unpressurized = "Unpressurized"


class ResourceType(CamelModel):
    """
    Type of resource
    """

    type: ResourceTypeType = Field(..., description="Type of this resource type")
    name: str = Field(..., description="Name of this resource type")
    class_of_supply: int = Field(..., description="Class of supply")
    environment: Environment = Field(..., description="Environment type")
    units: str = Field(..., description="Unit label for this resource type")
    unit_mass: float = Field(
        ..., description="Mass (kg) of 1.0 units of this resource type"
    )
    unit_volume: float = Field(
        ..., description="Volume (m^3) of 1.0 units of this resource type"
    )
    packing_factor: float = Field(
        ...,
        description="Estimated mass (kg) of COS 5 required to pack 1.0 units of this resource",
    )


class Location(CamelModel):
    """
    Spatial location in a scenario
    """

    id: int = Field(..., description="ID of this location")
    name: str = Field(..., description="Name of this location")


class Element(CamelModel):
    """
    Persistent element taking part in a scenario
    """

    id: int = Field(..., description="ID of this element")
    name: str = Field(..., description="Name of this element")


class Resource(CamelModel):
    """
    A defined quantity of a resource type.
    """

    resource: ResourceType = Field(..., description="Type of resource")
    amount: float = Field(..., description="Amount of resource (units)")
    mass: float = Field(..., description="Mass (kg) of resource")
    volume: float = Field(..., description="Volume (m^3) of resource")


class RawDemand(CamelModel):
    """
    Set of demands aggregated to a moment in time
    """

    time: float = Field(
        ..., description="Time (days relative to scenario start) of this demand"
    )
    location: Location = Field(
        ..., description="Location (node) associated with this demand"
    )
    element: Optional[Element] = Field(
        None, description="Element associated with this demand"
    )
    consumption: List[Resource] = Field(
        [], description="List of consumption demands aggregated to this moment"
    )
    production: List[Resource] = Field(
        [], description="List of production demands aggregated to this moment"
    )
    total_mass: float = Field(
        ..., description="Total mass (kg) of all demands aggregated to this moment"
    )
    total_volume: float = Field(
        ..., description="Total volume (m^3) of all demands aggregated to this moment"
    )


class RawDemandsAnalysis(CamelModel):
    """
    Set of demands aggregated to a moment in time
    """

    demands: List[RawDemand] = Field(
        [], description="List of demands aggregated to moments in time"
    )


class NodeDemand(CamelModel):
    """
    Demands aggregated to a supply node
    """

    time: float = Field(
        ...,
        description="Time (days relative to scenario start) of a supply opportunity to a node",
    )
    location: Location = Field(
        ..., description="Location associated with this supply node"
    )
    consumption: List[Resource] = Field(
        [], description="List of consumption demands aggregated to this supply node"
    )
    production: List[Resource] = Field(
        [], description="List of production demands aggregated to this supply node"
    )
    total_mass: float = Field(
        ..., description="Total mass (kg) of all demands aggregated to this supply node"
    )
    total_volume: float = Field(
        ...,
        description="Total volume (m^3) of all demands aggregated to this supply node",
    )


class EdgeDemand(CamelModel):
    """
    Demands aggregated to a supply edge
    """

    start_time: float = Field(
        ..., description="Start time (days relative to scenario start)"
    )
    end_time: float = Field(
        ..., description="End time (days relative to scenario start)"
    )
    origin: Location = Field(..., description="Origin of this edge")
    destination: Location = Field(..., description="Destination of this edge")
    location: Location = Field(
        ..., description="Location (edge) associated with this supply edge"
    )
    consumption: List[Resource] = Field(
        [], description="List of consumption demands aggregated to this supply edge"
    )
    production: List[Resource] = Field(
        [], description="List of production demands aggregated to this supply edge"
    )
    total_mass: float = Field(
        ..., description="Total mass (kg) of all demands aggregated to this supply edge"
    )
    total_volume: float = Field(
        ...,
        description="Total volume (m^3) of all demands aggregated to this supply edge",
    )
    max_cargo_mass: float = Field(
        ...,
        description="Max cargo mass (kg) available on all carriers in this supply edge",
    )
    net_cargo_mass: float = Field(
        ...,
        description="Net cargo mass (kg) remaining on all carriers in this supply edge",
    )
    max_cargo_volume: float = Field(
        ...,
        description="Max cargo volume (m^3) available on all carriers in this supply edge",
    )
    net_cargo_volume: float = Field(
        ...,
        description="Net cargo volume (m^3) remaining on all carriers in this supply edge",
    )


class AggregatedDemandsAnalysis(CamelModel):
    """
    List of demands aggregated to supply nodes and edges
    """

    nodes: List[NodeDemand] = Field(
        [], description="List of demands aggregated to supply nodes"
    )
    edges: List[EdgeDemand] = Field(
        [], description="List of demands aggregated to supply edges"
    )
