# Spark on Kubernetes
### Why Spark on Kubernetes(K8s)
Spark has been a de-facto big data processing tool with a lot of popularity in Apache open source community. As spark runs in a cluster i.e with few nodes,it needs a cluster manager.So spark supports standalone option with cluster managers like YARN, Mesos. 

The evolution of containerization of application programs has benefited us in several ways like making code base portable, packaging the code and the dependencies together so that the application exhibits similar behaviour irrespective of OS.
This is also applied to Spark programs. Spark released the K8s cluster support in 2018 adding another cluster manager support to the list.

Here we will build and run a small spark application and run it on local k8(minikube) and a k8 cluster in a cloud environment.

### Steps to build and deploy on spark on job local
#### Background
K8 understands and runs containers. So we need build a container(Docker) which will wrap our code and spark executables together. Spark has a docker file that can help us to build the base image and using that base image we will build our application
code. Follow the steps to build the images

#### Download the spark on your machine
You can download the latest spark from here https://spark.apache.org/downloads.html or any other versions based on your preferences from here https://archive.apache.org/dist/spark/

#### Build the base image
We are going to write a small pyspark application, but you can write any in Java or Scala. The approach will be same. Go to the downloaded folder and use the following command to build the
```build the image
./bin/docker-image-tool.sh \
-p kubernetes/dockerfiles/spark/bindings/python/Dockerfile \
build
```

```find the image and tag it and push it to your repo if you want to use it in future.
docker images
docker tag a3a6ad92d44e iamsoo/spark-py:v3.3.0
docker push iamsoo/spark-py:v3.3.0
```


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

