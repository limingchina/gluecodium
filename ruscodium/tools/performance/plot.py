#!/usr/bin/env python3
"""Plot parity-verified fresh-process measurements; not part of the timed run."""
import argparse
import json
import os
from pathlib import Path
import tempfile

# Managed workspaces may have a read-only home. These caches are outside the
# benchmark, temporary, and do not replace explicitly configured cache paths.
_cache = tempfile.TemporaryDirectory(prefix='ruscodium-performance-plot-')
os.environ.setdefault('MPLCONFIGDIR', str(Path(_cache.name) / 'matplotlib'))
os.environ.setdefault('XDG_CACHE_HOME', str(Path(_cache.name) / 'cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=here / 'results/fresh.json')
    parser.add_argument('--output-base', type=Path, default=here / 'results/comparison')
    args = parser.parse_args()
    data = json.loads(args.input.read_text())
    assert data['schema'] == 'ruscodium.performance.fresh.v1'
    assert len(data['samples']) == len(data['selected']) * data['trials'] * 2
    assert all(s['exit_code'] == 0 and not s['timeout']
               and s['matches_baseline'] and not s['logging_error']
               for s in data['samples']), 'Only clean, parity-verified runs may be plotted'
    labels = {'custom': 'Custom', 'default-normalized': 'Default\n(corrected copy)'}
    cases = data['selected']
    names = [labels.get(c, c.replace('structs-', '') + ' structs') for c in cases]
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.4))
    colors = {'jvm': '#cc702c', 'rust': '#087e8b'}
    for axis, metric, unit in [(axes[0], 'wall_seconds', 1),
                               (axes[1], 'peak_rss_kib', 1024)]:
        for implementation, offset in [('jvm', -0.19), ('rust', 0.19)]:
            stats = [data['statistics'][c][implementation][metric] for c in cases]
            med = [s['median'] / unit for s in stats]
            error = [[(s['median'] - s['q1']) / unit for s in stats],
                     [(s['q3'] - s['median']) / unit for s in stats]]
            axis.bar([i + offset for i in range(len(cases))], med, width=0.36,
                     yerr=error, capsize=3, color=colors[implementation],
                     label='Kotlin/JVM' if implementation == 'jvm' else 'Rust (release)')
        axis.set_xticks(range(len(cases)), names)
        axis.grid(axis='y', alpha=0.2)
        axis.set_axisbelow(True)
        axis.spines[['top', 'right']].set_visible(False)
    axes[0].set_yscale('log')
    axes[0].set_ylim(0.04, 80)
    axes[0].set_ylabel('Wall time (seconds, log scale)')
    axes[0].yaxis.set_major_formatter(ScalarFormatter())
    axes[0].set_title('Time per fresh invocation')
    axes[1].set_ylabel('Peak resident memory (MiB)')
    axes[1].set_title('Compiler process peak RSS')
    axes[0].legend(frameon=False)
    fig.suptitle(f"Current Gluecodium pipelines: median and interquartile range\n"
                 f"{data['trials']} trials per implementation/workload; fresh processes, warm filesystem",
                 fontsize=13, y=0.99)
    fig.subplots_adjust(top=0.80, bottom=0.22, left=0.07, right=0.98, wspace=0.24)
    fig.text(0.07, 0.05,
             'Identical C++ outputs verified. Includes startup, source loading, validation, rendering and writes.\n'
             'Shared host with a 2-CPU quota. The 500-struct Rust pilot timed out at 60 s and is excluded.\n'
             'The separate persistent-process experiment and validation-coverage limits are in PERFORMANCE.md.',
             fontsize=9)
    args.output_base.parent.mkdir(parents=True, exist_ok=True)
    for suffix in ['.svg', '.png']:
        fig.savefig(args.output_base.with_suffix(suffix), dpi=160)
    plt.close(fig)


if __name__ == '__main__':
    main()
