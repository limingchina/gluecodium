

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/Locale.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/Locales.h"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

using Locales = ::smoke::Locales;
using LocaleStruct = ::smoke::Locales::LocaleStruct;



void register_smoke_Locales(py::module_& module) {
auto cls_Locales = py::class_<Locales, std::shared_ptr<Locales>>(module, "smoke_Locales")
        .def("__gluecodium_id__", [](const Locales& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("locale_method", &Locales::locale_method, py::arg("input"))
        .def_property("locale_property", py::overload_cast<>(&Locales::get_locale_property, py::const_), py::overload_cast<const ::gluecodium::Locale&>(&Locales::set_locale_property))
        ;

auto cls_LocalesLocaleStruct = py::class_<LocaleStruct>(cls_Locales, "LocaleStruct")
        .def_readwrite("locale_field", &LocaleStruct::locale_field)
        .def(py::init<>())
        .def(py::init<::gluecodium::Locale>(), py::arg("locale_field"))
        ;


}
