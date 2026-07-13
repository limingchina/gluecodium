

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/CalculationResult.h"
#include "smoke/ListenersWithReturnValues.h"
#include "memory"
#include "string"
#include "vector"

void register_ListenersWithReturnValues(py::module_& module) {
    py::class_<ListenersWithReturnValues, std::shared_ptr<ListenersWithReturnValues>>(module, "ListenersWithReturnValues")
        .def("fetch_data_double", &ListenersWithReturnValues::fetch_data_double)
        .def("fetch_data_string", &ListenersWithReturnValues::fetch_data_string)
        .def("fetch_data_struct", &ListenersWithReturnValues::fetch_data_struct)
        .def("fetch_data_enum", &ListenersWithReturnValues::fetch_data_enum)
        .def("fetch_data_array", &ListenersWithReturnValues::fetch_data_array)
        .def("fetch_data_map", &ListenersWithReturnValues::fetch_data_map)
        .def("fetch_data_instance", &ListenersWithReturnValues::fetch_data_instance)
        ;
}

