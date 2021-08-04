import os, json
from elasticsearch import Elasticsearch

# specify index name here
ind = "test_index"
# Global variable to run while-loops
run = 1

# Elasticsearch connection function
# This connects to your specified cloud client of ElasticSearch.
# Please input your account information within the variables below
# elastic_pw could look like, for example: 
# elastic_pw = "Z7fIR7dXXeKAy2abHt24vOHk"
elastic_pw = ""

# elastic_endpoint could look like, for example:
# elastic_endpoint = "project.es.us-west-1.aws.found.io:1234"
elastic_endpoint = ""

connection = "https://elastic:" + elastic_pw + "@" + elastic_endpoint
es = Elasticsearch(connection)

# Your directory path should go to a folder which holds the .json files you are wanting to index.
# Very important to add the 'r' letter infront of the filepath. For example, should look like:
# directory = r"C:\Users\Your\files\here"
# And not:
# directory = "C:\Users\Your\files\here"
directory = r""

run_index = 0
clean_index = 0
running = 1
running2 = 1
# Get user choice to either index or skip indexing
print("Run the indexing process?\nEnter y or n")
while(running):
    choice = str(input())
    if(choice == "y"):
        run_index = 1
        # If indexing, get user choice to keep the current index or delete
        print("Would you like to delete the current index before indexing?\nEnter y or n")
        while(running2):
            choice2 = str(input())
            if(choice2 == "y"):
                clean_index = 1
                break
            elif(choice2 == "n"):
                clean_index = 0
                break
            # Catch for invalid input
            else:
                print("Please enter a valid input.")
        break
    elif(choice == "n"):
        run_index = 0
        break
    # Catch for invalid input
    else:
        print("Please enter a valid input.")

# Delete current index if user specified to
if(clean_index == 1):
    if not es.indices.exists(index=ind):
        print("No index currently exists, skipping deletion.")
    else:
        es.indices.delete(index=ind)

#page_id_dict = {} # Only used in depreciated queries
#doc_id_dict = {} # Only used in depreciated queries
doc_num = 0
file_num = 0
if(run_index == 1):
    # Iterate through all .json files within directory
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            # Get file contents
            f = open(filename, "r")
            content = f.read()
            # Format contents in dictionaries
            content_dict = json.loads(content)
            # Get keys from contents
            keys = list(content_dict.keys())
            single_key = keys[0]
            section = content_dict[single_key]
            #page_id_dict[file_num] = single_key # Only used in depreciated queries       
            for text in section:
                es.index(index=ind, ignore=400, id=doc_num, doc_type ="document", body=text)
                #doc_id_dict[doc_num] = single_key # Only used in depreciated queries
                doc_num += 1  
            file_num += 1  
   
while(run):
    options = ["Search through webpages for a term or terms, and show the top 10 (or fewer) relevant webpages.", "Close program."]

    print("\nWhat would you like to do?\n"
    "Enter the number corresponding to the topic you want.")
    val = 1
    # Print out available options
    for option in options:
        print("%d %s" % (val, option))
        val += 1

    choice = str(input())

    # 1 - Top 10 ranking
    if(choice == str(1)):
        print("\nWhat word or phrase would you like to search for?")
        search_for = str(input())

        # ES query
        response = es.search(index=ind, body={"query": {"bool": {"must": [{"match": {"content": (search_for)}}]}}})
    
        empty_list = []
        # If 0 results were found
        if(response['hits']['hits'] == empty_list):
            print("Sorry, not found.")
        else:
            texts = response['hits']['hits']
            val = 0
            items = []

            # Get the '_score' and 'title' parameters
            for section in texts:
                score = section['_score']
                title = section['_source']['title'].replace("\n", "")
                items.append([title, score])

            # Sort in descending order
            items.sort(key = lambda x: x[1], reverse=True)

            # Remove duplicate entries
            counter = 0
            new_list = []
            for item in items:
                if item not in new_list:
                    if(counter == 10):
                        break
                    new_list.append(item)
                    counter += 1
                else:
                    continue

            # Size check to say <value> amount of items will be returned
            if(len(new_list) > 10):
                size = 10
            else:
                size = len(new_list)
            print("\nThese are the top %d relevant sections to your word(s): " % (size))

            for item in new_list:
                print("%s\n%f" % (item[0], item[1]))

    # 2 - Exit
    elif(choice == str(2)):
        print("\nStopping\n")
        break

    # 3 - Catch invalid input
    else:
        print("\nPlease provide a valid input.\n")   


# Example queries
########################################## 
# body = {'query': {'match': {'section title': 'Other forms of the theorem'}}}
# response = es.search(index=ind, body=body)
# print(response)

# response = es.search(index=ind, body={"query": {"match": {"title": "Mathematics (album) - Wikipedia"}}})
# print(response)

# Search ALL query
# response = es.search(index=ind, body={"query": {"match_all": {}}})
# print(response)
##########################################


# Unused user options.
# Needs to index every time to work properly!
##########################################
# print("Beginning program.")
# while(run):
#     options = ["Learn about a specific topic.", "Search through webpages to find a specific term(s).", "Search through webpages for a term or terms, and show the top 10 (or fewer) relevant webpages.", "Close program."]

#     print("\nWhat would you like to do?\n"
#     "Enter the number corresponding to the topic you want.")
#     val = 1
#     for option in options:
#         print("%d %s" % (val, option))
#         val += 1

#     choice = str(input())

#     # 1 - Learn about specific topic
#     if(choice == str(1)):
#         print("\nWhich topic would you like to learn more about?\n"
#         "Enter the number corresponding to the topic you want.")
#         val = 1
#         for page in page_id_dict:
#             print("%d %s" % (val, page_id_dict[page]))
#             val += 1

#         choice = int(input())
#         choice -= 1
#         #print("choice is: ", choice)
#         entry = page_id_dict[choice]

#         id_list = []
#         for doc in doc_id_dict:
#             if(entry == doc_id_dict[doc]):
#                 id_list.append(doc)

#         titles = []
#         #print("id_list is: ", id_list)
#         for num in id_list:
#             response = es.get(index=ind, id=num)
#             titles.append(response['_source']['title'])

#         print("\nOf the topic %s, which section would you like to learn more about?\n"
#         "Enter the number corresponding to the topic you want." % (entry))
#         val = 1
#         for section in titles:
#             print("%d %s" % (val, section))
#             val += 1

#         choice = int(input())
#         choice -= 1
#         section = titles[choice]
#         print("section is: ", section)

#         response = es.search(index=ind, body={"query": {"query_string": {"query": (section), "default_field": "content"}}})
#         #print("response is: ", response)
#         actual_content = response['hits']['hits'][0]['_source']["content"]
#         print("\nHere you go!\n%s" % (actual_content))

#     # 2 - Search for word
#     elif(choice == str(2)):
#         #print("WIP for term search.\n")

#         print("\nWhat word or phrase would you like to search for?")
#         search_for = str(input())

#         # response = es.search(index=ind, body={"query": {"query_string": {"query": (search_for), "default_field": "content"}}})
#         response = es.search(index=ind, body={"query": {"bool": {"must": [{"match": {"content": (search_for)}}]}}})
#         #print("response is: ", response['hits']['hits'][1])

#         empty_list = []
#         if(response['hits']['hits'] == empty_list):
#             print("Sorry, not found.")
#         else:
            
#             # val = response['hits']['hits']
#             # num = int(val[0]['_id'])
#             # loc = doc_id_dict[num]
#             #text = response['hits']['hits'][0]['_source']
#             texts = response['hits']['hits']
#             #print("texts is: ", texts)
#             val = 0
#             titles = []
#             contents = []
#             for section in texts:
#                 #print("section is: ", section['_source'])
#                 text = section['_source']
#                 #print("text is: ", text)
#                 titles.append(text['title'])
#                 contents.append(text['content'])
#             #     val += 1
#             print("\n\"%s\" was found in section(s):" % (search_for))
#             for title in titles:
#                 print(title)
##########################################
