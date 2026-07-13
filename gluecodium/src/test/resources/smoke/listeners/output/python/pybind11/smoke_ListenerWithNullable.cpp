

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ListenerWithNullable.h"
#include "cstdint"
#include "optional"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ListenerWithNullable = ::gluecodium::smoke::ListenerWithNullable;

class ListenerWithNullableTrampoline : public ListenerWithNullable {
public:
    using ListenerWithNullable::ListenerWithNullable;

    std::optional< int8_t > method_with_byte(
            const std::optional< int8_t >& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(std::optional< int8_t >, ListenerWithNullable, method_with_byte, input);
    }
    std::optional< uint8_t > method_with_u_byte(
            const std::optional< uint8_t >& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(std::optional< uint8_t >, ListenerWithNullable, method_with_u_byte, input);
    }
    std::optional< int16_t > method_with_short(
            const std::optional< int16_t >& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(std::optional< int16_t >, ListenerWithNullable, method_with_short, input);
    }
    std::optional< uint16_t > method_with_u_short(
            const std::optional< uint16_t >& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(std::optional< uint16_t >, ListenerWithNullable, method_with_u_short, input);
    }
    std::optional< int32_t > method_with_int(
            const std::optional< int32_t >& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(std::optional< int32_t >, ListenerWithNullable, method_with_int, input);
    }
    std::optional< uint32_t > method_with_u_int(
            const std::optional< uint32_t >& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(std::optional< uint32_t >, ListenerWithNullable, method_with_u_int, input);
    }
    std::optional< int64_t > method_with_long(
            const std::optional< int64_t >& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(std::optional< int64_t >, ListenerWithNullable, method_with_long, input);
    }
    std::optional< uint64_t > method_with_u_long(
            const std::optional< uint64_t >& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(std::optional< uint64_t >, ListenerWithNullable, method_with_u_long, input);
    }
    std::optional< bool > method_with_double(
            const std::optional< bool >& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(std::optional< bool >, ListenerWithNullable, method_with_double, input);
    }
    std::optional< float > method_with_float(
            const std::optional< float >& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(std::optional< float >, ListenerWithNullable, method_with_float, input);
    }
    std::optional< double > method_with_double(
            const std::optional< double >& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(std::optional< double >, ListenerWithNullable, method_with_double, input);
    }
};

void register_ListenerWithNullable(py::module_& module) {
    py::class_<ListenerWithNullable, std::shared_ptr<ListenerWithNullable>, ListenerWithNullableTrampoline>(module, "ListenerWithNullable")
        .def(py::init<>())
        .def("method_with_byte", &ListenerWithNullable::method_with_byte, py::arg("input"))
        .def("method_with_u_byte", &ListenerWithNullable::method_with_u_byte, py::arg("input"))
        .def("method_with_short", &ListenerWithNullable::method_with_short, py::arg("input"))
        .def("method_with_u_short", &ListenerWithNullable::method_with_u_short, py::arg("input"))
        .def("method_with_int", &ListenerWithNullable::method_with_int, py::arg("input"))
        .def("method_with_u_int", &ListenerWithNullable::method_with_u_int, py::arg("input"))
        .def("method_with_long", &ListenerWithNullable::method_with_long, py::arg("input"))
        .def("method_with_u_long", &ListenerWithNullable::method_with_u_long, py::arg("input"))
        .def("method_with_double", &ListenerWithNullable::method_with_double, py::arg("input"))
        .def("method_with_float", &ListenerWithNullable::method_with_float, py::arg("input"))
        .def("method_with_double", &ListenerWithNullable::method_with_double, py::arg("input"))
        ;
}

