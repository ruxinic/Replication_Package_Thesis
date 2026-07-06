import os
from concurrent.futures import ProcessPoolExecutor
import pyperf as perf
import django.conf
from django.template import Context, Template

DEFAULT_SIZE = 100

# Global setup needs to happen inside every process worker
def init_django():
    if not django.conf.settings.configured:
        django.conf.settings.configure(TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
        }])
        django.setup()

def render_worker(template_src, table_size, count):
    # worker function executed by each individual CPU core
    # renders the template 'count' times sequentially on its own core
    init_django()
    template = Template(template_src)
    table = [range(table_size) for _ in range(table_size)]
    context = Context({"table": table})
    
    # render loop bound to this specific worker process core
    for _ in range(count):
        template.render(context)

def run_parallel_renders(num_cores, template_src, table_size):
    # G26: launch worker processes to saturate every available core on the server simultaneously
    # each core handles 5 renders concurrently (Total of 5 * num_cores renders)
    renders_per_core = 5 
    
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        # send the work across all cores
        futures = [
            executor.submit(render_worker, template_src, table_size, renders_per_core)
            for _ in range(num_cores)
        ]
        # wait for all cores to complete their workload chunks
        for future in futures:
            future.result()

def bench_django_template(runner, size):
    template_src = """<table>
{% for row in table %}
<tr>{% for col in row %}<td>{{ col|escape }}</td>{% endfor %}</tr>
{% endfor %}
</table>"""

    num_cores = os.cpu_count() or 1
    runner.bench_func(
        'django_template_g26', 
        run_parallel_renders, 
        num_cores, 
        template_src, 
        size
    )

if __name__ == "__main__":
    init_django()

    runner = perf.Runner()
    cmd = runner.argparser
    cmd.add_argument("--table-size",
                     type=int, default=DEFAULT_SIZE,
                     help="Size of the HTML table, height and width (default: %s)" % DEFAULT_SIZE)

    args = runner.parse_args()
    runner.metadata['description'] = "Django template parallelized (G26)"
    runner.metadata['django_version'] = django.__version__
    runner.metadata['django_table_size'] = args.table_size
    runner.metadata['cpu_cores_allocated'] = os.cpu_count() or 1

    bench_django_template(runner, args.table_size)