from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import DateType
import seaborn as sns
import matplotlib.pyplot as plt

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

df =    spark.read \
    .option("multiline", "true")\
      .option("quote", '"')\
      .option("header", "true")\
      .option("escape", "\\")\
      .option("escape", '"')\
    .csv("ct_data.csv")
#df.show()
df = df.withColumn("Post Created Date", col("Post Created Date").cast(DateType()))
df = df.na.drop(subset=["Post Created Date"])
#df.select("Page Name", "User Name", "Facebook Id", "Page Category", "Page Admin Top Country","Post Created Date").orderBy("Post Created Date").show()
counted_posts_by_date = df.groupBy("Post Created Date").count().orderBy("Post Created Date")

#print(df.dtypes)
#df.show()
counted_posts_by_date.show()

counted_posts_by_date.write.csv("count_posts_date.csv")

#pd_counted_dates = counted_posts_by_date.toPandas()
#print(pd_counted_dates)
#counted_posts_by_date.to_csv("count_posts_date.csv")

"""


number_of_elements_in_dataframes = 20
partitions = len(pd_counted_dates.index)//number_of_elements_in_dataframes

splited_df = [pd_counted_dates.iloc[(i-1)*number_of_elements_in_dataframes:i*number_of_elements_in_dataframes] for i in range(1, partitions-1)]

for df in splited_df:
    ax = sns.barplot(x = "Post Created Date", y = "count", data = df)
    plt.title(f"Timeline from {df['Post Created Date'].iloc[0]} to {df['Post Created Date'].iloc[-1]}")
    plt.savefig(f"Timeline from {df['Post Created Date'].iloc[0]} to {df['Post Created Date'].iloc[-1]}")
"""

