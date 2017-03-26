KeepCoding Django

# Install

make install

# Development server

make start

# httpie

``` bash
http -v -f POST http://127.0.0.1:8000/api/v1/user/ email=user.name@example.com password=basicsecret is_admin=False
echo -ne "user.name@example.com:basicsecret" | base64 --wrap 0
http -v -f GET http://127.0.0.1:8000/api/v1/user/user.name@example.com/ 'Authorization: Basic dXNlci5uYW1lQGV4YW1wbGUuY29tOmJhc2ljc2VjcmV0'
http -v -f PATCH http://127.0.0.1:8000/api/v1/user/user.name@example.com/ email=user.name@example.com is_admin=True 'Authorization: Basic dXNlci5uYW1lQGV4YW1wbGUuY29tOmJhc2ljc2VjcmV0'
http -v -f DELETE http://127.0.0.1:8000/api/v1/user/user.name@example.com/ 'Authorization: Basic dXNlci5uYW1lQGV4YW1wbGUuY29tOmJhc2ljc2VjcmV0'
```

## create user

```bash
http -v -f POST http://127.0.0.1:8000/api/v1/user/ email=user.name@example.com password=basicsecret is_admin=False
```

## create post

```bash
http -v -f POST http://127.0.0.1:8000/api/v1/post/ title=NewPostTitle owner='user.name@example.com'
```
