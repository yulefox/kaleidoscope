# 通信协议

[HTTP/2](https://tools.ietf.org/html/rfc7540)

[ABNF](https://tools.ietf.org/html/rfc5234)

## 大纲

gRPC 请求应答消息流的一般顺序:

- 请求 → 请求报头 *有定界符的消息 EOS
- 应答 → (应答报头 *有定界符的消息 跟踪消息) / 仅跟踪时

## 请求

- 请求 → 请求报头 *有定界符的消息 EOS

请求报头以报头+连续帧的格式作为 HTTP2 报头发送.

- **Request-Headers** → Call-Definition *Custom-Metadata
- **Call-Definition** → Method Scheme Path TE \[Authority] \[Timeout] \[Content-Type] \[Message-Type] \[Message-Encoding] \[Message-Accept-Encoding] \[User-Agent]
- **Method** → “:method POST”
- **Scheme** → “:scheme ” (“http” / “https”)
- **Path** → “:path” “/” Service-Name “/” {method name} # But see note below.
- **Service-Name** → {IDL-specific service name}
- **Authority** → “:authority” {virtual host name of authority}
- **TE** → “te” “trailers” # Used to detect incompatible proxies
- **Timeout** → “grpc-timeout” TimeoutValue TimeoutUnit
- **TimeoutValue** → {positive integer as ASCII string of at most 8 digits}
- **TimeoutUnit** → Hour / Minute / Second / Millisecond / Microsecond / Nanosecond
- **Hour** → “H”
- **Minute** → “M”
- **Second** → “S”
- **Millisecond** → “m”
- **Microsecond** → “u”
- **Nanosecond** → “n”
- **Content-Type** → “content-type” “application/grpc” [(“+proto” / “+json” / {custom})]
- **Content-Coding** → “gzip” / “deflate” / “snappy” / {custom}
- **Message-Encoding** → “grpc-encoding” Content-Coding
- **Message-Accept-Encoding** → “grpc-accept-encoding” Content-Coding *(“,” Content-Coding)
- **User-Agent** → “user-agent” {structured user-agent string}
- **Message-Type** → “grpc-message-type” {type name for message schema}
- **Custom-Metadata** → Binary-Header / ASCII-Header
- **Binary-Header** → {lowercase ASCII header name ending in “-bin” } {base64 encoded value}
- **ASCII-Header** → {lowercase ASCII header name} {value}

- **Delimited-Message** → Compressed-Flag Message-Length Message
- **Compressed-Flag** → 0 / 1 # encoded as 1 byte unsigned integer
- **Message-Length** → {length of Message} # encoded as 4 byte unsigned integer
- **Message** → *{binary octet}


## 应答


- **Response** → (Response-Headers *Delimited-Message Trailers) / Trailers-Only
- **Response-Headers** → HTTP-Status [Message-Encoding] [Message-Accept-Encoding] Content-Type *Custom-Metadata
- **Trailers-Only** → HTTP-Status Content-Type Trailers
- **Trailers** → Status [Status-Message] *Custom-Metadata
- **HTTP-Status** → “:status 200”
- **Status** → “grpc-status”
- **Status-Message** → “grpc-message”

## 示例

Sample unary-call showing HTTP2 framing sequence

### Request

```
HEADERS (flags = END_HEADERS)
:method = POST
:scheme = http
:path = /google.pubsub.v2.PublisherService/CreateTopic
:authority = pubsub.googleapis.com
grpc-timeout = 1S
content-type = application/grpc+proto
grpc-encoding = gzip
authorization = Bearer y235.wef315yfh138vh31hv93hv8h3v

DATA (flags = END_STREAM)
<Delimited Message>
```

### Response

HEADERS (flags = END_HEADERS)
:status = 200
grpc-encoding = gzip

DATA
<Delimited Message>

HEADERS (flags = END_STREAM, END_HEADERS)
grpc-status = 0 # OK
trace-proto-bin = jher831yy13JHy3hc

## User Agents

While the protocol does not require a user-agent to function it is recommended that clients provide a structured user-agent string that provides a basic description of the calling library, version & platform to facilitate issue diagnosis in heterogeneous environments. The following structure is recommended to library developers:

```
User-Agent → “grpc-” Language ?(“-” Variant) “/” Version ?( “ (“  *(AdditionalProperty “;”) “)” )
```

E.g.

```
grpc-java/1.2.3
grpc-ruby/1.2.3
grpc-ruby-jruby/1.3.4
grpc-java-android/0.9.1 (gingerbread/1.2.4; nexus5; tmobile)
```

## HTTP2 Transport Mapping

### Stream Identification

All GRPC calls need to specify an internal ID. We will use HTTP2 stream-ids as call identifiers in this scheme. NOTE: These ids are contextual to an open HTTP2 session and will not be unique within a given process that is handling more than one HTTP2 session nor can they be used as GUIDs.

### Data Frames

DATA frame boundaries have no relation to Delimited-Message boundaries and implementations should make no assumptions about their alignment.

### Errors

When an application or runtime error occurs during an RPC a Status and Status-Message are delivered in Trailers.

In some cases it is possible that the framing of the message stream has become corrupt and the RPC runtime will choose to use an RST_STREAM frame to indicate this state to its peer. RPC runtime implementations should interpret RST_STREAM as immediate full-closure of the stream and should propagate an error up to the calling application layer.

The following mapping from RST_STREAM error codes to GRPC error codes is applied.

| HTTP2 Code | GRPC Code |
| ---------- |:---------:|
| NO_ERROR(0) | INTERNAL - An explicit GRPC status of OK should have been sent but this might be used to aggressively lameduck in some scenarios. |
| PROTOCOL_ERROR(1) | INTERNAL |
| INTERNAL_ERROR(2) | INTERNAL |
| FLOW_CONTROL_ERROR(3) | INTERNAL |
| SETTINGS_TIMEOUT(4) | INTERNAL |
| STREAM_CLOSED | No mapping as there is no open stream to propagate to. Implementations should log. |
| FRAME_SIZE_ERROR | INTERNAL |
| REFUSED_STREAM | UNAVAILABLE - Indicates that no processing occurred and the request can be retried, possibly elsewhere. |
| CANCEL(8) | Mapped to call cancellation when sent by a client. Mapped to CANCELLED when sent by a server. Note that servers should only use this mechanism when they need to cancel a call but the payload byte sequence is incomplete. |
| COMPRESSION_ERROR | INTERNAL |
| CONNECT_ERROR | INTERNAL |
| ENHANCE_YOUR_CALM | RESOURCE_EXHAUSTED … with additional error detail provided by runtime to indicate that the exhausted resource is bandwidth. |
| INADEQUATE_SECURITY | PERMISSION_DENIED … with additional detail indicating that permission was denied as protocol is not secure enough for call. |

### Security

The HTTP2 specification mandates the use of TLS 1.2 or higher when TLS is used with HTTP2. It also places some additional constraints on the allowed ciphers in deployments to avoid known-problems as well as requiring SNI support. It is also expected that HTTP2 will be used in conjunction with proprietary transport security mechanisms about which the specification can make no meaningful recommendations.

Connection Management

GOAWAY Frame

Sent by servers to clients to indicate that they will no longer accept any new streams on the associated connections. This frame includes the id of the last successfully accepted stream by the server. Clients should consider any stream initiated after the last successfully accepted stream as UNAVAILABLE and retry the call elsewhere. Clients are free to continue working with the already accepted streams until they complete or the connection is terminated.

Servers should send GOAWAY before terminating a connection to reliably inform clients which work has been accepted by the server and is being executed.

PING Frame

Both clients and servers can send a PING frame that the peer must respond to by precisely echoing what they received. This is used to assert that the connection is still live as well as providing a means to estimate end-to-end latency. If a server initiated PING does not receive a response within the deadline expected by the runtime all outstanding calls on the server will be closed with a CANCELLED status. An expired client initiated PING will cause all calls to be closed with an UNAVAILABLE status. Note that the frequency of PINGs is highly dependent on the network environment, implementations are free to adjust PING frequency based on network and application requirements.

Connection failure

If a detectable connection failure occurs on the client all calls will be closed with an UNAVAILABLE status. For servers open calls will be closed with a CANCELLED status.

Appendix A - GRPC for Protobuf

The service interfaces declared by protobuf are easily mapped onto GRPC by code generation extensions to protoc. The following defines the mapping to be used.

- **Service-Name** → ?( {proto package name} “.” ) {service name}
- **Message-Type** → {fully qualified proto message name}
- **Content-Type** → “application/grpc+proto”
