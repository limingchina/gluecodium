

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
using Locales = ::gluecodium::smoke::Locales;

void register_Locales(py::module_& module) {
    py::class_<Locales, std::shared_ptr<Locales>>(module, "Locales")
        .def("locale_method", &Locales::locale_method, py::arg("input"))
        .def_property("locale_property", py::overload_cast<>(&Locales::get_locale_property, py::const_), py::overload_cast<const ::gluecodium::Locale&>(&Locales::set_locale_property))
        ;
}

