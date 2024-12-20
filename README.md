

# Generate Proto

```bash
python -m grpc_tools.protoc -I=./src/protos --python_out=./src/rpc/user --pyi_out=./src/rpc/user --grpc_python_out=./src/rpc/user ./src/protos/user.proto
```