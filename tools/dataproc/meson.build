dataproc_cflags = [
    '-std=gnu17',
    '-O3',
    '-Wall',
    '-Wextra',
    '-Wpedantic',
    '-Wconversion',
    '-Wno-sign-conversion',
    '-Wno-unused-result',
    '-Wno-stringop-overflow',
]

dataproc_dep = declare_dependency(
    include_directories: include_directories('lib/include'),
    link_with: static_library(
        'dataproc',
        sources: files(
            'lib/dataproc.c',
            'lib/json.c',
        ),

        c_args: dataproc_cflags,

        include_directories: include_directories('lib/include'),
        dependencies: dependency('yyjson'),
        native: true,
    ),
)

repo_include = meson.global_source_root() / 'include'
repo_build = meson.global_build_root()
dataproc_templates_dir = meson.current_source_dir() / 'data'

commonproc_dep = declare_dependency(
    link_with: static_library(
        'commonproc',
        sources: files('src/common.c'),

        c_args: [
            dataproc_cflags,
            f'-DREPO_INCLUDE="@repo_include@"',
            f'-DREPO_BUILD="@repo_build@"',
            f'-DTEMPLATES_DIR="@dataproc_templates_dir@"',
        ],

        dependencies: [
            dataproc_dep,
            nitroarc_dep,
            libenum_dep,
            libexpr_dep,
        ],
        native: true,
    ),
    dependencies: [ dataproc_dep, nitroarc_dep, libenum_dep ],
)

cc = meson.get_compiler('c', native: true)
speciesproc_exe = executable(
    'speciesproc',
    sources: [ files('src/speciesproc.c'), c_consts_generators ],
    c_args: dataproc_cflags,
    include_directories: [ public_includes, toplevel_includes ],
    dependencies: [
        commonproc_dep,
        cc.find_library('m', required: true),
    ],
    native: true,
)

resdatproc_exe = executable(
    'resdatproc',
    sources: files('src/resdatproc.c'),
    c_args: dataproc_cflags,
    include_directories: [ public_includes, toplevel_includes ],
    dependencies: commonproc_dep,
    native: true,
)

dexproc_exe = executable(
    'dexproc',
    sources: [ files('src/dexproc.c'), c_consts_generators ],
    c_args: dataproc_cflags,
    include_directories: [ public_includes, toplevel_includes ],
    dependencies: commonproc_dep,
    native: true,
)

trainerproc_exe = executable(
    'trainerproc',
    sources: [ files('src/trainerproc.c'), c_consts_generators ],
    c_args: dataproc_cflags,
    include_directories: [ public_includes, toplevel_includes ],
    dependencies: commonproc_dep,
    native: true,
)

frontierproc_exe = executable(
    'frontierproc',
    sources: [ files('src/frontierproc.c'), c_consts_generators ],
    c_args: dataproc_cflags,
    include_directories: [ public_includes, toplevel_includes ],
    dependencies: commonproc_dep,
    native: true,
)

itemproc_exe = executable(
    'itemproc',
    sources: [ files('src/itemproc.c'), c_consts_generators ],
    c_args: dataproc_cflags,
    include_directories: [ public_includes, toplevel_includes ],
    dependencies: commonproc_dep,
    native: true,
)

npctradeproc_exe = executable(
    'npctradeproc',
    sources: [ files('src/npctradeproc.c'), c_consts_generators ],
    c_args: dataproc_cflags,
    include_directories: [ public_includes, toplevel_includes ],
    dependencies: commonproc_dep,
    native: true,
)

bst_py = files('src/bst_proc.py')
r = run_command(bst_py)
if r.returncode() != 0
    error('Could not generate BST header')
endif
progressitem_py = files('src/progressitem_proc.py')
r = run_command(progressitem_py)
if r.returncode() != 0
    error('Could not generate progression item header')
endif
helditem_py = files('src/helditem_proc.py')
r = run_command(helditem_py)
if r.returncode() != 0
    error('Could not generate held item header')
endif
add_version_py = files('src/add_version.py')
r = run_command(add_version_py)
if r.returncode() != 0
    error('Could not template the version #')
endif
