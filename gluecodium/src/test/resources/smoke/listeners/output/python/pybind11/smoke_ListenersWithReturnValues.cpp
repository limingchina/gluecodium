

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
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/CalculationResult.h"
#include "smoke/ListenersWithReturnValues.h"
#include "memory"
#include "string"
#include "unordered_map"
#include "vector"

using ListenersWithReturnValues = ::smoke::ListenersWithReturnValues;
using ResultStruct = ::smoke::ListenersWithReturnValues::ResultStruct;
using ResultEnum = ::smoke::ListenersWithReturnValues::ResultEnum;

class ListenersWithReturnValuesTrampoline : public ListenersWithReturnValues {
public:
    using ListenersWithReturnValues::ListenersWithReturnValues;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ListenersWithReturnValues> m_impl;

    double fetch_data_double(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->fetch_data_double();
        }
        PYBIND11_OVERRIDE_PURE(double, ListenersWithReturnValues, fetch_data_double);
    }
    ::std::string fetch_data_string(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->fetch_data_string();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, ListenersWithReturnValues, fetch_data_string);
    }
    ::smoke::ListenersWithReturnValues::ResultStruct fetch_data_struct(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->fetch_data_struct();
        }
        PYBIND11_OVERRIDE_PURE(::smoke::ListenersWithReturnValues::ResultStruct, ListenersWithReturnValues, fetch_data_struct);
    }
    ::smoke::ListenersWithReturnValues::ResultEnum fetch_data_enum(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->fetch_data_enum();
        }
        PYBIND11_OVERRIDE_PURE(::smoke::ListenersWithReturnValues::ResultEnum, ListenersWithReturnValues, fetch_data_enum);
    }
    ::std::vector< double > fetch_data_array(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->fetch_data_array();
        }
        PYBIND11_OVERRIDE_PURE(::std::vector< double >, ListenersWithReturnValues, fetch_data_array);
    }
    using fetch_data_map_return_type = ::std::unordered_map< ::std::string, double >;
    ::std::unordered_map< ::std::string, double > fetch_data_map(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->fetch_data_map();
        }
        PYBIND11_OVERRIDE_PURE(fetch_data_map_return_type, ListenersWithReturnValues, fetch_data_map);
    }
    ::std::shared_ptr< ::smoke::CalculationResult > fetch_data_instance(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->fetch_data_instance();
        }
        PYBIND11_OVERRIDE_PURE(::std::shared_ptr< ::smoke::CalculationResult >, ListenersWithReturnValues, fetch_data_instance);
    }
};



void register_smoke_ListenersWithReturnValues(py::module_& module) {
auto cls_ListenersWithReturnValues = py::class_<ListenersWithReturnValues, std::shared_ptr<ListenersWithReturnValues>, ListenersWithReturnValuesTrampoline>(module, "smoke_ListenersWithReturnValues")
        .def("__gluecodium_id__", [](const ListenersWithReturnValues& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<ListenersWithReturnValues> native) {
            auto self = std::make_shared<ListenersWithReturnValuesTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("fetch_data_double", [](ListenersWithReturnValues& self) {
            return self.fetch_data_double();
        })
        .def("fetch_data_string", [](ListenersWithReturnValues& self) {
            return self.fetch_data_string();
        })
        .def("fetch_data_struct", [](ListenersWithReturnValues& self) {
            return self.fetch_data_struct();
        })
        .def("fetch_data_enum", [](ListenersWithReturnValues& self) {
            return self.fetch_data_enum();
        })
                .def("fetch_data_array", [](ListenersWithReturnValues& self) -> py::object {
                        return gluecodium::python::to_python_regular(self.fetch_data_array());
                })
                .def("fetch_data_map", [](ListenersWithReturnValues& self) -> py::object {
                        return gluecodium::python::to_python_regular(self.fetch_data_map());
                })
        .def("fetch_data_instance", [](ListenersWithReturnValues& self) {
            return self.fetch_data_instance();
        })
        ;

auto cls_ListenersWithReturnValuesResultStruct = py::class_<ResultStruct>(cls_ListenersWithReturnValues, "ResultStruct")
        .def_readwrite("result", &ResultStruct::result)
        .def(py::init<>())
        .def(py::init<double>(), py::arg("result"))
        ;

auto cls_ListenersWithReturnValuesResultEnum = py::enum_<ResultEnum>(cls_ListenersWithReturnValues, "ResultEnum")
        .value("NONE", ResultEnum::NONE)
        .value("RESULT", ResultEnum::RESULT)
        ;


}
