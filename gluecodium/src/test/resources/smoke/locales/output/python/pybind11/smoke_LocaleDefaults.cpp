

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/Locale.h"
#include "smoke/LocaleDefaults.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using LocaleDefaults = ::gluecodium::smoke::LocaleDefaults;

void register_LocaleDefaults(py::module_& module) {
    py::class_<LocaleDefaults>(module, "LocaleDefaults")
        .def_readwrite("english", &LocaleDefaults::english)
        .def_readwrite("lat_am_spanish", &LocaleDefaults::lat_am_spanish)
        .def_readwrite("romansh_sursilvan", &LocaleDefaults::romansh_sursilvan)
        .def_readwrite("serbian_cyrillic", &LocaleDefaults::serbian_cyrillic)
        .def_readwrite("traditional_chinese_taiwan", &LocaleDefaults::traditional_chinese_taiwan)
        .def_readwrite("zuerich_german", &LocaleDefaults::zuerich_german)
        ;
}

