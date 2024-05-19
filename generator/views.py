import os
import subprocess
import shutil
from django.http import HttpResponse
from django.shortcuts import render
from .forms import ProjectForm
from .models import GeneratedProject


def copier_fichier(source_path, destination_path):
    try:
        with open(source_path, 'r') as source_file:
            contenu = source_file.read()

        with open(destination_path, 'w') as destination_file:
            destination_file.write(contenu)

        print("Le contenu a été copié avec succès.")
    except Exception as e:
        print(f"Une erreur s'est produite: {e}")


# Utilisation de la fonction
copier_fichier('/static/scripte.js', '/home/mouaad/testprojet/{project_name}/base/static/js/scripte.js')


def create_virtual_environment(project_path):
    """
    Crée un environnement virtuel dans le répertoire spécifié.
    """
    env_path = os.path.join(project_path, 'env')
    subprocess.run(['python3', '-m', 'venv', env_path], check=True)
    return env_path


def install_requirements(env_path, requirements_path):
    """
    Installe les dépendances listées dans le fichier requirements.txt.
    """
    pip_executable = os.path.join(env_path, 'bin', 'pip')
    subprocess.run([pip_executable, 'install', '-r', requirements_path], check=True)


import os


def modify_urls_file(project_path, project_name):
    urls_file = os.path.join(project_path, project_name, 'urls.py')

    new_url_config = """from django.urls import path, include, re_path\n\n"""
    new_url_config += """urlpatterns = [\n"""
    new_url_config += """    path('admin/', admin.site.urls),\n"""
    new_url_config += """    re_path(r'^', include(('base.urls', 'base'), namespace="base")),\n"""
    new_url_config += """    re_path(r'^', include(('client.urls', 'client'), namespace="client")),\n"""
    new_url_config += """    re_path(r'^', include(('order.urls', 'order'), namespace="order")),\n"""
    new_url_config += """]\n"""

    try:
        with open(urls_file, 'r') as f:
            content = f.read()

        # Recherche de la section urlpatterns
        urlpatterns_index = content.find('urlpatterns')
        urls_index = content.find('urlpatterns = [')
        if urlpatterns_index != -1:
            end_urls_index = content.find(']', urlpatterns_index)
            if end_urls_index != -1:
                content = content[:urls_index] + new_url_config + content[end_urls_index + 1:]

                print(f"Nouveau contenu de urls.py après modification de urlpatterns : \n{content}")
            else:
                raise ValueError("Fin de la section urlpatterns non trouvée.")
        else:
            raise ValueError("Section urlpatterns non trouvée dans le fichier urls.py.")

        # Écriture du nouveau contenu dans le fichier urls.py
        with open(urls_file, 'w') as f:
            f.write(content)
        print("Modification de urls.py réussie !")

    except FileNotFoundError:
        print(f"Fichier {urls_file} introuvable.")
    except Exception as e:
        print(f"Erreur lors de la modification de urls.py : {e}")


def modify_settings_file(project_path, project_name):
    settings_file = os.path.join(project_path, project_name, 'settings.py')

    new_database_config = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '',
    }"""

    try:
        # Lecture du contenu du fichier settings.py
        with open(settings_file, 'r') as f:
            content = f.read()

        print(f"Contenu actuel de settings.py : \n{content}")

        # Recherche et modification de la section INSTALLED_APPS
        installed_apps_index = content.find('INSTALLED_APPS')
        if installed_apps_index != -1:
            insertion_point = content.find('[', installed_apps_index)
            if insertion_point != -1:
                new_apps = (
                        "\n    'colorfield',\n"
                        + "    'base',\n"
                        + "    'client',\n"
                        + "    'order',\n"
                        + "    'django_htmx',\n"
                        + "    'crispy_forms',\n"
                        + "    'django_tables2',\n"
                        + "    'debug_toolbar',\n"
                        + "    'crispy_bootstrap5',\n"
                )
                new_content = (
                        content[:insertion_point + 1].strip()  # Garantir l'alignement
                        + new_apps
                        + content[insertion_point + 1:]
                )

                print(f"Nouveau contenu de settings.py après modification de INSTALLED_APPS : \n{new_content}")

                content = new_content
            else:
                raise ValueError("Point d'insertion pour INSTALLED_APPS non trouvé.")
        else:
            raise ValueError("Section INSTALLED_APPS non trouvée dans le fichier settings.py.")

        # Recherche et modification de la section DATABASES
        databases_index = content.find('DATABASES = {')
        if databases_index != -1:
            end_databases_index = content.find('}', databases_index)
            if end_databases_index != -1:
                end_databases_index += 1
                content = content[:databases_index] + new_database_config + content[end_databases_index:]

                print(f"Nouveau contenu de settings.py après modification de DATABASES : \n{content}")
            else:
                raise ValueError("Fin de la section DATABASES non trouvée.")
        else:
            raise ValueError("Section DATABASES non trouvée dans le fichier settings.py.")

        # Écriture du nouveau contenu dans le fichier settings.py
        with open(settings_file, 'w') as f:
            f.write(content)
        print("Modification de settings.py réussie !")

    except FileNotFoundError:
        print(f"Fichier settings.py introuvable à {settings_file}.")
    except Exception as e:
        print(f"Erreur lors de la modification de settings.py : {e}")


# Exemple d'utilisation
project_path = '/home/mouaad/testproject/'
project_name = 'apsstrrdd'
modify_settings_file(project_path, project_name)

from django.urls import path
from . import views

# Définition des URL à ajouter
url_patterns_content = [

]


def create_base_views_file(project_path):
    views_path = os.path.join(project_path, 'base', 'views.py')
    with open(views_path, 'w') as views_file:
        views_file.write(
            "from django.shortcuts import render\n\n"
            "def home(request):\n"
            "    return render(request, 'base/dashboard.html')\n"
        )


def generate_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project_name = form.cleaned_data['project_name']
            application = form.cleaned_data['application']
            app = form.cleaned_data['app']

            project_path = os.path.abspath(os.path.join('/home/mouaad/testproject/', project_name))

            # les fichier de base
            app_pathP = os.path.abspath(os.path.join(project_path, 'base'))
            path_template = os.path.abspath(os.path.join(app_pathP, 'templates'))

            path_base = os.path.abspath(os.path.join(path_template, 'base'))
            path_base_html = os.path.abspath(os.path.join(path_base, 'base.html'))
            path_index = os.path.abspath(os.path.join(path_base, 'index.html'))
            path_dashboard = os.path.abspath(os.path.join(path_base, 'dashboard.html'))
            path_includes = os.path.abspath(os.path.join(path_base, 'includes'))
            path_base_table = os.path.abspath(os.path.join(path_includes, 'base_table.html'))
            path_list_table = os.path.abspath(os.path.join(path_includes, 'list_table.html'))
            path_list_filter = os.path.abspath(os.path.join(path_includes, 'list_filter.html'))

            path_layout = os.path.abspath(os.path.join(path_template, 'layout'))

            path_aside = os.path.abspath(os.path.join(path_layout, 'aside'))
            path_menu_assets = os.path.abspath(os.path.join(path_aside, '_menu.html'))

            path_header = os.path.abspath(os.path.join(path_layout, 'header'))
            path_menu_header = os.path.abspath(os.path.join(path_header, '_menu.html'))

            path_registration = os.path.abspath(os.path.join(path_template, 'registration'))
            path_login = os.path.abspath(os.path.join(path_registration, 'login.html'))
            #   path_login_base = os.path.abspath(os.path.join(path_registration, 'login_base.html'))
            #  path_changer_pasw = os.path.abspath(os.path.join(path_registration, 'changer_passwoard.html'))

            path_errore = os.path.abspath(os.path.join(path_template, 'custom_errors'))

            path_foter = os.path.abspath(os.path.join(path_layout, '_footer.html'))

            path_static = os.path.abspath(os.path.join(app_pathP, 'static'))
            path_assets = os.path.abspath(os.path.join(path_static, 'assets'))
            path_css = os.path.abspath(os.path.join(path_assets, 'css'))
            path_style = os.path.abspath(os.path.join(path_css, 'style.css'))
            path_style_table = os.path.abspath(os.path.join(path_css, 'table.css'))

            path_img = os.path.abspath(os.path.join(path_static, 'img'))

            path_js = os.path.abspath(os.path.join(path_assets, 'js'))
            path_js_custom = os.path.abspath(os.path.join(path_js, 'custom'))
            path_js_htmx = os.path.abspath(os.path.join(path_js, 'htmx.js'))
            path_js_page = os.path.abspath(os.path.join(path_js, 'par_page.js'))
            path_js_plugins = os.path.abspath(os.path.join(path_js, 'plugins.bundle.js'))
            path_js_script = os.path.abspath(os.path.join(path_js, 'scripts.bundle.js'))
            path_js_widgets = os.path.abspath(os.path.join(path_js, 'widgets.bundle.js'))
            path_scripte = os.path.abspath(os.path.join(path_js, 'scripte.js'))

            path_plugins = os.path.abspath(os.path.join(path_static, 'plugins'))
            # autre application
            app_path = os.path.abspath(os.path.join(project_path, application))
            app_path2 = os.path.abspath(os.path.join(project_path, app))

            path_urls = os.path.abspath(os.path.join(app_pathP, 'urls.py'))
            path_urls_app = os.path.abspath(os.path.join(app_path, 'urls.py'))
            path_urls_ap = os.path.abspath(os.path.join(app_path2, 'urls.py'))
            path_requirements = os.path.abspath(os.path.join(project_path, 'requirement.txt'))

            settings_file = os.path.join(project_path, project_name, 'settings.py')
            urls_file = os.path.join(project_path, project_name, 'urls.py')

            # path_urls_application = os.path.join(project_name, 'urls.py')

            path_forms = os.path.abspath(os.path.join(app_path, 'forms.py'))
            path_tables = os.path.abspath(os.path.join(app_path, 'tables.py'))
            path_filter = os.path.abspath(os.path.join(app_path, 'filter.py'))
            views_path = os.path.join(project_path, 'base', 'views.py')

            app_static_path = os.path.join(app_pathP, 'static')
            app_template_path = os.path.join(app_pathP, 'templates')
            base_static_path = os.path.join(app_path, 'static')
            base_template_path = os.path.join(app_path, 'templates')

            try:
                # Créer les répertoires nécessaires
                os.makedirs(app_path, exist_ok=True)
                os.makedirs(path_base, exist_ok=True)
                os.makedirs(app_path2, exist_ok=True)
                os.makedirs(app_pathP, exist_ok=True)
                os.makedirs(path_includes, exist_ok=True)
                os.makedirs(path_errore, exist_ok=True)
                os.makedirs(path_header, exist_ok=True)
                os.makedirs(path_registration, exist_ok=True)
                os.makedirs(path_aside, exist_ok=True)
                os.makedirs(path_layout, exist_ok=True)
                os.makedirs(path_template, exist_ok=True)
                os.makedirs(path_static, exist_ok=True)
                os.makedirs(path_css, exist_ok=True)
                # os.makedirs(path_style, exist_ok=True)
                os.makedirs(path_js, exist_ok=True)
                os.makedirs(path_js_custom, exist_ok=True)
                os.makedirs(path_plugins, exist_ok=True)
                os.makedirs(path_assets, exist_ok=True)
                # os.touch(path_urls, exist_ok=True)

                # Copier les fichiers statiques
                for root, _, files in os.walk(app_static_path):
                    for file in files:
                        src_file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(src_file_path, app_static_path)
                        dest_file_path = os.path.join(base_static_path, rel_path)
                        os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                        shutil.copy2(src_file_path, dest_file_path)
                        print(f"Copied static file: {src_file_path} to {dest_file_path}")

                # Copier les fichiers de template
                for root, _, files in os.walk(app_template_path):
                    for file in files:
                        src_file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(src_file_path, app_template_path)
                        dest_file_path = os.path.join(base_template_path, rel_path)
                        os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                        shutil.copy2(src_file_path, dest_file_path)
                        print(f"Copied template file: {src_file_path} to {dest_file_path}")

                # Créer un fichier urls.py vide
                with open(path_urls, 'a'):  # Utilisation de 'a' pour créer le fichier s'il n'existe pas
                    pass

                # Créer un fichier urls.py vide
                with open(path_urls_app, 'a'):  # Utilisation de 'a' pour créer le fichier s'il n'existe pas
                    pass

                with open(path_urls_ap, 'a'):  # Utilisation de 'a' pour créer le fichier s'il n'existe pas
                    pass

                with open(views_path, 'w') as views_file:
                    views_file.write(
                        "from django.shortcuts import render\n\n"
                        "def home(request):\n"
                        "    return render(request, 'base/dashboard.html')\n"
                    )

                with open(path_requirements, 'w') as views_file:
                    views_file.write('''crispy-bootstrap5==0.7
Django==4.2.3
django-crispy-forms==2.0
django-debug-toolbar==4.1.0
django-filter==23.2
django-fsm==2.8.1
django-fsm-log==3.1.0
django-htmx==1.17.2
django-mailer==2.3.1
django-tables2==2.7.0
djangorestframework==3.14.0
json5==0.9.14
requests==2.31.0



                    ''')

                    with open(path_scripte, 'w') as index_file:
                        pass
                    # -----------------------base.html--------------------------#
                    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'base', 'base.html')

                    with open(template_path, 'r') as template_file:
                        template_content = template_file.read()

                    with open(path_base_html, 'w') as index_file:
                        index_file.write(template_content)
                    # -----------------------------------dashboard.html-----------------------------------#
                    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'base', 'dashboard.html')

                    with open(template_path, 'r') as template_file:
                        template_content = template_file.read()

                    with open(path_dashboard, 'w') as index_file:
                        index_file.write(template_content)
                    # -----------------------------------layout menu.html---------------------------------#
                    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'layout', 'aside',
                                                 '_menu.html')

                    with open(template_path, 'r') as template_file:
                        template_content = template_file.read()

                    with open(path_index, 'w') as index_file:
                        index_file.write(template_content)
                    # --------------------------------header------------------------------------#
                    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'layout', 'header',
                                                 '_menu.html')

                    with open(template_path, 'r') as template_file:
                        template_content = template_file.read()

                    with open(path_menu_header, 'w') as index_file:
                        index_file.write(template_content)
                    # ------------------------------------footer--------------------------------#
                    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'layout', '_footer.html')

                    with open(template_path, 'r') as template_file:
                        template_content = template_file.read()

                    with open(path_foter, 'w') as index_file:
                        index_file.write(template_content)
                    # -----------------------------login---------------------------------------#
                    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'registration', 'login.html')

                    with open(template_path, 'r') as template_file:
                        template_content = template_file.read()

                    with open(path_login, 'w') as index_file:
                        index_file.write(template_content)
                    # ---------------------------------base table-----------------------------------#
                    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'base', 'includes',
                                                 'base_table.html')

                    with open(template_path, 'r') as template_file:
                        template_content = template_file.read()

                    with open(path_base_table, 'w') as index_file:
                        index_file.write(template_content)
                    # -------------------------------list table-------------------------------------#
                    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'base', 'includes',
                                                 'list_filter.html')

                    with open(template_path, 'r') as template_file:
                        template_content = template_file.read()

                    with open(path_list_filter, 'w') as index_file:
                        index_file.write(template_content)
                    # -------------------------------list filter-------------------------------------#
                    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'base', 'includes',
                                                 'list_table.html')

                    with open(template_path, 'r') as template_file:
                        template_content = template_file.read()

                    with open(path_list_table, 'w') as index_file:
                        index_file.write(template_content)
                        # ---------------------------------css style-----------------------------------#
                        template_path = os.path.join(os.path.dirname(__file__), 'static', 'assets', 'css', 'style.css')

                        with open(template_path, 'r') as template_file:
                            template_content = template_file.read()

                        with open(path_style, 'w') as index_file:
                            index_file.write(template_content)
                        # --------------------------------------------------------------------#
                        template_path = os.path.join(os.path.dirname(__file__), 'static', 'assets', 'js', 'plugins.bundle.js')

                        with open(template_path, 'r') as template_file:
                            template_content = template_file.read()

                        with open(path_js_plugins, 'w') as index_file:
                            index_file.write(template_content)
                        # --------------------------------------------------------------------#
                        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'layout', 'aside',
                                                     '_menu.html')

                        with open(template_path, 'r') as template_file:
                            template_content = template_file.read()

                        with open(path_menu_assets, 'w') as index_file:
                            index_file.write(template_content)
                        # --------------------------------------------------------------------#

                    path_static = 'static/assets/plugins'  # Remplacez par le chemin correct
                    path_plugins = os.path.abspath(os.path.join(path_static, 'plugins'))
                    static_path = os.path.join(os.path.dirname(__file__), 'static', 'assets', 'plugins')

                    # Créer le dossier de destination s'il n'existe pas
                    os.makedirs(path_plugins, exist_ok=True)

                    try:
                        for item in os.listdir(static_path):
                            source_path = os.path.join(static_path, item)
                            destination_path = os.path.join(path_plugins, item)
                            if os.path.isdir(source_path):
                                shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
                            else:
                                shutil.copy2(source_path, destination_path)
                        print(f"Le contenu du dossier '{static_path}' a été copié avec succès vers '{path_plugins}'.")
                    except Exception as e:
                        print(f"Une erreur s'est produite lors de la copie : {e}")

                    # --------------------------------------------------------------------#

                with open(path_forms, 'a'):
                    pass

                # Remplir le fichier urls.py avec le contenu des URL
                with open(path_urls_app, 'w') as urls_file:
                    urls_file.write("from django.urls import path\n")
                    urls_file.write("from . import views\n\n")
                    urls_file.write("urlpatterns = [\n")
                    for url_pattern in url_patterns_content:
                        urls_file.write(f"    {url_pattern}\n")
                    urls_file.write("]\n")

                with open(path_urls_ap, 'w') as urls_file:
                    urls_file.write("from django.urls import path\n")
                    urls_file.write("from . import views\n\n")
                    urls_file.write("urlpatterns = [\n")
                    for url_pattern in url_patterns_content:
                        urls_file.write(f"    {url_pattern}\n")
                    urls_file.write("]\n")

                with open(path_urls, 'w') as urls_file:
                    urls_file.write("from django.urls import path\n")
                    urls_file.write("from . import views\n")
                    urls_file.write("from .views import home\n\n")
                    urls_file.write("urlpatterns = [\n")
                    urls_file.write("    path('', home, name='home'),\n")
                    for url_pattern in url_patterns_content:
                        urls_file.write(f"    {url_pattern}\n")
                    urls_file.write("]\n")

                for file_path in [path_forms, path_tables, path_filter]:
                    with open(file_path, 'a'):
                        pass

                # Construire la commande pour créer le projet Django
                os.system(f'django-admin startproject  {project_name} {os.path.join(project_path)}')

                # Créer une nouvelle application dans le projet avec manage.py startapp
                os.system(f'python3 manage.py startapp {application} {os.path.join(app_path, app_path)}')
                os.system(f'python3 manage.py startapp {app} {os.path.join(app_path2, app_path2)}')

                os.system(f'python3 manage.py startapp base {os.path.join(app_pathP, app_pathP)}')

                # Modifier le fichier settings.py pour utiliser PostgreSQL
                modify_settings_file(project_path, project_name)
                modify_urls_file(project_path, project_name)
                copier_fichier(project_path, project_name)
                create_base_views_file(project_path, app_pathP)

                new_app_name = 'base'
                base_app_cmd = ['python3', 'manage.py', 'startapp', new_app_name]
                subprocess.run(base_app_cmd, cwd=os.path.join(project_path, project_name), check=True)





                # Créer le fichier urls.py pour l'application 'base'
                urls_path = os.path.join(project_path, 'base', 'urls.py')
                with open(path_urls, 'w') as f:
                    f.write(
                        "from django.urls import path\n"
                        "from . import views\n\n"
                        "urlpatterns = [\n"
                        "    path('', views.home_view, name='home'),\n"
                        "]\n"
                    )

                # Copier les fichiers du projet principal dans le répertoire de la nouvelle application
                main_project_dir = os.path.join(project_path, project_name)
                new_app_dir = os.path.join(project_path, application)
                shutil.copytree(main_project_dir, new_app_dir)

                # Créer l'environnement virtuel
                env_path = create_virtual_environment(project_path)
                install_requirements(env_path, path_requirements)


                # Enregistrer les informations du projet dans la base de données
                GeneratedProject.objects.create(project_name=project_name, project_path=project_path,
                                                application=application)

                return HttpResponse(f'Projet {project_name} généré avec succès à {project_path}/{application}.')

            except subprocess.CalledProcessError as e:
                return HttpResponse(f'Erreur lors de la création du projet : {e}')
            except shutil.Error as e:
                return HttpResponse(f'Erreur lors de la copie des fichiers : {e}')
            except Exception as e:
                return HttpResponse(f'Erreur inattendue : {e}')

    else:
        form = ProjectForm()

    return render(request, 'form.html', {'form': form})




def dashboard(request):
    return render(request, 'base/home.html')
