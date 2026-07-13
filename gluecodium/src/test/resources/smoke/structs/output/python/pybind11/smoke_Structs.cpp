

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/Structs.h"
#include "smoke/TypeCollection.h"
#include "cstdint"
#include "memory"
#include "optional"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Structs = ::smoke::Structs;

void register_Structs(py::module_& module) {
    py::class_<Structs, std::shared_ptr<Structs>>(module, "Structs")
        .def("swap_point_coordinates", &Structs::swap_point_coordinates, py::arg("input"))
        .def("return_all_types_struct", &Structs::return_all_types_struct, py::arg("input"))
        .def("create_point", &Structs::create_point, py::arg("x"), py::arg("y"))
        .def("modify_all_types_struct", &Structs::modify_all_types_struct, py::arg("input"))
        ;
}

