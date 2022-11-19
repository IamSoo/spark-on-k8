# Spark on Kubernetes
### Why Spark on Kubernetes


### Steps to build and deploy on spark on job local





./bin/docker-image-tool.sh \
-p kubernetes/dockerfiles/spark/bindings/python/Dockerfile \
build

docker images
docker tag a3a6ad92d44e iamsoo/spark-py:v3.3.0
docker push iamsoo/spark-py:v3.3.0


docker build -t iamsoo/pyspark-app .




./bin/spark-submit \
--master k8s://https://127.0.0.1:54914 \
--deploy-mode cluster \
--conf spark.kubernetes.driver.container.image=iamsoo/pyspark-app:latest \
--conf spark.kubernetes.executor.container.image=iamsoo/pyspark-app:latest \
--conf spark.kubernetes.namespace=spark \
--conf spark.kubernetes.authenticate.driver.serviceAccountName=spark-service-account \
local:///opt/application/main.py



minikube --memory 2200 --cpus 2 start
kubectl create namespace spark

kubectl create serviceaccount spark-service-account --namespace spark
kubectl create clusterrolebinding spark-role-binding --clusterrole=edit --serviceaccount=spark:spark-service-account --namespace=spark

