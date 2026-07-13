

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/InterfaceWithStatic.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InterfaceWithStatic = ::gluecodium::smoke::InterfaceWithStatic;

class InterfaceWithStaticTrampoline : public InterfaceWithStatic {
public:
    using InterfaceWithStatic::InterfaceWithStatic;

    ::std::string regular_function(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::string, InterfaceWithStatic, regular_function);
    }
    ::std::string& get_regular_property() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::string&, InterfaceWithStatic, get_regular_property);
    }
    void set_regular_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, InterfaceWithStatic, set_regular_property, value);
    }
    ::std::string& get_static_property() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::string&, InterfaceWithStatic, get_static_property);
    }
    void set_static_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, InterfaceWithStatic, set_static_property, value);
    }
};

void register_InterfaceWithStatic(py::module_& module) {
    py::class_<InterfaceWithStatic, std::shared_ptr<InterfaceWithStatic>, InterfaceWithStaticTrampoline>(module, "InterfaceWithStatic")
        .def("regular_function", &InterfaceWithStatic::regular_function)
        .def("static_function", &InterfaceWithStatic::static_function)
        .def_property("regular_property", py::overload_cast<>(&InterfaceWithStatic::get_regular_property, py::const_), py::overload_cast<const ::std::string&>(&InterfaceWithStatic::set_regular_property))
        .def_property("static_property", py::overload_cast<>(&InterfaceWithStatic::get_static_property, py::const_), py::overload_cast<const ::std::string&>(&InterfaceWithStatic::set_static_property))
        ;
}

