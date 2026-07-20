

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/Locale.h"
#include "smoke/Locales.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using LocaleStruct = ::smoke::Locales::LocaleStruct;

void register_LocalesLocaleStruct(py::module_& module) {
    py::class_<LocaleStruct>(module, "LocalesLocaleStruct")
        .def_readwrite("locale_field", &LocaleStruct::locale_field)
        .def(py::init<>())
        .def(py::init<::gluecodium::Locale>(), py::arg("locale_field"))
        ;
}

