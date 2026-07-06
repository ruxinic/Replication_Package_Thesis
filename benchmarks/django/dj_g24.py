import pyperf as perf
import django.conf
from django.template import Context, Template
import django
import numpy as np  # G24: Import High-Performance Computing library

# 2016-10-10: Python 3.6 takes 380 ms
DEFAULT_SIZE = 100

def bench_django_template(runner, size):
    template = Template("""<table>
{% for row in table %}
<tr>{% for col in row %}<td>{{ col|escape }}</td>{% endfor %}</tr>
{% endfor %}
</table>
    """)
    
    # G24: use NumPy to generate the table data.
    # np.tile and np.arange perform the matrix creation in compiled C code
    table = np.tile(np.arange(size), (size, 1))
    
    context = Context({"table": table})

    runner.bench_func('django_template', template.render, context)

if __name__ == "__main__":
    if not django.conf.settings.configured:
        django.conf.settings.configure(TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
        }])
        django.setup()

    runner = perf.Runner()
    cmd = runner.argparser
    cmd.add_argument("--table-size",
                     type=int, default=DEFAULT_SIZE,
                     help="Size of the HTML table, height and width "
                          "(default: %s)" % DEFAULT_SIZE)

    args = runner.parse_args()
    runner.metadata['description'] = "Django template"
    runner.metadata['django_version'] = django.__version__
    runner.metadata['django_table_size'] = args.table_size

    bench_django_template(runner, args.table_size)