

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/CalculationResult.h"
#include "smoke/ListenerWithProperties.h"
#include "cstdint"
#include "memory"
#include "string"
#include "vector"

void register_ListenerWithProperties(py::module_& module) {
    py::class_<ListenerWithProperties, std::shared_ptr<ListenerWithProperties>>(module, "ListenerWithProperties")
        .def_property("message", &ListenerWithProperties::get_message)
        .def_property("packed_message", &ListenerWithProperties::get_packed_message)
        .def_property("structured_message", &ListenerWithProperties::get_structured_message)
        .def_property("enumerated_message", &ListenerWithProperties::get_enumerated_message)
        .def_property("arrayed_message", &ListenerWithProperties::get_arrayed_message)
        .def_property("mapped_message", &ListenerWithProperties::get_mapped_message)
        .def_property("buffered_message", &ListenerWithProperties::get_buffered_message)
        ;
}

