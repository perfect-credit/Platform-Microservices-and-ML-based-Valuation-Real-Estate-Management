import json

import grpc
import pb.valuation_pb2
import pb.valuation_pb2_grpc

def run():
    # Connect to the server
    with grpc.insecure_channel('localhost:50053') as channel:
        stub = pb.valuation_pb2_grpc.ValuationServiceStub(channel)
        
        request = pb.valuation_pb2.PropertyValuationRequest(property_id_nma="0301-27-493-0-0", date="2027-01-01")
        response = stub.GetPropertyValuation(request)
        print(f"GetPropertyValuation response received: {json.loads(response.valuations)}")
        
        request = pb.valuation_pb2.UnitValuationRequest(unit_id=288292015, date="2027-01-01")
        response = stub.GetUnitValuation(request)
        print(f"GetUnitValuation response received: {json.loads(response.valuations)}")

if __name__ == "__main__":
    run()
