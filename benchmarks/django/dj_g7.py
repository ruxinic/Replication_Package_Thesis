import pyperf as perf
import django.conf
from django.template import Context, Template
import django

# 2016-10-10: Python 3.6 takes 380 ms
DEFAULT_SIZE = 100

def bench_django_template(runner, size):
    template = Template("""<table>
{% for row in table %}
<tr>{% for col in row %}<td>{{ col|escape }}</td>{% endfor %}</tr>
{% endfor %}
</table>
    """)
    
    # G7: instead of generating 'size' number of range 
    # objects one-by-one in a loop, create one prototype row
    single_row = list(range(size))
    
    # G7: use a bulk multiplier to create the table structure at once 
    table = [single_row] * size 
    
    context = Context({"table": table})
    runner.bench_func('django_template', template.render, context)

def prepare_cmd(runner, cmd):
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