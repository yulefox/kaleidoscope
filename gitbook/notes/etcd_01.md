# etcd 服务发现

插件式服务注册发现.

- 服务注册

- 服务发现

```go
func NewMaster(endpoints []string) {
	cfg := client.Config{
		Endpoints:			   endpoints,
		Transport:			   client.DefaultTransport,
		HeaderTimeoutPerRequest: time.Second,
	}
	etcdClient, err := client.New(cfg)
	if err != nil {
		log.Fatal("Error: cannot connec to etcd:", err)
	}
	master := &Master{
		members: make(map[string]*Member),
		KeysAPI: client.NewKeysAPI(etcdClient),
	}
	go master.WatchWorkers()
	return master
}
```

```go
func (m *Master) WatchWorkers() {
	api := m.KeysAPI
	watcher := api.Watcher("workers/", &client.WatcherOptions{
		Recursive: true,
	})
	for {
		res, err := watcher.Next(context.Background())
		if err != nil {
			log.Println("Error watch workers:", err)
			break
		}
		if res.Action == "expire" {
			member, ok := m.members[res.Node.Key]
			if ok {
				member.InGroup = false
			}
		} else if res.Action == "set" || res.Action == "update"{
			info := &WorkerInfo{}
			err := json.Unmarshal([]byte(res.Node.Value), info)
			if err != nil {
				log.Print(err)
			}
			if _, ok := m.members[info.Name]; ok {
				m.UpdateWorker(info)
			} else {
				m.AddWorker(info)
			}
		} else if res.Action == "delete" {
			delete(m.members, res.Node.Key)
		}
	}
}
```