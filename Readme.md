# Sphinx Local Deployment

## How to use:  

* set the list of sphinx documentation repositories you want to deploy in  ```./repo_list/repolist.yaml```
* then ```docker-compose up```
* Access your documentation in browser at ```localhost:8080```

 **REMARKS :**  
 * **Theme:** if you use other tehme than sphinx_rtd_theme, you have to install it in dockerfile
 * **Security:** for local use only
 * **Git clone:** only use https so your repo should be publicly available. otherwise setup an ssh key.
 * **Git branch:** Not taken into account at this time. always cloning main/master.


## How it works:
* 2 containers/services in docker compose:
  * **web_server :** nginx that mount a dedicated conf volume and map ports.
  * **cron_builder :** Run periodically a cron task calling python script.  
  cron task and python script are copied in the image through dockerfile.
  python script daily do the following
    * git clone or git pull the listed repo
    * for each repo:
      * empty the build folder
      * call make html (to rebuild it)
      * copy the build folder in /deploy/<repo_name>
      * create the landing page (/deploy/index.html) with a link to all repo pages <repo_name>/index.html
