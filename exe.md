### docker
+ launch docker desktop
```
docker exec -it my-mysql bash
cd ~/share/
mysql -uroot -p123456 < 20240812220237.sql
```

### mysql
```
mysql -h 127.0.0.1 -uroot -p123456
```

### main
```
conda activate careerx
uvicorn main:app --host 0.0.0.0 --reload
```
- 在浏览器访问localhost:8000/docs查看API文档
- 开发人员本地开发登录账号：18888888888; 密码：123456
