

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/BasicTypes.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using BasicTypes = ::gluecodium::smoke::BasicTypes;

void register_BasicTypes(py::module_& module) {
    py::class_<BasicTypes, std::shared_ptr<BasicTypes>>(module, "BasicTypes")
        .def("string_function", &BasicTypes::string_function, py::arg("input"))
        .def("bool_function", &BasicTypes::bool_function, py::arg("input"))
        .def("float_function", &BasicTypes::float_function, py::arg("input"))
        .def("double_function", &BasicTypes::double_function, py::arg("input"))
        .def("byte_function", &BasicTypes::byte_function, py::arg("input"))
        .def("short_function", &BasicTypes::short_function, py::arg("input"))
        .def("int_function", &BasicTypes::int_function, py::arg("input"))
        .def("long_function", &BasicTypes::long_function, py::arg("input"))
        .def("ubyte_function", &BasicTypes::ubyte_function, py::arg("input"))
        .def("ushort_function", &BasicTypes::ushort_function, py::arg("input"))
        .def("uint_function", &BasicTypes::uint_function, py::arg("input"))
        .def("ulong_function", &BasicTypes::ulong_function, py::arg("input"))
        ;
}

