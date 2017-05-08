# Swagger

## 部署

- Swagger-UI

```sh
docker pull swaggerapi/swagger-ui
docker run -p 80:8080 swaggerapi/swagger-ui
```

- Swagger-Editor

```sh
docker pull swaggerapi/swagger-editor  
docker run -p 5000:8080 swaggerapi/swagger-editor
```

## 编写

- yaml
- json

swagger.yaml
swagger.json

## 生成

基于 yaml/json 生成 echo 可用代码.
