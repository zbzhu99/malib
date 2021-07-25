# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

#import MoZiAI_SDK.core.GRPCServerBase_pb2 as GRPCServerBase__pb2
import malib.envs.mozi.mozi_simu_sdk.comm.GRPCServerBase_pb2 as GRPCServerBase__pb2


class gRPCStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GrpcConnect = channel.unary_unary(
        '/GRPC.gRPC/GrpcConnect',
        request_serializer=GRPCServerBase__pb2.GrpcRequest.SerializeToString,
        response_deserializer=GRPCServerBase__pb2.GrpcReply.FromString,
        )
    self.GrpcConnectStream = channel.unary_stream(
        '/GRPC.gRPC/GrpcConnectStream',
        request_serializer=GRPCServerBase__pb2.GrpcRequest.SerializeToString,
        response_deserializer=GRPCServerBase__pb2.GrpcReply.FromString,
        )


class gRPCServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def GrpcConnect(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GrpcConnectStream(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_gRPCServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GrpcConnect': grpc.unary_unary_rpc_method_handler(
          servicer.GrpcConnect,
          request_deserializer=GRPCServerBase__pb2.GrpcRequest.FromString,
          response_serializer=GRPCServerBase__pb2.GrpcReply.SerializeToString,
      ),
      'GrpcConnectStream': grpc.unary_stream_rpc_method_handler(
          servicer.GrpcConnectStream,
          request_deserializer=GRPCServerBase__pb2.GrpcRequest.FromString,
          response_serializer=GRPCServerBase__pb2.GrpcReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'GRPC.gRPC', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
