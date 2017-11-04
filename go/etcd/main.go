package main

import (
	"fmt"

	"github.com/coreos/etcd"
)

func main() {
	fmt.Println("hello")

	client := etcd.NewClient()
}
