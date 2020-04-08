## Data Streaming Nanodegree
##### Final Project: Analisys San Francisco crime incidentes using Apache Spark Structured Streaming

##### What I used in my enviroment?

I mounted the enviroment using docker-compose (versioned in the project), because of the fresh restart 
hability that I gain. I used spark 2.4.5 and the kafka 5.2.2, the same of the first module of this course.

##### Dificulties ?

I found some parts of the project very confusing and dificult to understand, sometimes I caught myself struggling
to understand what you want from me beyond of the technical aspects of solution. Until now I dont 
understand what you really whant with the TODO "count the number of original crime type". I assumed something and
have gone ahead. I disregarded agrouping the information in a window, because the exercise didn't request.

##### Screenshots

###### Take a screenshot of your progress reporter after executing a Spark job

[progress_reporter.png](./progress_reporter.png)

###### Take a screenshot of the Spark Streaming UI as the streaming continues

[spark_streaming_ui.png](./spark_streaming_ui.png) 

##### Questions

###### How did changing values on the SparkSession property parameters affect the throughput and latency of the data?

I read the documentation to discover all possible parameters to configure my spark session. While I was reading I tried
to identify what parameters can affect troughput and the latency. The options that could have more impact on this 
properties, and it's a hunch, are listed bellow. I included the summing up of the property effect on the sparksession. 
In our example I really don't believe that these parameters gonna make much difference, because we are running locally 
with a small dataset being produced just once per second.

*https://spark.apache.org/docs/latest/configuration.html*

**spark.executor.cores**
The number of cores to use on each executor.

**spark.default.parallelism**
Default number of partitions in RDDs returned by transformations like join, reduceByKey, and parallelize when not set by user.

**spark.streaming.backpressure.enabled**
This enables the Spark Streaming to control the receiving rate based on the current batch scheduling delays and processing times so that the system receives only as fast as the system can process.

**spark.streaming.kafka.maxRatePerPartition**
Maximum rate (number of records per second) at which data will be read from each Kafka partition when using the new Kafka direct stream API. 

###### What were the 2-3 most efficient SparkSession property key/value pairs? Through testing multiple variations on values, how can you tell these were the most optimal?

As I imagened it's very dificultie to observe a lot of difference because of the low load over spark. However simulating a lot of changes among the parameters upside, It was possible to observe a difference in "processedRowsPerSecond", even in this simulation scenario.

The biggest variation in "processedRowsPerSecond" was observed when I increased the config spark.default.parallelism, the number that I defined in the end of tests was **36**, 3 times more than the number of cores in my machine.

It's obvious that the number of cores influence in throughput. By default, in local mode, spark uses all cores in machine, but decreasing the value as well descrease the "processedRowsPerSecond".

When i figured out in docs the parameter "spark.streaming.backpressure.enabled", I thought that this parameter would made
a lot of difference. In our example, I can't observe this. However I still thinking that this parameter should be
very useful, because it's able to force spark the control the streaming flow of received date. Despite that, I was able
to observe some increase in the "processedRowsPerSecond" when I enabled this parameter. Moreover, the parameter 
"spark.streaming.kafka.maxRatePerPartition" is very important to control the max number of processed messages
from kafka, in a streaming application. The parameter "spark.streaming.backpressure.enabled" use this parameter
as reference to the maximum value that can be processed.



