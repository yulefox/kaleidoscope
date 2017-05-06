package main

import (
	"log"

	"os"
	"os/signal"

	"fmt"

	"github.com/Shopify/sarama"
)

func main() {
	//consumer, err := sarama.NewConsumer([]string{"192.168.1.130:9092"}, nil)
	consumer, err := sarama.NewConsumer([]string{"yulefox.com:9092"}, nil)
	//consumer, err := sarama.NewConsumer([]string{"139.162.126.168:9092"}, nil)
	//consumer, err := sarama.NewConsumer([]string{"localhost:9092"}, nil)
	if err != nil {
		panic(err)
	}
	defer func() {
		if err := consumer.Close(); err != nil {
			log.Fatalln(err)
		}
	}()

	partitionConsumer, err := consumer.ConsumePartition("test", 0, 0)
	if err != nil {
		panic(err)
	}
	defer func() {
		if err := partitionConsumer.Close(); err != nil {
			log.Fatalln(err)
		}
	}()

	signals := make(chan os.Signal, 1)
	signal.Notify(signals, os.Interrupt)

	consumed := 0
ConsumerLoop:
	for {
		select {
		case msg := <-partitionConsumer.Messages():
			log.Printf("Consumed %d: %s\n", msg.Offset, string(msg.Value))
			consumed++
		case <-signals:
			fmt.Println("exit")
			break ConsumerLoop
		}
	}
	log.Printf("Consumed: %d\n", consumed)
}
