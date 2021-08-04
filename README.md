# ElasticSearch Indexing and Querying
Made by Luke McFadden

**What it does & requirements to run**

 This program was written with the intention of connecting to a online client of ElasticSearch. This means any usage of this program requires you to input your own valid account credentials for the program to successfully connect to the ElasticSearch site. Specifically, lines 14 needs your ElasticSearch account password, and line 18 needs the specific project endpoint. Further instructions are included within the code.

Three .json files are included as to provide examples of how the format of .json files should be so that this program can properly utilize them. Your own .json files may be added, just make sure they adhere to the format of the included .json files. Both the _index_and_queries.py_ file and all .json files you want to index should exist within the same directory.
 
Upon startup, you are asked if you would like to index your .json files; you can skip straight to querying if no indexing is needed. If you choose to index, you're also asked if you want to delete the current exisitng index; if no is chosen, new .json files not currently indexed will simply be added to the existing index. 
 
When performing the "Top 10 ranking", the program queries ElasticSearch to search through the index for documents which are the most relevant to the inputted word or phrase. 
Up to 10 documents and their scores will be returned - less than 10 documents can be returned if fewer than 10 documents were found relevant. 0 documents can also be returned if ElasticSearch found no documents were relevant to the word or phrase.

Returned relevant documents will always be shown in descending order according to their relevancy score.  
