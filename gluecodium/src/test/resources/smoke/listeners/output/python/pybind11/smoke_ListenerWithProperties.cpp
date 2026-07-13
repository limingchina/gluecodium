

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
#include "smoke/ListenerWithProperties.h"
#include "cstdint"
#include "memory"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ListenerWithProperties = ::gluecodium::smoke::ListenerWithProperties;

class ListenerWithPropertiesTrampoline : public ListenerWithProperties {
public:
    using ListenerWithProperties::ListenerWithProperties;

    ::std::string& get_message() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::string&, ListenerWithProperties, get_message);
    }
    void set_message(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ListenerWithProperties, set_message, value);
    }
    ::std::shared_ptr< ::smoke::CalculationResult >& get_packed_message() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::shared_ptr< ::smoke::CalculationResult >&, ListenerWithProperties, get_packed_message);
    }
    void set_packed_message(const ::std::shared_ptr< ::smoke::CalculationResult >& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ListenerWithProperties, set_packed_message, value);
    }
    ::smoke::ListenerWithProperties::ResultStruct& get_structured_message() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::smoke::ListenerWithProperties::ResultStruct&, ListenerWithProperties, get_structured_message);
    }
    void set_structured_message(const ::smoke::ListenerWithProperties::ResultStruct& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ListenerWithProperties, set_structured_message, value);
    }
    ::smoke::ListenerWithProperties::ResultEnum get_enumerated_message() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::smoke::ListenerWithProperties::ResultEnum, ListenerWithProperties, get_enumerated_message);
    }
    void set_enumerated_message(const ::smoke::ListenerWithProperties::ResultEnum value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ListenerWithProperties, set_enumerated_message, value);
    }
    ::std::vector< ::std::string >& get_arrayed_message() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::vector< ::std::string >&, ListenerWithProperties, get_arrayed_message);
    }
    void set_arrayed_message(const ::std::vector< ::std::string >& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ListenerWithProperties, set_arrayed_message, value);
    }
    ::std::unordered_map< ::std::string, double >& get_mapped_message() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::unordered_map< ::std::string, double >&, ListenerWithProperties, get_mapped_message);
    }
    void set_mapped_message(const ::std::unordered_map< ::std::string, double >& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ListenerWithProperties, set_mapped_message, value);
    }
    ::std::shared_ptr< ::std::vector< uint8_t > >& get_buffered_message() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::shared_ptr< ::std::vector< uint8_t > >&, ListenerWithProperties, get_buffered_message);
    }
    void set_buffered_message(const ::std::shared_ptr< ::std::vector< uint8_t > >& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ListenerWithProperties, set_buffered_message, value);
    }
};

void register_ListenerWithProperties(py::module_& module) {
    py::class_<ListenerWithProperties, std::shared_ptr<ListenerWithProperties>, ListenerWithPropertiesTrampoline>(module, "ListenerWithProperties")
        .def_property("message", py::overload_cast<>(&ListenerWithProperties::get_message, py::const_), py::overload_cast<const ::std::string&>(&ListenerWithProperties::set_message))
        .def_property("packed_message", py::overload_cast<>(&ListenerWithProperties::get_packed_message, py::const_), py::overload_cast<const ::std::shared_ptr< ::smoke::CalculationResult >&>(&ListenerWithProperties::set_packed_message))
        .def_property("structured_message", py::overload_cast<>(&ListenerWithProperties::get_structured_message, py::const_), py::overload_cast<const ::smoke::ListenerWithProperties::ResultStruct&>(&ListenerWithProperties::set_structured_message))
        .def_property("enumerated_message", py::overload_cast<>(&ListenerWithProperties::get_enumerated_message, py::const_), py::overload_cast<const ::smoke::ListenerWithProperties::ResultEnum>(&ListenerWithProperties::set_enumerated_message))
        .def_property("arrayed_message", py::overload_cast<>(&ListenerWithProperties::get_arrayed_message, py::const_), py::overload_cast<const ::std::vector< ::std::string >&>(&ListenerWithProperties::set_arrayed_message))
        .def_property("mapped_message", py::overload_cast<>(&ListenerWithProperties::get_mapped_message, py::const_), py::overload_cast<const ::std::unordered_map< ::std::string, double >&>(&ListenerWithProperties::set_mapped_message))
        .def_property("buffered_message", py::overload_cast<>(&ListenerWithProperties::get_buffered_message, py::const_), py::overload_cast<const ::std::shared_ptr< ::std::vector< uint8_t > >&>(&ListenerWithProperties::set_buffered_message))
        ;
}

