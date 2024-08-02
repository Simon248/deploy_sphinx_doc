# Sphinx Local Deployment

## How to use:  

* set the list of sphinx documentation repositories you want to deploy in  ```./repo_list/repolist.yaml```
* then ```docker-compose up```
* Access your documentation in browser at ~~```localhost:8080```~~ http://192.168.2.25/
* check networking in docker-compose.yaml cause using bridge mode providing a docker network that coul be already in use on your setup.

 **REMARKS :**  
 * **Cron task period :** is defined in docker compose for easy change. Default is short period (1min) for testing
 * **Theme:** if you use other tehme than sphinx_rtd_theme, you have to install it in dockerfile
 * **Security:** for local use only  
 * ~~**Git clone:** only use https so your repo should be publicly available. otherwise setup an ssh key.~~
 * **Git clone:** if git repo is private you can use a github token and put it into a .env file next to the docker-compose.yaml
 * **Git branch:** Not taken into account at this time. always cloning main/master.


## How it works:
* 2 containers/services in docker compose:
  * **web_server :** nginx that mount a dedicated conf volume and map ports.
  * **cron_builder :** Run periodically a cron task calling python script.  
  python script is copied in the image through dockerfile.  
  cron task is defined in entrypoint.  
  python script do the following:
    * git clone or git pull the listed repo
    * for each repo:
      * empty the build folder
      * call make html (to rebuild it)
      * copy the build folder in /deploy/<repo_name>
      * create the landing page (/deploy/index.html) with a link to all repo pages <repo_name>/index.html
