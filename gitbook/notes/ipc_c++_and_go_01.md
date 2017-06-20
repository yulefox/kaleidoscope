# gRPC 介绍与安装

## gRPC 概述

[gRPC](http://www.grpc.io/) 的客户端应用可以直接调用不同机器上服务端应用的方法, 如同调用本地对象一样, 使得创建分布式应用和服务变得更加容易. 同很多 RPC 系统类似, gRPC 定义服务, 提供可以被远程调用的方法, 这些方法可以有自己的参数和返回类型. 服务端实现这些方法并运行 gRPC 服务以处理客户端调用, 客户端则提供与服务端方法对应的桩模块.

![gRPC](/assets/notes/grpc_landing.svg)

gRPC 客户端与服务端可以运行在多种环境下并可彼此通信, 客户端与服务端可以使用 gRPC 支持的不同的编程语言分别实现. 另外, 最新的 Google API 将提供 gRPC 版本, 供使用者将这些 Google 的功能集成到自己的应用中.

### 使用 Protocol Buffer

gRPC 默认使用 [protobuf](https://developers.google.com/protocol-buffers/docs/overview)(也可使用其他数据格式如 *JSON* 等)作为接口定义语言(Interface Definition Language, IDL).

首先, 定义序列化的数据结构(`.proto`). protobuf 的数据称作*消息(message)*, 每个消息包含一系列称作*域(field)*的键值对, 示例:

```protobuf
message Person {
    string name = 1;
    int32 id = 2;
    bool has_ponycopter = 3;
}
```

接下来, 使用编译器 `protoc` 生成相应语言(*C++*, *Go*, *Python* 等)的*数据访问类(data access class)*及序列化/解析方法等. 以 C++ 为例, 前例将生成 `Person` 类, 可在 C++ 代码中通过该类使用, 序列化及操作前面定义的 `Person` 消息.

来看一个定义了 gRPC 服务的 protobuf 消息:

```protobuf
// The greeter service definition.
Service Greeter {
    // Send a greeting
    rpc SayHello (HelloRequest) returns (HelloResponse) {}

// The request message containing the user's name.
Message HelloRequest {
    string name = 1;
}

// The response message containing the greetings.
Message HelloResponse {
    string message = 1;
}
```

gRPC 同样使用 `protoc` 生成相应代码, 只需使用 gRPC 插件即可.

### Protocol buffer 版本

推荐使用最新的 proto3 版本, proto3 使用更加简单的语法, 并新引入一些有用的特性, 支持更多的语言.

## 安装 gRPC

虽非强制, 但 gRPC 通常使用 proto3 作为服务定义和数据序列化的协议格式. gRPC [源码安装步骤](https://github.com/grpc/grpc/blob/master/INSTALL.md)如下.

### Linux(Ubuntu)

```sh
sudo apt-get install build-essential autoconf libtool
sudo apt-get install pkg-config
sudo apt-get install libgflags-dev libgtest-dev
sudo apt-get install clang libc++-dev
```

### macOS

需安装 Xcode 或 Xcode 的命令行工具.

```sh
sudo code-select --install
brew install autoconf automake libtool shtool
brew install gflags
LIBTOOL=glibtool LIBTOOLIZE=glibtoolize make
```

### 源码构建

```sh
# install protoc
git clone -b $(curl -L http://grpc.io/release) https://github.com/grpc/grpc
cd grpc
git submodule update --init
make
sudo make install

# install protobuf
cd third_party/protobuf
./autogen.sh
./configure
make
sudo make install

# build the example
cd examples/cpp/helloworld/
make

# run the server example
./greeter_server

# run the client example
./greeter_client
```