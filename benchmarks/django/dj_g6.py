import pyperf as perf
import django.conf
from django.template import Context, Template
import django

# 2016-10-10: Python 3.6 takes 380 ms
DEFAULT_SIZE = 100

def bench_django_template(runner, size):
    # G6: keep the template object but avoid saving the 'table' and 'context' to local variables
    # pass the data generation and Context creation directly into the benchmark call
    
    template = Template("""<table>
{% for row in table %}
<tr>{% for col in row %}<td>{{ col|escape }}</td>{% endfor %}</tr>
{% endfor %}
</table>
    """)

    runner.bench_func(
        'django_template', 
        template.render, 
        Context({"table": [range(size) for _ in range(size)]})
    )

def prepare_cmd(runner, cmd):
    # G6: inline the attribute access directly into the append call 
    cmd.append("--table-size=%s" % runner.args.table_size)

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