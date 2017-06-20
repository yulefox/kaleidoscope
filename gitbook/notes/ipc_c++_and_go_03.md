# gRPC 鉴权

gRPC 自建鉴权机制, 插入自定义鉴权系统, 如何使用 gRPC 鉴权.

## 概述

gRPC 设计了一系列鉴权机制, 以便可以安全使用 gRPC 与其他系统通信.

## 所支持的鉴权机制

- SSL/TLS: gRPC 整合了 SSL/TLS, 支持使用 SSL/TLS 进行服务端鉴权, 并对客户端与服务端的交换数据进行加密. 客户端也可以使用证书进行鉴权.

- Google 提供的基于令牌的鉴权: gRPC 提供了一套请求应答时附带元数据证书的通用机制. 在通过 gRPC 访问 Google API 时, 也需要获取访问令牌(通常是 OAuth2 令牌). Google 不允许非安全连接.

> 警告: Google 证书应仅用于连接 Google 服务. 向非 Google 服务发送 Google 的 OAuth2 令牌可能导致令牌泄露.

## 鉴权 API

gRPC 提供了基于证书(Credentials)的简单的鉴权 API. 可被用于创建 gRPC 通道或单次 gRPC 调用.

### 证书类型

- **通道证书** 附加到 `Channel` 上, 如 SSL 证书.
- **调用证书** 附加到 RPC 调用上(C++ 的 `ClientContext`).

上述证书可以组合至 `CompositeChannelCredentials`, 以 SSL 详细信息

### 使用客户端 SSL/TLS

客户端验证服务端, 加密所有通信数据.

```c++
// Create a default SSL ChannelCredentials object.
auto channel_creds = grpc::SslCredentials(grpc::SslCredentialsOptions());
// Create a channel using the credentials created in the previous step.
auto channel = grpc::CreateChannel(server_name, channel_creds);
// Create a stub on the channel.
std::unique_ptr<Greeter::Stub> stub(Greeter::NewStub(channel));
// Make actual RPC calls on the stub.
grpc::Status s = stub->sayHello(&context, *request, response);
```

### 使用 Google 令牌鉴权

```c++
auto creds = grpc::GoogleDefaultCredentials();
// Create a channel, stub and make RPC calls (same as in the previous example)
auto channel = grpc::CreateChannel(server_name, creds);
std::unique_ptr<Greeter::Stub> stub(Greeter::NewStub(channel));
grpc::Status s = stub->sayHello(&context, *request, response);
```

### gRPC 扩展其他鉴权机制

证书插件 API 运行开发者引入自定义证书类型:

- `MetadataCredentialsPlugin` 抽象类, 包含纯虚函数 `GetMetadata`, 需要在子类中被实现.

- `MetadataCredentialsFromPlugin` 函数, 基于 `MetadataCredentialsPlugin` 中创建一个 `CallCredentials`.

```c++
class MyCustomAuthenticator : public grpc::MetadataCredentialsPlugin {
 public:
  MyCustomAuthenticator(const grpc::string& ticket) : ticket_(ticket) {}

  grpc::Status GetMetadata(
      grpc::string_ref service_url, grpc::string_ref method_name,
      const grpc::AuthContext& channel_auth_context,
      std::multimap<grpc::string, grpc::string>* metadata) override {
    metadata->insert(std::make_pair("x-custom-auth-ticket", ticket_));
    return grpc::Status::OK;
  }

 private:
  grpc::string ticket_;
};

auto call_creds = grpc::MetadataCredentialsFromPlugin(
    std::unique_ptr<grpc::MetadataCredentialsPlugin>(
        new MyCustomAuthenticator("super-secret-ticket")));
```

更进一步, gRPC 允许开发者使用其他加解密机制替代 SSL/TLS.

## 示例

无加密:

```c++
auto channel = grpc::CreateChannel("localhost:50051", InsecureChannelCredentials());
std::unique_ptr<Greeter::Stub> stub(Greeter::NewStub(channel));
...
```

SSL/TLS 鉴权:

```c++
auto channel_creds = grpc::SslCredentials(grpc::SslCredentialsOptions());
auto channel = grpc::CreateChannel("myservice.example.com", creds);
std::unique_ptr<Greeter::Stub> stub(Greeter::NewStub(channel));
...
```

Google 鉴权:

```c++
auto creds = grpc::GoogleDefaultCredentials();
auto channel = grpc::CreateChannel("greeter.googleapis.com", creds);
std::unique_ptr<Greeter::Stub> stub(Greeter::NewStub(channel));
...
```