## glide

包管理

## testing

测试

## mock

模拟环境, 下文直接使用 *mock*.

```go
import "github.com/golang/mock/gomock"
```

GoMock - 基于 Go 的 mock 框架.

标准用法:

1) 定义需要 mock 的接口:

```go
type MyInterface interface {
    SomeMethod(x int64, y string)
}
```

2) 使用 mockgen 为接口生成 mock:

```sh
    mockgen -source something/something.go -destination mock_something.go
```

3) 在 test 中使用该 mock:

```go
func TestMyThing(t *testing.T) {
    mockCtrl := gomock.NewController(t)
    defer mockCtrl.Finish()

    mockObj := NewMockMyInterface(mockCtrl)
    mockObj.EXPECT().SomeMethod(4, "blah")
}
```

缺省情况下, 对 `mock` 方法的多次调用, 不会限定为按照特定顺序运行, 调用顺序依赖可以通过 `InOrder` 及/或 `Call.After` 限定. `Call.After` 可以创建多样的顺序依赖, 而 `InOrder` 则更加简便.

下面的示例创建了相同的调用顺序依赖.

`Call.After` 示例:

```go
firstCall := mockObj.EXPECT().SomeMethod(1, "first")
secondCall := mockObj.EXPECT().SomeMethod(2, "second").After(firstCall)
mockObj.EXPECT().SomeMethod(3, "third").After(secondCall)
```

`InOrder` 示例:

```go
gomock.InOrder(
    mockObj.EXPECT().SomeMethod(1, "first"),
    mockObj.EXPECT().SomeMethod(2, "second"),
    mockObj.EXPECT().SomeMethod(3, "third"),
)
```

可以看到: `InOrder` 将依照给定顺序依次运行, 而 `Call.After` 只是约定了两个调用间的依赖关系.

TODO:

    处理不同参数/返回类型(如: ..., chan, map, interface)

## protobuf

协议

## grpc

远程调用

## swagger

- [x] API 设计
- [ ] API 设计

## API

- 使用 **protobuf** 定义数据及 API 协议
- 使用 **swagger** 生成 API 及文档
- 使用 **mock** 搭建模拟环境
- 使用 **test** 完成模拟测试
- 实现 API
- 使用 **test** 完成真实测试(单元测试/压力测试)
