import os,sys
import codecs
import subprocess
from subprocess import Popen,PIPE
import ast
import argparse
import json

functions_folder = '/functions/'
index_folder = '/indexes/'
query_folder = '/queries/'
results_folder = '/results/'
judgment_folder = '/judgments/'

def print_debug(s):
    print '-'*30
    print s
    print '-'*30

def replace_and_make(fn):
    try:
        container_fn = os.path.join(functions_folder, os.path.basename(fn))
        with open(container_fn) as _input:
            inputs = _input.read()
            with open('src/TermScoreFunction.cpp', 'w') as f:
                f.write(inputs)
    except:
        sys.exit(container_fn+' does not exist!')
    p = Popen(['make'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        sys.exit(stderr)
    #print stdout
    #print_debug('Compile Success!!')


def run_query(index_path, query_file_path, pertube_type='0', pertube_paras_str=''):
    container_index_path = os.path.join(index_folder, os.path.basename(index_path))
    query_folder_path = os.path.join(query_folder, os.path.basename(query_file_path) )
    for qf in os.listdir(query_folder_path):
        container_query_file_path = os.path.join(query_folder_path, qf)
        p = Popen(['./runquery/IndriRunQuery', 
                container_query_file_path, 
                '-index=%s' % container_index_path], 
                '-pertube=%s' % pertube_type,
                '-pertube_paras=%s' % pertube_paras_str,
                stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            sys.exit(stderr)
        result_file_path = os.path.join(results_folder, qf)
        with open(result_file_path, 'w') as f:
            f.write(stdout) 
    #print_debug('Run Query Success!!')
    #return result_file_path

def print_eval_all_avg(performace_dict):
    all_performances = {}
    for qid, performace_str in performace_dict.items():
        for line in performace_str.split('\n'):
            line = line.strip()
            if line:
                row = line.split()
                evaluation_method = row[0]
                qid = row[1]
                try:
                    performace = ast.literal_eval(row[2])
                except:
                    continue

                if evaluation_method not in all_performances:
                    all_performances[evaluation_method] = []
                all_performances[evaluation_method].append(performace)
    json_output = {}
    for evaluation_method, l in all_performances.items():
        json_output[evaluation_method] = round(sum(l)/float(len(l)), 4)

    print json.dumps(json_output, indent=2, sort_keys=True)

def eval_results(judgement_file_path):
    container_judgement_file_path = os.path.join(judgment_folder, os.path.basename(judgement_file_path))
    # p = Popen(['./bin/trec_eval', '-q', '-m', 'all_trec', container_judgement_file_path, result_file_path], 
    #         stdout=PIPE, stderr=PIPE)
    all_performances = {}
    for rp in os.listdir(results_folder):
        p = Popen(['./bin/trec_eval', container_judgement_file_path, os.path.join(results_folder, rp)], stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            print stderr
            sys.exit(stderr)
        #print stdout
        all_performances[rp] = stdout
    print_eval_all_avg(all_performances)
    #print_debug('Eval Success!!')


def run_all(function_file_path, index_path, query_file_path, judgement_file_path, 
        pertube_type='0', pertube_paras_str=''):
    replace_and_make(function_file_path)
    run_query(index_path, query_file_path, pertube_type, pertube_paras_str)
    eval_results(judgement_file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--all",
        nargs=6,
        help="run all of the functionalities: make, run query, eval")

    parser.add_argument("-m", "--replace_and_make",
        nargs=1,
        help="Replace and Make the new IndriRunQuery binary")

    parser.add_argument("-r", "--run_query",
        nargs=4,
        help="run query")

    args = parser.parse_args()

    if args.all:
        function_file_path = args.all[0]
        index_path = args.all[1]
        query_file_path = args.all[2]
        judgement_file_path = args.all[3]
        pertube_type = args.all[4]
        pertube_paras_str = args.all[5]
        run_all(function_file_path, index_path, query_file_path, 
            judgement_file_path, pertube_type, pertube_paras_str)

    if args.replace_and_make:
        file_path = args.replace_and_make[0]
        replace_and_make(file_path)

    if args.run_query:
        index_path = args.run_query[0]
        query_file_path = args.run_query[1]
        pertube_type = args.run_query[2]
        pertube_paras_str = args.run_query[3]
        run_query(index_path, query_file_path, pertube_type, pertube_paras_str)