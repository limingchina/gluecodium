

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/TypeCollection.h"
#include "smoke/TypeDefs.h"
#include "string"
#include "vector"

void register_TypeDefs(py::module_& module) {
    py::class_<TypeDefs>(module, "TypeDefs")
        .def("method_with_primitive_type_def", &TypeDefs::method_with_primitive_type_def, py::arg("input"))
        .def("method_with_complex_type_def", &TypeDefs::method_with_complex_type_def, py::arg("input"))
        .def("return_nested_int_type_def", &TypeDefs::return_nested_int_type_def, py::arg("input"))
        .def("return_test_struct_type_def", &TypeDefs::return_test_struct_type_def, py::arg("input"))
        .def("return_nested_struct_type_def", &TypeDefs::return_nested_struct_type_def, py::arg("input"))
        .def("return_type_def_point_from_type_collection", &TypeDefs::return_type_def_point_from_type_collection, py::arg("input"))
        .def_property("primitive_type_property", &TypeDefs::get_primitive_type_property)
        ;
}

