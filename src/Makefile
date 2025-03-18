startRedisContainer:
	docker start redis-stack-server

startRedis:
	docker exec -it redis-stack-server redis-cli

stopRedisContainer:
	docker stop redis-stack-server

benchmarkGETSET:
	redis-benchmark -t SET,GET -q -n 100000

clearRedisBackup:
	> src/backup.txt

startClient:
	python Client.py

startRedisServer:
	python RedisServer.py