

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
#include "smoke/TypeCollection.h"
#include "cstdint"
#include "memory"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using AllTypesStruct = ::smoke::TypeCollection::AllTypesStruct;

void register_smoke_TypeCollectionAllTypesStruct(py::module_& module) {
    py::class_<AllTypesStruct>(module, "smoke_TypeCollectionAllTypesStruct")
        .def_readwrite("int8_field", &AllTypesStruct::int8_field)
        .def_readwrite("uint8_field", &AllTypesStruct::uint8_field)
        .def_readwrite("int16_field", &AllTypesStruct::int16_field)
        .def_readwrite("uint16_field", &AllTypesStruct::uint16_field)
        .def_readwrite("int32_field", &AllTypesStruct::int32_field)
        .def_readwrite("uint32_field", &AllTypesStruct::uint32_field)
        .def_readwrite("int64_field", &AllTypesStruct::int64_field)
        .def_readwrite("uint64_field", &AllTypesStruct::uint64_field)
        .def_readwrite("float_field", &AllTypesStruct::float_field)
        .def_readwrite("double_field", &AllTypesStruct::double_field)
        .def_readwrite("string_field", &AllTypesStruct::string_field)
        .def_readwrite("boolean_field", &AllTypesStruct::boolean_field)
        .def_readwrite("bytes_field", &AllTypesStruct::bytes_field)
        .def_readwrite("point_field", &AllTypesStruct::point_field)
        .def(py::init<>())
        .def(py::init<int8_t, uint8_t, int16_t, uint16_t, int32_t, uint32_t, int64_t, uint64_t, float, double, ::std::string, bool, ::std::shared_ptr< ::std::vector< uint8_t > >, ::smoke::TypeCollection::Point>(), py::arg("int8_field"), py::arg("uint8_field"), py::arg("int16_field"), py::arg("uint16_field"), py::arg("int32_field"), py::arg("uint32_field"), py::arg("int64_field"), py::arg("uint64_field"), py::arg("float_field"), py::arg("double_field"), py::arg("string_field"), py::arg("boolean_field"), py::arg("bytes_field"), py::arg("point_field"))
        ;
}

