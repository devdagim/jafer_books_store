# Setting PYTHONPATH on Linux
ref: https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html
ref: https://stackoverflow.com/questions/26616003/shopt-command-not-found-in-bashrc-after-shell-updation

1,Open terminal

2,Open the file(with_name={terminal_name:rc}) ~/.bashrc or ~/.zshrc
```shell
nano ~/.bashrc
```

3,Add the following line to the end:
```shell
export PYTHONPATH={ur project path}
```

4,Save the file.
ctr + s 

5,Close your terminal text editor(nano)
ctr+x

6,reload the modified .bashrc file 
```
source ~/.bashrc
```
7,check it
```shell
echo $PYTHONPATH
```

# this project path,terminal
```shell
# python: jafaer_books_project path seting
export PYTHONPATH=/home/pr_dagi/Project/jafer_books_store
```
terminal_name=zsh

