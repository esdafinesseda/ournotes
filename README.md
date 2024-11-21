# Our Notes

The goal of this project is to develop a community note taking and course discussion platform that leverages semantic embeddings, clustering, and Retrieval Augmented Generation (RAG) to allow students to build a collective understanding of a given topic.

# TODO

1. Remove index cache router and rename everything to index record cache
2. Remove index interactions from the note controller and add in index record cache interactions
3. Build the batched update method i.e. update index which effects all changes: group by type, create, update, or delete
4. Look into scheduling for updates
