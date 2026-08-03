

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
#include "smoke/BasicTypes.h"
#include "cstdint"
#include "string"

using BasicTypes = ::smoke::BasicTypes;



void register_smoke_BasicTypes(py::module_& module) {
auto cls_BasicTypes = py::class_<BasicTypes, std::shared_ptr<BasicTypes>>(module, "smoke_BasicTypes")
        .def("__gluecodium_id__", [](const BasicTypes& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("string_function", &BasicTypes::string_function, py::arg("input"))
        .def_static("bool_function", &BasicTypes::bool_function, py::arg("input"))
        .def_static("float_function", &BasicTypes::float_function, py::arg("input"))
        .def_static("double_function", &BasicTypes::double_function, py::arg("input"))
        .def_static("byte_function", &BasicTypes::byte_function, py::arg("input"))
        .def_static("short_function", &BasicTypes::short_function, py::arg("input"))
        .def_static("int_function", &BasicTypes::int_function, py::arg("input"))
        .def_static("long_function", &BasicTypes::long_function, py::arg("input"))
        .def_static("ubyte_function", &BasicTypes::ubyte_function, py::arg("input"))
        .def_static("ushort_function", &BasicTypes::ushort_function, py::arg("input"))
        .def_static("uint_function", &BasicTypes::uint_function, py::arg("input"))
        .def_static("ulong_function", &BasicTypes::ulong_function, py::arg("input"))
        ;


}
