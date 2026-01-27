import time

import grpc
import pb.ads_pb2
import pb.ads_pb2_grpc
import pb.properties_pb2
import pb.properties_pb2_grpc

def run():
    # Connect to the server
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = pb.properties_pb2_grpc.PropertyServiceStub(channel)
        
        # # Create a request
        # request = pb.properties_pb2.FilterPropertyRequest(
        #     # The line `# area={"min": 50, "max": 100},` is a commented-out line in the code snippet
        #     # you provided. This means that it is not currently being executed by the program.
        #     area={"min": 50, "max": 100},
        #     page=1,
        # )
        
        # # Make the call
        # response = stub.SearchProperties(request)
        
        # # Print the response
        # print("SearchProperties response received")
        
        # response = stub.CountProperties(request)
        # print("CountProperties response received", response)
        
        # request = pb.properties_pb2.SinglePropertyRequest(property_id_nma="0301-148-303-0-0")
        # response = stub.GetProperty(request)
        # print("GetProperty response received")
        
        # request = pb.properties_pb2.PropertyUnitsRequest(property_id_nma="0301-148-303-0-0", page=1)
        # response = stub.GetPropertyUnits(request)
        # print("GetPropertyUnits response received")
        
        # response = stub.CountPropertyUnits(request)
        # print("CountPropertyUnits response received", response)
        
        # request = pb.properties_pb2.SingleUnitRequest(unit_id=288292015)
        # response = stub.GetUnit(request)
        # print("GetUnit response received")
        
        # request = pb.properties_pb2.OwnedItemsRequest(owner_id="40008146", page=1)
        # response = stub.GetOwnedProperties(request)
        # print("GetOwnedProperties response received")
        
        # response = stub.CountOwnedProperties(request)
        # print("CountOwnedProperties response received", response)
        
        request = pb.properties_pb2.SingleUnitRequest(unit_id=286606769)    
        response = stub.GetHistoricValuations(request)
        print(f"GetHistoricValuations response received: {response}")
        
        # stub = pb.ads_pb2_grpc.AdServiceStub(channel)
        
        # request = pb.ads_pb2.SingleAdRequest(property_id_nma="0301-148-303-0-3", phone_number="993040253")
        # response = stub.HasWriteAccess(request)
        # print(f"HasWriteAccess response received: {response}")
        
        # request = pb.ads_pb2.SingleAdRequest(property_id_nma="0301-148-303-0-0", phone_number="99304024")
        # response = stub.HasWriteAccess(request)
        # print(f"HasWriteAccess response received: {response}")
        
        # request = pb.ads_pb2.RealEstateAd(
        #     title="New Ad",
        #     description="This is a new ad",
        #     address="123 Main St",
        #     property_id_nma="0301-148-303-0-0",
        #     price=1000,
        #     type="rental",
        #     phone_number="99304024",
        # )
        # response = stub.CreateAd(request)
        # print(f"CreateAd response received: {response}")
        # ad_id = response.id
        
        # request = pb.ads_pb2.SingleAdRequest(id=ad_id)
        # response = stub.GetAd(request)
        # print(f"GetAd response received: {response}")
        
        # request = pb.ads_pb2.FilterAdsRequest(
        #     property_id_nma="0301-148-303-0-1",
        #     # type="rental",
        #     # status="live",
        #     # min_price=1000,
        #     # max_price=2000,
        #     page=1,
        # )
        # response = stub.GetAds(request)
        # print(f"GetAds response received: {len(response.ads)}")
        
        # request = pb.ads_pb2.RealEstateAd(
        #     id=ad_id,
        #     title="New Ad",
        #     description="This is a new ad",
        #     address="123 Main St",
        #     property_id_nma="0301-148-303-0-0",
        #     price=1000,
        #     type="rental",
        #     phone_number="99304024",
        # )
        # response = stub.UpdateAd(request)
        # print(f"UpdateAd response received: {response}")
        
        # time.sleep(5)
        # request = pb.ads_pb2.SingleAdRequest(id=ad_id, property_id_nma="0301-148-303-0-0", phone_number="99304024")
        # response = stub.DeleteAd(request)
        # print(f"DeleteAd response received: {response}")

if __name__ == "__main__":
    run()
