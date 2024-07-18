from flask.views import MethodView
from flask_smorest import Blueprint

from app.schemas.simulation_schema import (
    SimulationByModelQuerySchema,
    SimulationSchema,
    SimulationRunSchema,
    SimulationCreateBodySchema,
    SimulationUpdateBodySchema,
)
from app.services import simulation_service

blp = Blueprint("Simulation", __name__, description="Simulation API")


@blp.route("/simulations")
class SimulationList(MethodView):
    @blp.arguments(SimulationByModelQuerySchema, location='query')
    @blp.response(200, SimulationSchema(many=True))
    def get(self, query_data):
        result = simulation_service.get_simulation_by_model_id(
            query_data['modelId']
        )
        return result

    @blp.arguments(SimulationCreateBodySchema)
    @blp.response(201, SimulationSchema)
    def post(self, body_data):
        schema = SimulationCreateBodySchema()
        validated_data = schema.load(body_data)
        result = simulation_service.create_new_simulation(validated_data)
        return result


@blp.route("/simulations/<int:simulation_id>")
class SimulationList(MethodView):
    @blp.response(200, SimulationSchema)
    def get(self, simulation_id):
        result = simulation_service.get_simulation_by_id(simulation_id)
        return result

    @blp.arguments(SimulationUpdateBodySchema)
    @blp.response(200, SimulationSchema)
    def put(self, body_data, simulation_id):
        result = simulation_service.update_simulation_by_id(body_data, simulation_id)
        return result

    @blp.response(200)
    def delete(self, simulation_id):
        simulation_service.delete_simulation(simulation_id)
        return {
            "message": "Simulation deleted successfully!"
        }


@blp.route("/simulations/run")
class SimulationRunList(MethodView):
    @blp.response(200, SimulationRunSchema(many=True))
    def get(self):
        result = simulation_service.get_simulation_run()
        return result

    @blp.arguments(SimulationCreateBodySchema)
    @blp.response(201, SimulationSchema)
    def post(self, body_data):
        schema = SimulationCreateBodySchema()
        validated_data = schema.load(body_data)
        result = simulation_service.create_new_simulation(validated_data)
        return result


# TODO: implement route for /simulations/run/:simulationrunId
# TODO: implement route for /simulations/run/status/:simulationsrunId