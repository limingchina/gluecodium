

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/Locale.h"
#include "smoke/Locales.h"

void register_Locales(py::module_& module) {
    py::class_<Locales>(module, "Locales")
        .def("locale_method", &Locales::locale_method, py::arg("input"))
        .def_property("locale_property", &Locales::get_locale_property)
        ;
}

