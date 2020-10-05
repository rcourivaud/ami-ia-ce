# Documentation
## Configurate workspace

Before generating documentation, the following libraries must be installed :

* sphinx (last)
```bash
pip install -U sphinx --proxy http://proxy.conseil-etat.fr:8080
```

* rst2pdf (v0.96)
```bash
pip install rst2pdf==0.96 --proxy http://proxy.conseil-etat.fr:8080
```

For the first time you run sphinx on the project, execute the folowing command inside the docs folder and use default parameters except for 'Separate source and build directories (y/n)' where you have to set 'y'
```bash
spinx-quickstart
```
Create en empty docs/source/__init__.py file. 
Activate the following lines in the docs/source/conf.py file
```python
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))
#...
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.napoleon', 'rst2pdf.pdfbuilder']
```

If a new module is created in the project, you need to specify its path to sphynx for the module to be considered in the documentation generation.
In docs/source/code.rst, add the following lines to the file :
```bash
.. automodule:: <path_to_module>
	:members:
```

## Generate documentation

Be sure to be in the docs/ folder before running the commands.

In case the already generated documentation is causing trouble, run the following command :

```bash
make clean
```

To generate the HTML files, run the following command :

```bash
make html
```

The output will be stored in docs/build/html/

To generate the PDF files, rune the following command :

```bash
sphinx-build -b pdf ./source build/pdf
```

The output will be stored in docs/build/pdf/

