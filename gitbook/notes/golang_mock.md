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
mockgen sample/something MyInterface \
  > sample/mock_something/mock_something.go
```

```go
// Automatically generated by MockGen. DO NOT EDIT!
// Source: something (interfaces: MyInterface)

package mock_something

import (
	gomock "github.com/golang/mock/gomock"
)

// Mock of MyInterface interface
type MockMyInterface struct {
	ctrl     *gomock.Controller
	recorder *_MockMyInterfaceRecorder
}

// Recorder for MockMyInterface (not exported)
type _MockMyInterfaceRecorder struct {
	mock *MockMyInterface
}

func NewMockMyInterface(ctrl *gomock.Controller) *MockMyInterface {
	mock := &MockMyInterface{ctrl: ctrl}
	mock.recorder = &_MockMyInterfaceRecorder{mock}
	return mock
}

func (_m *MockMyInterface) EXPECT() *_MockMyInterfaceRecorder {
	return _m.recorder
}

func (_m *MockMyInterface) SomeMethod(x int64, y string) {
	_m.ctrl.Call(_m, "SomeMethod", x, y)
}

func (_mr *_MockMyInterfaceRecorder) SomeMethod(arg0, arg1 interface{}) *gomock.Call {
	return _mr.mock.ctrl.RecordCall(_mr.mock, "SomeMethod", arg0, arg1)
}
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

缺省情况下, 对 mock **期望**的多次调用, 不会限定为按照特定顺序运行, 调用顺序依赖可以通过 `InOrder` 及/或 `Call.After` 限定. `Call.After` 可以创建多样的顺序依赖, 而 `InOrder` 则更加简便.

**期望** 是 mock 对象的一个实例.

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

### func InOrder

```go
func InOrder(calls ...*Call)
```

`InOrder` 声明了给定调用应依照顺序执行

### type Call

```go
type Call struct {
    // contains filtered or unexported fields
}
```

`Call` 表示对 mock 的期望的调用

### func (*Call) After

```go
func (c *Call) After(preReq *Call) *Call
```

`After` 指示该调用仅当 `preReq` 执行完毕后才被执行

### func (*Call) AnyTimes

```go
func (c *Call) AnyTimes() *Call
```

`AnyTimes` 允许该期望被调用 0 或多次

### func (*Call) Do

```go
func (c *Call) Do(f interface{}) *Call
```

`Do` 指示调用执行完毕后的动作, 带有一个 `interface{}` 参数, 以支持多元函数.

### func (*Call) MaxTimes

```go
func (c *Call) MaxTimes(n int) *Call
```

`MaxTimes` 限定调用的最大执行次数为 `n`. 如果 `AnyTimes` 或 `MinTimes` 未被调用, `MaxTimes` 将设定调用次数的最小值为 `0`.

### func (*Call) MinTimes

```go
func (c *Call) MinTimes(n int) *Call
```

`MinTimes` 指定调用的最小执行次数为 `n`. 如果 `AnyTimes` 或 `MaxTimes` 未被调用, `MinTimes` 将设定调用次数的最大值为无限(`1e8`).

### func (*Call) Return

```go
func (c *Call) Return(rets ...interface{}) *Call
```

### func (*Call) SetArg

```go
func (c *Call) SetArg(n int, value interface{}) *Call
```

`SetArg` 间接通过指针指定第 `n` 个参数的值

### func (*Call) String

```go
func (c *Call) String() string
```

### func (*Call) Times

```go
func (c *Call) Times(n int) *Call
```

### type Controller

```go
type Controller struct {
    // contains filtered or unexported fields
}
```

`Controller` 表示 mock 生态系统中的顶层控制. 定义了 mock 对象的作用域, 生命周期及其期望. 对 `Controller`方法的调用是协程安全的.

### func NewController

```go
func NewController(t TestReporter) *Controller
```

### func (*Controller) Call

```go
func (ctrl *Controller) Call(receiver interface{}, method string, args ...interface{}) []interface{}
```

### func (*Controller) Finish

```go
func (ctrl *Controller) Finish()
```

### func (*Controller) RecordCall

```go
func (ctrl *Controller) RecordCall(receiver interface{}, method string, args ...interface{}) *Call
```

### type Matcher

```go
type Matcher interface {
    // Matches returns whether y is a match.
    Matches(x interface{}) bool

    // String describes what the matcher matches.
    String() string
}
```

`Matcher` 表示一类值. 向 mock 方法提供合法值或期望值.

### func Any

```go
func Any() Matcher
```

### func Eq

```go
func Eq(x interface{}) Matcher
```

### func Nil

```go
func Nil() Matcher
```

### func Not

```go
func Not(x interface{}) Matcher
```

### type TestReporter

```go
type TestReporter interface {
    Errorf(format string, args ...interface{})
    Fatalf(format string, args ...interface{})
}
```

`TestReporter` 可以报告测试失败结果. 支持标准库的 `testing.T`.