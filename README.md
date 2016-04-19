# RIRES_EVAL

For Example


```
docker run --rm -v /home/ypeilin/Documents/:/functions/ -v /home/ypeilin/Documents/index/:/indexes/ -v /home/ypeilin/Documents/queries/:/queries/ -v /home/ypeilin/Documents/results/:/results/ -v /home/ypeilin/Documents/judgements/:/judgments/ yangpeilyn/rires_eval:latest -a TermScoreFunction.cpp(function_file_path) wt2g(index_path) wt2g(query_path) wt2g(judgment_path)
```


Currnetly the IndriRunQuery only works for one query at a time (unkown reasons), so please generate 
multiple query files for a query set (e.g. wt2g) and make it as a directory.
