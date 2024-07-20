import os
import yaml
import subprocess
import shutil

REPO_LIST_PATH = '/repo_list/repo_list.yaml'
BUILD_DIR = '/documentation_sphinx_build'
DEPLOY_DIR = '/documentation_sphinx_deploy'
HOME_PAGE_PATH = os.path.join(DEPLOY_DIR, 'index.html')

# Fonction pour générer la page d'accueil
def generer_page_accueil(dossier_destination):
    projets = [d for d in os.listdir(dossier_destination) if os.path.isdir(os.path.join(dossier_destination, d))]
    with open(HOME_PAGE_PATH, 'w') as f:
        f.write("<html><head><title>Documentation Projects</title></head><body><h1>Documentation Projects</h1><ul>")
        for projet in projets:
            f.write(f'<li><a href="{projet}/index.html">{projet}</a></li>')
        f.write("</ul></body></html>")
    print(f"Page d'accueil générée à {HOME_PAGE_PATH}")

def vider_dossier(dossier_path):
    if os.path.exists(dossier_path):
        shutil.rmtree(dossier_path)
        print(f"Le dossier {dossier_path} a été vidé.")



# Fonction pour construire la documentation Sphinx et copier le dossier HTML
def build_sphinx_and_copy(dossier_source, dossier_destination):
    # Assurez-vous que le dossier source contient un fichier conf.py
    if not os.path.isfile(os.path.join(dossier_source,'source', 'conf.py')):
        print(f"Le dossier {dossier_source} ne contient pas de fichier conf.py")
        return

    # Construire la documentation Sphinx en utilisant `make html`
    env = os.environ.copy()
    env["PATH"] = "/usr/local/bin:" + env["PATH"]

    try:
        subprocess.run(['make', 'html'], cwd=dossier_source, check=True, env=env)
        print(f"Documentation construite pour {dossier_source}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la construction de la documentation Sphinx pour {dossier_source}: {e}")
        return

    # Chemin vers le dossier HTML généré
    dossier_html = os.path.join(dossier_source, 'build', 'html')

    # Copier le dossier HTML vers le dossier de destination
    if not os.path.exists(dossier_destination):
        os.makedirs(dossier_destination)

    destination_html = os.path.join(dossier_destination, os.path.basename(dossier_source))
    if os.path.exists(destination_html):
        shutil.rmtree(destination_html)
    shutil.copytree(dossier_html, destination_html)
    print(f"Dossier HTML copié de {dossier_html} vers {destination_html}")



def clone_repos():
    with open(REPO_LIST_PATH, 'r') as file:
        data = yaml.safe_load(file)
        repos = data.get('repos', [])

    if not os.path.exists(BUILD_DIR):
        os.makedirs(BUILD_DIR)

    for repo in repos:
        
        repo_name = repo.split('/')[-1].replace('.git', '')
        repo_path = os.path.join(BUILD_DIR, repo_name)

        print(f"Cloning repository: {repo}")

        if os.path.exists(repo_path):
            subprocess.run(['git', '-C', repo_path, 'pull'], check=True)
        else:
            subprocess.run(['git', 'clone', repo, repo_path], check=True)

        print(f"RAZ du dossier build")
        vider_dossier(os.path.join(repo_path, 'build'))
        
        build_sphinx_and_copy(repo_path,DEPLOY_DIR)

    generer_page_accueil(DEPLOY_DIR)

if __name__ == "__main__":
    clone_repos()
