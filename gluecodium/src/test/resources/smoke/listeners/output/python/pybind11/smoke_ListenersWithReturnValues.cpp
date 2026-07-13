

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "smoke/CalculationResult.h"
#include "smoke/ListenersWithReturnValues.h"
#include "memory"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ListenersWithReturnValues = ::gluecodium::smoke::ListenersWithReturnValues;

class ListenersWithReturnValuesTrampoline : public ListenersWithReturnValues {
public:
    using ListenersWithReturnValues::ListenersWithReturnValues;

    double fetch_data_double(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(double, ListenersWithReturnValues, fetch_data_double);
    }
    ::std::string fetch_data_string(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::string, ListenersWithReturnValues, fetch_data_string);
    }
    ::smoke::ListenersWithReturnValues::ResultStruct fetch_data_struct(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::smoke::ListenersWithReturnValues::ResultStruct, ListenersWithReturnValues, fetch_data_struct);
    }
    ::smoke::ListenersWithReturnValues::ResultEnum fetch_data_enum(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::smoke::ListenersWithReturnValues::ResultEnum, ListenersWithReturnValues, fetch_data_enum);
    }
    ::std::vector< double > fetch_data_array(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::vector< double >, ListenersWithReturnValues, fetch_data_array);
    }
    ::std::unordered_map< ::std::string, double > fetch_data_map(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::unordered_map< ::std::string, double >, ListenersWithReturnValues, fetch_data_map);
    }
    ::std::shared_ptr< ::smoke::CalculationResult > fetch_data_instance(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::shared_ptr< ::smoke::CalculationResult >, ListenersWithReturnValues, fetch_data_instance);
    }
};

void register_ListenersWithReturnValues(py::module_& module) {
    py::class_<ListenersWithReturnValues, std::shared_ptr<ListenersWithReturnValues>, ListenersWithReturnValuesTrampoline>(module, "ListenersWithReturnValues")
        .def(py::init<>())
        .def("fetch_data_double", &ListenersWithReturnValues::fetch_data_double)
        .def("fetch_data_string", &ListenersWithReturnValues::fetch_data_string)
        .def("fetch_data_struct", &ListenersWithReturnValues::fetch_data_struct)
        .def("fetch_data_enum", &ListenersWithReturnValues::fetch_data_enum)
        .def("fetch_data_array", &ListenersWithReturnValues::fetch_data_array)
        .def("fetch_data_map", &ListenersWithReturnValues::fetch_data_map)
        .def("fetch_data_instance", &ListenersWithReturnValues::fetch_data_instance)
        ;
}

