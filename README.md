# Spark on Kubernetes
### Why Spark on Kubernetes(K8s)
Spark has been a de-facto big data processing tool with a lot of popularity in Apache open source community. As spark runs in a cluster i.e with few nodes, it needs a cluster manager. So spark supports standalone option with cluster managers like YARN, Mesos. 

The evolution of containerization of application programs has benefited us in several ways like making the code base portable, packaging the code and the dependencies together so that the application exhibits similar behaviour irrespective of OS and 
this is also applied to Spark programs. Spark programs can also be containerized and run as a container. Spark released the K8s cluster support in 2018 adding another cluster manager support to the list.

Here, we will build and run a small spark application and run it on local k8(minikube) and a k8 cluster in a cloud environment step by step.

### Steps to build and deploy on spark on job local
#### Background
K8 understands and runs containers. So we need to build a container(Docker) which will wrap our code and spark executables together. Spark has a docker file that can help us to build the base image and using that base image we will build our application
code. Follow the steps to build the images

#### Download the spark on your machine
You can download the latest spark source code from here https://spark.apache.org/downloads.html or any other versions based on your preferences from here https://archive.apache.org/dist/spark/

#### Build the base image
We are going to write a small pyspark application, but you can write any in Java or Scala. The approach will be same. Go to the spark source downloaded folder and use the following command to build the
```
./bin/docker-image-tool.sh \
-p kubernetes/dockerfiles/spark/bindings/python/Dockerfile \
build
```
Find the image and tag it and push it to your repo if you want to use it in the future.
```
docker images
docker tag <image-id> iamsoo/spark-py:v3.3.0
docker push iamsoo/spark-py:v3.3.0
```
Now the base image has been build, we need to write our application program. The main.py contains a simple basic pyspark code that does a filter and count of employees getting a salary. The pyspark program does not run on huge volume of data as we are not 
very much interested in pyspark here rather on how to run it on k8.

The next step is to build the docker container of our application using the base image that we built above.
Follow the below command to build the app.

```commandline
docker build -t iamsoo/pyspark-app .
docker push iamsoo/pyspark-app
```
Now the containerization part is done. From now onwards its all about deployment into k8s. We can create a cluster in a cloud environment or we can install minikube which is like small k8 cluster on the local machine.
Minikube has a very good set of documentation. Follow https://minikube.sigs.k8s.io/docs/start/ and install it on the local machine.

Once minikube is installed, in the terminal type the following command to see the status.
```commandline
minikube status
```
Spark needs atleast 2 CPUs and a RAM limit, otherwise the jobs will fail. We can set these values while creating the minikube cluster so that our programs run smoothly.
Now we will create a spark cluster with cpu and memory limit, create a namespace where we will run our spark pods. We will also create a service account and cluster role binding which will give the service account set of permissions 
to create pods in the namespace.

Type the following command to do so
```commandline
minikube --memory 2200 --cpus 2 start
kubectl create namespace spark

kubectl create serviceaccount spark-service-account --namespace spark
kubectl create clusterrolebinding spark-role-binding --clusterrole=edit --serviceaccount=spark:spark-service-account --namespace=spark
```
With the above command, we are creating a namespace "spark", and a service account "spark-service-account", which will have permissions to operate in the cluster.
Now we have everything ready to run our pyspark program as a POD in k8s. We need to submit the container information to spark, which will create a driver program inside a pod and then spawn workers in other different pods.
Once the POD starts, we can go ahead and check the minikube dashboard or use kubectl command to explore the status of the pod.

Run the following command to submit the job to minikube. We need know the API server address in order to submit the job. To know the API server details we can type the following command.

```commandline
kubectl cluster-info
```
We use the above value and pass it as --master argument in the below command

```commandline
./bin/spark-submit \
--master k8s://https://127.0.0.1:54914 \
--deploy-mode cluster \
--conf spark.kubernetes.driver.container.image=iamsoo/pyspark-app:latest \
--conf spark.kubernetes.executor.container.image=iamsoo/pyspark-app:latest \
--conf spark.kubernetes.namespace=spark \
--conf spark.kubernetes.authenticate.driver.serviceAccountName=spark-service-account \
local:///opt/application/main.py
```
Open minikube dashboard to check the status of the POD.