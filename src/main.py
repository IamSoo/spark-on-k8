from pyspark.sql.session import SparkSession


def spark_session():
    session = (
        SparkSession.builder.master("local").appName("spark-on-minikube").getOrCreate()
    )
    return session


def generate_df(spark):
    data = [
        ("James", "", "Smith", "1991-04-01", "M", 3000),
        ("Michael", "Rose", "", "2000-05-19", "M", 4000),
        ("Robert", "", "Williams", "1978-09-05", "M", 4000),
        ("Maria", "Anne", "Jones", "1967-12-01", "F", 4000),
        ("Jen", "Mary", "Brown", "1980-02-17", "F", -1),
    ]
    columns = ["firstname", "middlename", "lastname", "dob", "gender", "salary"]
    df = spark.createDataFrame(data=data, schema=columns)
    return df


def run():
    spark = spark_session()
    df = generate_df(spark)
    emp_count = df.filter(df.salary == 4000).select("firstname").count()
    print(f"Total employees with 4000 salary are {emp_count}")
    spark.stop()


if __name__ == "__main__":
    run()
