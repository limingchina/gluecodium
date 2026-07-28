

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
#include "smoke/StringsWithCstring.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StringsWithCstring = ::smoke::StringsWithCstring;


void register_smoke_StringsWithCstring(py::module_& module) {
    py::class_<StringsWithCstring, std::shared_ptr<StringsWithCstring>>(module, "smoke_StringsWithCstring")
        .def("__gluecodium_id__", [](const StringsWithCstring& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("return_input_string_type", py::overload_cast<const char*>(&StringsWithCstring::return_input_string), py::arg("input_string"))
        .def_static("return_input_string", py::overload_cast<const ::std::string&>(&StringsWithCstring::return_input_string), py::arg("input_string"))
        ;
}

