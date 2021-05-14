# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: peer.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='peer.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\npeer.proto\"\x0e\n\x0cGetSuccessor\"\x10\n\x0eGetPredecessor\"-\n\x11NotifyPredecessor\x12\n\n\x02ip\x18\x01 \x01(\x0c\x12\x0c\n\x04port\x18\x02 \x01(\r\"\x1c\n\rFindSuccessor\x12\x0b\n\x03key\x18\x01 \x01(\t\"4\n\x0cPeerResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\n\n\x02ip\x18\x02 \x01(\x0c\x12\x0c\n\x04port\x18\x03 \x01(\r\"\x1d\n\x0eStatusResponse\x12\x0b\n\x03res\x18\x01 \x01(\x08\x32\xd8\x01\n\x04Peer\x12.\n\x0cgetSuccessor\x12\r.GetSuccessor\x1a\r.PeerResponse\"\x00\x12\x32\n\x0egetPredecessor\x12\x0f.GetPredecessor\x1a\r.PeerResponse\"\x00\x12:\n\x11updatePredecessor\x12\x12.NotifyPredecessor\x1a\x0f.StatusResponse\"\x00\x12\x30\n\rfindSuccessor\x12\x0e.FindSuccessor\x1a\r.PeerResponse\"\x00\x62\x06proto3'
)




_GETSUCCESSOR = _descriptor.Descriptor(
  name='GetSuccessor',
  full_name='GetSuccessor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=14,
  serialized_end=28,
)


_GETPREDECESSOR = _descriptor.Descriptor(
  name='GetPredecessor',
  full_name='GetPredecessor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=30,
  serialized_end=46,
)


_NOTIFYPREDECESSOR = _descriptor.Descriptor(
  name='NotifyPredecessor',
  full_name='NotifyPredecessor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ip', full_name='NotifyPredecessor.ip', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='port', full_name='NotifyPredecessor.port', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=48,
  serialized_end=93,
)


_FINDSUCCESSOR = _descriptor.Descriptor(
  name='FindSuccessor',
  full_name='FindSuccessor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='FindSuccessor.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=95,
  serialized_end=123,
)


_PEERRESPONSE = _descriptor.Descriptor(
  name='PeerResponse',
  full_name='PeerResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='PeerResponse.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ip', full_name='PeerResponse.ip', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='port', full_name='PeerResponse.port', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=125,
  serialized_end=177,
)


_STATUSRESPONSE = _descriptor.Descriptor(
  name='StatusResponse',
  full_name='StatusResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='res', full_name='StatusResponse.res', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=179,
  serialized_end=208,
)

DESCRIPTOR.message_types_by_name['GetSuccessor'] = _GETSUCCESSOR
DESCRIPTOR.message_types_by_name['GetPredecessor'] = _GETPREDECESSOR
DESCRIPTOR.message_types_by_name['NotifyPredecessor'] = _NOTIFYPREDECESSOR
DESCRIPTOR.message_types_by_name['FindSuccessor'] = _FINDSUCCESSOR
DESCRIPTOR.message_types_by_name['PeerResponse'] = _PEERRESPONSE
DESCRIPTOR.message_types_by_name['StatusResponse'] = _STATUSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetSuccessor = _reflection.GeneratedProtocolMessageType('GetSuccessor', (_message.Message,), {
  'DESCRIPTOR' : _GETSUCCESSOR,
  '__module__' : 'peer_pb2'
  # @@protoc_insertion_point(class_scope:GetSuccessor)
  })
_sym_db.RegisterMessage(GetSuccessor)

GetPredecessor = _reflection.GeneratedProtocolMessageType('GetPredecessor', (_message.Message,), {
  'DESCRIPTOR' : _GETPREDECESSOR,
  '__module__' : 'peer_pb2'
  # @@protoc_insertion_point(class_scope:GetPredecessor)
  })
_sym_db.RegisterMessage(GetPredecessor)

NotifyPredecessor = _reflection.GeneratedProtocolMessageType('NotifyPredecessor', (_message.Message,), {
  'DESCRIPTOR' : _NOTIFYPREDECESSOR,
  '__module__' : 'peer_pb2'
  # @@protoc_insertion_point(class_scope:NotifyPredecessor)
  })
_sym_db.RegisterMessage(NotifyPredecessor)

FindSuccessor = _reflection.GeneratedProtocolMessageType('FindSuccessor', (_message.Message,), {
  'DESCRIPTOR' : _FINDSUCCESSOR,
  '__module__' : 'peer_pb2'
  # @@protoc_insertion_point(class_scope:FindSuccessor)
  })
_sym_db.RegisterMessage(FindSuccessor)

PeerResponse = _reflection.GeneratedProtocolMessageType('PeerResponse', (_message.Message,), {
  'DESCRIPTOR' : _PEERRESPONSE,
  '__module__' : 'peer_pb2'
  # @@protoc_insertion_point(class_scope:PeerResponse)
  })
_sym_db.RegisterMessage(PeerResponse)

StatusResponse = _reflection.GeneratedProtocolMessageType('StatusResponse', (_message.Message,), {
  'DESCRIPTOR' : _STATUSRESPONSE,
  '__module__' : 'peer_pb2'
  # @@protoc_insertion_point(class_scope:StatusResponse)
  })
_sym_db.RegisterMessage(StatusResponse)



_PEER = _descriptor.ServiceDescriptor(
  name='Peer',
  full_name='Peer',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=211,
  serialized_end=427,
  methods=[
  _descriptor.MethodDescriptor(
    name='getSuccessor',
    full_name='Peer.getSuccessor',
    index=0,
    containing_service=None,
    input_type=_GETSUCCESSOR,
    output_type=_PEERRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='getPredecessor',
    full_name='Peer.getPredecessor',
    index=1,
    containing_service=None,
    input_type=_GETPREDECESSOR,
    output_type=_PEERRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='updatePredecessor',
    full_name='Peer.updatePredecessor',
    index=2,
    containing_service=None,
    input_type=_NOTIFYPREDECESSOR,
    output_type=_STATUSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='findSuccessor',
    full_name='Peer.findSuccessor',
    index=3,
    containing_service=None,
    input_type=_FINDSUCCESSOR,
    output_type=_PEERRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_PEER)

DESCRIPTOR.services_by_name['Peer'] = _PEER

# @@protoc_insertion_point(module_scope)
