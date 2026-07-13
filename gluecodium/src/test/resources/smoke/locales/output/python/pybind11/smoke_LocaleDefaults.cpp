

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/Locale.h"
#include "smoke/LocaleDefaults.h"

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

